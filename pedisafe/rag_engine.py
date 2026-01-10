"""
PediSafe RAG Engine
Motor de Generación Aumentada por Recuperación usando FAISS (gratuito)
"""

import os
from pathlib import Path
from typing import List, Tuple

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import get_system_prompt, get_rag_template, TRIAGE_RULES


class PediSafeRAG:
    """Motor RAG para el asistente de triaje pediátrico"""
    
    def __init__(self, api_key: str, knowledge_dir: str = "knowledge", language: str = "en", provider: str = "openai"):
        self.api_key = api_key
        self.knowledge_dir = Path(knowledge_dir)
        self.language = language
        self.provider = provider
        self.vectorstore = None
        self.retriever = None
        self.chain = None
        
        # Initialize components
        self._setup_embeddings()
        self._load_knowledge_base()
        self._setup_chain()
    
    def _setup_embeddings(self):
        """Configura embeddings según el proveedor"""
        if self.provider == "cerebras":
            # Cerebras no tiene embeddings propios
            # Usar Hugging Face embeddings (100% GRATIS, sin API key necesaria)
            print("🆓 Usando embeddings gratuitos de Hugging Face (sentence-transformers)")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            self.embeddings = OpenAIEmbeddings(
                api_key=self.api_key,
                model="text-embedding-3-small"  # Más barato: $0.02/1M tokens
            )
    
    def _load_knowledge_base(self):
        """Carga y vectoriza los documentos de conocimiento con estrategia optimizada"""
        # Load markdown files
        loader = DirectoryLoader(
            str(self.knowledge_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        
        # RAG Best Practice: Hierarchical chunking con overlap adecuado
        # chunk_size: 800-1200 tokens es óptimo para medical context
        # overlap: 150-250 para preservar contexto entre chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Tamaño óptimo para contexto médico
            chunk_overlap=200,  # 20% overlap para coherencia
            separators=[
                "\n## ",      # Secciones principales (H2)
                "\n### ",     # Subsecciones (H3)
                "\n#### ",    # Sub-subsecciones (H4)
                "\n\n",       # Párrafos
                "\n",         # Líneas
                ". ",         # Oraciones
                " "           # Palabras (último recurso)
            ],
            length_function=len,
            is_separator_regex=False
        )
        splits = text_splitter.split_documents(documents)
        
        # RAG Best Practice: FAISS con IndexFlatL2 para búsqueda exacta
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        
        # RAG Best Practice: Hybrid search con MMR para diversidad
        # MMR (Maximal Marginal Relevance) reduce redundancia en resultados
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",  # MMR en lugar de similarity para mayor diversidad
            search_kwargs={
                "k": 6,              # Top 6 chunks (mejor cobertura)
                "fetch_k": 20,       # Fetch 20, luego MMR selecciona 6
                "lambda_mult": 0.7   # Balance relevancia (1.0) vs diversidad (0.0)
            }
        )
    
    def _setup_chain(self):
        """Configura la cadena RAG con LangChain"""
        if self.provider == "cerebras":
            # Cerebras API es compatible con OpenAI SDK
            llm = ChatOpenAI(
                api_key=self.api_key,
                model="llama-3.3-70b",
                base_url="https://api.cerebras.ai/v1",
                temperature=0.3
            )
        else:
            llm = ChatOpenAI(
                api_key=self.api_key,
                model="gpt-4o-mini",  # Más barato: $0.15/1M input, $0.60/1M output
                temperature=0.3  # Bajo para respuestas más consistentes
            )
        
        # Create prompt template with language support
        system_prompt = get_system_prompt(self.language)
        rag_template = get_rag_template(self.language)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", rag_template)
        ])
        
        self.llm = llm
        self.prompt = prompt
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Formatea documentos recuperados para el contexto con URLs específicas"""
        import re
        formatted = []
        
        # Map de archivos a URLs específicas - SOLO fuentes oficiales AAP/NHS
        # NO incluir documentos internos consolidados o ejemplos
        source_urls = {
            "aap_fever_baby.md": ("Fever and Your Baby - AAP", "https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-and-Your-Baby.aspx"),
            "aap_fever_without_fear.md": ("Fever Without Fear - AAP", "https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-Without-Fear.aspx"),
            "aap_symptom_checker.md": ("Symptom Checker: Fever - AAP", "https://www.healthychildren.org/English/tips-tools/symptom-checker/Pages/symptomviewer.aspx?symptom=Fever+(0-12+Months)"),
            "aap_when_to_call.md": ("When to Call the Pediatrician - AAP", "https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/When-to-Call-the-Pediatrician.aspx"),
            "nhs_fever_children.md": ("High Temperature in Children - NHS", "https://www.nhs.uk/conditions/fever-in-children/"),
        }
        
        for i, doc in enumerate(docs, 1):
            source_path = doc.metadata.get("source", "Unknown")
            # Extraer nombre del archivo
            source_file = Path(source_path).name if source_path != "Unknown" else "Unknown"
            
            # Obtener título y URL específica
            if source_file in source_urls:
                title, url = source_urls[source_file]
                source_info = f"[{title}]({url})"
            else:
                source_info = source_file
            
            formatted.append(f"[Fragment {i}] Source: {source_info}\n{doc.page_content}")
        
        return "\n\n---\n\n".join(formatted)
    
    def _check_red_flags(self, message: str) -> Tuple[bool, str]:
        """Capa A: Verificación determinista de señales de alarma"""
        message_lower = message.lower()
        
        # CRÍTICO: Verificar edad + fiebre ANTES de buscar red flags textuales
        age_temp_data = self._extract_age_temp(message)
        
        # Regla AAP: CUALQUIER fiebre en <3 meses es EMERGENCIA
        if age_temp_data["age_months"] is not None and age_temp_data["temp_c"] is not None:
            age_months = age_temp_data["age_months"]
            temp_c = age_temp_data["temp_c"]
            
            # <3 meses con temp >= 38.0°C = RED FLAG automático
            if age_months < 3 and temp_c >= 38.0:
                return True, f"bebé <3 meses con fiebre {temp_c}°C"
            
            # 3-6 meses con temp >= 39.0°C = RED FLAG
            if 3 <= age_months < 6 and temp_c >= 39.0:
                return True, f"bebé 3-6 meses con fiebre alta {temp_c}°C"
        
        # Buscar red flags textuales (síntomas críticos)
        for flag in TRIAGE_RULES["red_flags"]:
            if flag.lower() in message_lower:
                return True, flag
        
        return False, ""
    
    def _extract_age_temp(self, message: str) -> dict:
        """Extrae edad y temperatura del mensaje con alta precisión"""
        import re
        
        result = {"age_months": None, "temp_c": None}
        message_lower = message.lower()
        
        # Buscar edad - PRIORIDAD: meses explícitos
        age_patterns = [
            (r"(\d+)\s*meses?", 1),           # "8 meses" -> meses
            (r"(\d+)\s*months?", 1),          # "8 months" -> meses
            (r"(\d+)\s*años?", 12),           # "3 años" -> 36 meses
            (r"(\d+)\s*years?", 12),          # "3 years" -> 36 meses
            (r"(\d+)\s*semanas?", 0.25),      # "4 semanas" -> 1 mes
            (r"(\d+)\s*weeks?", 0.25),        # "4 weeks" -> 1 mes
            (r"bebé?\s*de\s*(\d+)", 1),       # "bebé de 2" -> 2 meses
            (r"(\d+)[-\s]?(month|mes)", 1),   # "2-month" -> 2 meses
        ]
        
        for pattern, multiplier in age_patterns:
            match = re.search(pattern, message_lower)
            if match:
                age_value = float(match.group(1))
                result["age_months"] = int(age_value * multiplier)
                break
        
        # Buscar temperatura con múltiples formatos
        temp_patterns = [
            r"(\d+\.?\d*)\s*°?\s*[cC](?:\s|,|$)",  # 38.5°C o 38.5 C
            r"(\d+\.?\d*)\s*grados",                # 38.5 grados
            r"temperatura\s*:?\s*(\d+\.?\d*)",      # temperatura: 38.5
            r"(\d+\.?\d*)\s*°?\s*[fF]",             # 101°F (Fahrenheit)
            r"temp\w*\s*:?\s*(\d+\.?\d*)",          # temp: 38.5
        ]
        
        for pattern in temp_patterns:
            match = re.search(pattern, message_lower)
            if match:
                temp = float(match.group(1))
                # Detectar y convertir Fahrenheit
                if temp > 45 or 'f' in pattern.lower():
                    temp = (temp - 32) * 5/9
                result["temp_c"] = round(temp, 1)
                break
        
        return result
    
    def get_response(self, user_message: str, chat_history: str = "") -> str:
        """Genera respuesta usando RAG"""
        
        # Capa A: Verificar red flags primero
        has_red_flag, flag_found = self._check_red_flags(user_message)
        
        # Recuperar documentos relevantes
        docs = self.retriever.invoke(user_message)
        context = self._format_docs(docs)
        
        # Preparar el prompt
        if has_red_flag:
            enhanced_message = f"⚠️ ALERTA: El usuario menciona '{flag_found}' que es una señal de alarma. Prioriza la seguridad.\n\nMensaje original: {user_message}"
        else:
            enhanced_message = user_message
        
        # Generar respuesta
        messages = self.prompt.format_messages(
            context=context,
            chat_history=chat_history,
            user_message=enhanced_message
        )
        
        response = self.llm.invoke(messages)
        
        return response.content
    
    def get_sources(self) -> List[str]:
        """Retorna lista de fuentes cargadas"""
        sources = []
        for file in self.knowledge_dir.glob("**/*.md"):
            sources.append(file.name)
        return sources


def test_rag_engine():
    """Test básico del motor RAG"""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY to test")
        return
    
    rag = PediSafeRAG(api_key)
    response = rag.get_response("Mi bebé de 2 meses tiene 38.5°C de fiebre")
    print(response)


if __name__ == "__main__":
    test_rag_engine()
