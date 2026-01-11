# 🧪 Instrucciones para Recrear el Entorno de Testing PediSafe

Este documento explica paso a paso cómo configurar y ejecutar la suite de tests automáticos de PediSafe.

---

## 📋 Requisitos Previos

- **Python 3.12** o superior
- **Git** instalado
- **Conexión a Internet** (para descargar dependencias)
- **~2GB de espacio libre** (para dependencias de PyTorch)

---

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd 1_ALAMEDA_HACKS
```

### 2. Crear el Virtual Environment (VENV)

#### En Windows:
```powershell
# Crear venv
python -m venv venv

# Activar venv
venv\Scripts\activate

# Verificar que estás en el venv (deberías ver (venv) en el prompt)
```

#### En Linux/Mac:
```bash
# Crear venv
python3 -m venv venv

# Activar venv
source venv/bin/activate
```

### 3. Instalar Dependencias Base

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias principales
pip install -r pedisafe/requirements.txt
```

### 4. Instalar Dependencias de Testing

```bash
# Instalar herramientas de testing
pip install pytest pytest-html

# Instalar componentes de LangChain
pip install langchain-text-splitters langchain-core langchain-community langchain-openai

# Instalar embeddings y vectorstore
pip install sentence-transformers faiss-cpu
```

**Nota:** La instalación de `sentence-transformers` descargará ~110MB de PyTorch. Esto es normal y puede tomar varios minutos.

---

## ⚙️ Configuración del API Key

### Opción 1: Variable de Entorno (Recomendado)

#### Windows:
```powershell
# Temporal (solo esta sesión)
$env:CEREBRAS_API_KEY="tu-api-key-aqui"

# Permanente
setx CEREBRAS_API_KEY "tu-api-key-aqui"
```

#### Linux/Mac:
```bash
# Agregar a ~/.bashrc o ~/.zshrc
export CEREBRAS_API_KEY="tu-api-key-aqui"

# Cargar el cambio
source ~/.bashrc
```

### Opción 2: Archivo .env

```bash
# Crear archivo .env en la carpeta pedisafe/
echo "CEREBRAS_API_KEY=tu-api-key-aqui" > pedisafe/.env
```

**Nota:** El API key por defecto en los tests es: `csk-59knkfwehxxxckxcdw8f56mjxj3v8f6hm3239rtnxwf6cmjf`

---

## 🧪 Ejecutar los Tests

### Opción 1: Comando Directo

```bash
# Asegúrate de estar en la raíz del proyecto
cd d:\PROYECTOS\HACKATONES\1_DEVPOST\1_ALAMEDA_HACKS

# Activar venv (si no está activado)
venv\Scripts\activate

# Ejecutar todos los tests
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v

# Ejecutar solo tests críticos
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v -m critical

# Generar reporte HTML
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v --html=pedisafe/report.html --self-contained-html
```

### Opción 2: Script Batch (Windows)

```bash
# Ejecutar el script proporcionado
RUN_TESTS.bat
```

### Opción 3: Makefile (Linux/Mac)

```bash
# Crear un Makefile simple
make test
```

---

## 📊 Interpretar los Resultados

### Estados de Tests

- ✅ **PASSED** - Test exitoso
- ❌ **FAILED** - Test fallido (ver detalles en output)
- ⏭️ **SKIPPED** - Test omitido (generalmente por falta de configuración)

### Ejemplo de Output

```
============================================== test session starts ==============================================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
collected 16 items

pedisafe\test_pedisafe.py::test_critical_cases[Fever <3 months] PASSED                                    [  6%]
pedisafe\test_pedisafe.py::test_critical_cases[Red flag symptom] PASSED                                   [ 12%]
...
============================= 13 passed, 2 failed, 1 skipped in 38.25s ==============================
```

### Reporte HTML

Después de ejecutar con `--html=pedisafe/report.html`, abre el archivo en un navegador:

```bash
# Windows
start pedisafe/report.html

# Linux
xdg-open pedisafe/report.html

# Mac
open pedisafe/report.html
```

---

## 📁 Estructura de Archivos de Testing

```
1_ALAMEDA_HACKS/
├── pedisafe/
│   ├── test_pedisafe.py          # Suite principal de tests
│   ├── test_rag_simple.py        # Test diagnóstico simple
│   ├── pytest.ini                # Configuración de pytest
│   ├── report.html               # Reporte HTML generado
│   ├── TEST_README.md            # Documentación de tests
│   └── TEST_RESULTS.md           # Resultados y análisis
├── RUN_TESTS.bat                 # Script de ejecución Windows
├── TESTS_FINALES.md              # Resumen de resultados
└── SETUP_TESTS.md                # Este archivo
```

---

## 🔍 Casos de Test Incluidos

### Tests Críticos de Seguridad (8 casos)

1. **Fiebre en bebés <3 meses** (3 variantes)
   - 2 meses, 38.2°C → Debe ser RED
   - 1 mes, 38.0°C → Debe ser RED
   - 10 semanas → Debe ser RED

