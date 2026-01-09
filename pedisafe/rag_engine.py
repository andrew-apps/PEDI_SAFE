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
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import SYSTEM_PROMPT, RAG_TEMPLATE, TRIAGE_RULES


class PediSafeRAG:
    """Motor RAG para el asistente de triaje pediátrico"""
    
    def __init__(self, api_key: str, knowledge_dir: str = "knowledge"):
        self.api_key = api_key
        self.knowledge_dir = Path(knowledge_dir)
        self.vectorstore = None
        self.retriever = None
        self.chain = None
        
        # Initialize components
        self._setup_embeddings()
        self._load_knowledge_base()
        self._setup_chain()
    
    def _setup_embeddings(self):
        """Configura embeddings de OpenAI (text-embedding-3-small es más barato)"""
        self.embeddings = OpenAIEmbeddings(
            api_key=self.api_key,
            model="text-embedding-3-small"  # Más barato: $0.02/1M tokens
        )
    
    def _load_knowledge_base(self):
        """Carga y vectoriza los documentos de conocimiento"""
        # Load markdown files
        loader = DirectoryLoader(
            str(self.knowledge_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n## ", "\n### ", "\n", " "]
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store with FAISS (gratuito, local)
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # Top 5 chunks más relevantes
        )
    
    def _setup_chain(self):
        """Configura la cadena RAG con LangChain"""
        # Use GPT-4o-mini for cost efficiency
        llm = ChatOpenAI(
            api_key=self.api_key,
            model="gpt-4o-mini",  # Más barato: $0.15/1M input, $0.60/1M output
            temperature=0.3  # Bajo para respuestas más consistentes
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", RAG_TEMPLATE)
        ])
        
        self.llm = llm
        self.prompt = prompt
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Formatea documentos recuperados para el contexto"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            formatted.append(f"[Fragmento {i}] (Fuente: {source})\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)
    
    def _check_red_flags(self, message: str) -> Tuple[bool, str]:
        """Capa A: Verificación determinista de señales de alarma"""
        message_lower = message.lower()
        
        for flag in TRIAGE_RULES["red_flags"]:
            if flag.lower() in message_lower:
                return True, flag
        
        return False, ""
    
    def _extract_age_temp(self, message: str) -> dict:
        """Extrae edad y temperatura del mensaje si están presentes"""
        import re
        
        result = {"age_months": None, "temp_c": None}
        
        # Buscar edad en meses
        age_patterns = [
            r"(\d+)\s*meses?",
            r"(\d+)\s*months?",
            r"bebé?\s*de\s*(\d+)",
        ]
        for pattern in age_patterns:
            match = re.search(pattern, message.lower())
            if match:
                result["age_months"] = int(match.group(1))
                break
        
        # Buscar temperatura
        temp_patterns = [
            r"(\d+\.?\d*)\s*°?\s*[cC]",
            r"(\d+\.?\d*)\s*grados",
            r"temperatura\s*:?\s*(\d+\.?\d*)",
        ]
        for pattern in temp_patterns:
            match = re.search(pattern, message)
            if match:
                temp = float(match.group(1))
                # Si parece Fahrenheit, convertir
                if temp > 45:
                    temp = (temp - 32) * 5/9
                result["temp_c"] = temp
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