2. **Red flags de emergencia**
   - Dificultad respiratoria → RED
   - Convulsión → RED
   - Alta fiebre + deshidratación → ORANGE

3. **Fiebre moderada/baja**
   - 6-12 meses sin signos de alarma → YELLOW
   - 5 años con fiebre baja → GREEN

### Edge Cases (4 casos)

- Fiebre persistente >72 horas
- Temperatura alta con buen comportamiento
- Comportamiento alterado
- Erupción no blanqueable

### Validación de Falsos Positivos (2 casos)

- 37.8°C NO es fiebre → GREEN
- 37.5°C temperatura normal → GREEN

### Validación de Sistema (2 casos)

- Citas de fuentes AAP/NHS
- Presencia de disclaimers

---

## ⚠️ Problemas Comunes y Soluciones

### Error: "No module named 'langchain_text_splitters'"

**Solución:**
```bash
venv\Scripts\python.exe -m pip install langchain-text-splitters langchain-core
```

### Error: "No module named 'sentence_transformers'"

**Solución:**
```bash
venv\Scripts\python.exe -m pip install sentence-transformers
```

### Error: "Could not initialize RAG engine"

**Causas posibles:**
1. API key no configurado
2. No hay conexión a Internet
3. Archivos de knowledge base faltantes

**Verificar:**
```bash
# Verificar que existen los archivos .md en knowledge/
dir pedisafe\knowledge\*.md

# Debería listar 5 archivos:
# - aap_fever_baby.md
# - aap_fever_without_fear.md
# - aap_symptom_checker.md
# - aap_when_to_call.md
# - nhs_fever_children.md
```

### Error: "pytest: command not found"

**Solución:**
```bash
# Usar el módulo de Python en lugar del comando directo
venv\Scripts\python.exe -m pytest ...
```

### Tests muy lentos (>2 minutos)

**Causas:**
- Primera ejecución descargando modelos de embeddings
- Generación del índice FAISS

**Solución:** La primera ejecución es lenta. Las siguientes serán más rápidas.

---

## 🔄 Actualizar Dependencias

```bash
# Activar venv
venv\Scripts\activate

# Actualizar todas las dependencias
pip install --upgrade -r pedisafe/requirements.txt
pip install --upgrade pytest pytest-html sentence-transformers

# Verificar versiones instaladas
pip list
```

---

## 🧹 Limpiar y Recrear el Entorno

### Si algo sale mal, recrear desde cero:

```bash
# 1. Desactivar venv
deactivate

# 2. Eliminar venv
rmdir /s /q venv

# 3. Recrear venv
python -m venv venv
venv\Scripts\activate

# 4. Reinstalar todo
pip install --upgrade pip
pip install -r pedisafe/requirements.txt
pip install pytest pytest-html
pip install langchain-text-splitters langchain-core langchain-community langchain-openai
pip install sentence-transformers faiss-cpu

# 5. Ejecutar tests
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v
```

---

## 📊 Criterios de Éxito

Para considerar que el sistema está listo:

✅ **Mínimo 80% de tests pasando** (13/16 o mejor)  
✅ **100% de tests críticos <3 meses pasando** (0 falsos negativos)  
✅ **0 alucinaciones detectadas**  
✅ **Fuentes AAP/NHS correctamente citadas**

---

## 📝 Notas Adicionales

### Ignorar en Git

El archivo `.gitignore` ya está configurado para ignorar:
- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`
- `.env`

### Tiempo de Ejecución Esperado

- **Primera ejecución:** 50-90 segundos (descarga de modelos)
- **Ejecuciones siguientes:** 30-40 segundos
- **Solo tests críticos:** 15-20 segundos

### Recursos del Sistema

- **RAM:** ~2GB durante ejecución de tests
- **Espacio disco:** ~1.5GB para venv con todas las dependencias
- **CPU:** Uso normal (no requiere GPU)

---

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que el venv está activado
2. Confirma que todas las dependencias están instaladas
3. Revisa los logs de error completos
4. Consulta `TEST_README.md` para detalles de cada test
5. Revisa `TESTS_FINALES.md` para resultados esperados

---

## ✅ Checklist de Verificación

Antes de reportar que los tests funcionan:

- [ ] Venv creado y activado
- [ ] Todas las dependencias instaladas sin errores
- [ ] API key configurado
- [ ] 5 archivos .md presentes en `knowledge/` (AAP: 4, NHS: 1)
- [ ] Tests ejecutándose sin errores de importación
- [ ] Al menos 13/16 tests pasando
- [ ] `report.html` generado correctamente
- [ ] Reporte abre en navegador y muestra resultados

---

**Última actualización:** 2026-01-09  
**Versión Python probada:** 3.12.1  
**Plataforma probada:** Windows 10  
**Estado:** ✅ Funcionando
