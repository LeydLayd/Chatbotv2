# 🤖 Chatbot Lina v2.0 - Asistente Médico con IA

Un chatbot médico especializado en diabetes que combina cuestionarios estructurados con inteligencia artificial (Gemini 2.5 Flash) para generar expedientes médicos completos y personalizados.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Reference](#-api-reference)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🏥 **Sistema Médico Inteligente**
- **Cuestionario estructurado** con 20+ preguntas médicas especializadas
- **Preguntas condicionales** que se adaptan a las respuestas del paciente
- **Resúmenes clínicos automáticos** generados por IA
- **Preguntas complementarias dinámicas** personalizadas para cada paciente

### 🤖 **Inteligencia Artificial**
- **Gemini 2.5 Flash** para análisis médico avanzado
- **Generación de resúmenes clínicos** profesionales
- **Preguntas complementarias inteligentes** basadas en el contexto
- **Validación de respuestas** médicas

### 📊 **Integración de Datos**
- **Google Sheets** para almacenamiento automático
- **Estructura organizada** por columnas
- **Sincronización en tiempo real**

### 🎨 **Interfaz de Usuario**
- **Chat interactivo** con Streamlit
- **Diseño responsivo** y moderno
- **Controles intuitivos** (regresar, progreso)
- **Indicadores visuales** de estado

## 🏗️ Arquitectura

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit UI] --> B[Chat Interface]
        A --> C[Progress Indicators]
        A --> D[Privacy Notice]
    end
    
    subgraph "Application Layer"
        E[Main Controller] --> F[Session Management]
        E --> G[Question Engine]
        E --> H[Response Processor]
    end
    
    subgraph "AI Layer"
        I[Gemini Connector] --> J[Clinical Summary Generator]
        I --> K[Complementary Questions Generator]
        I --> L[Response Validator]
    end
    
    subgraph "Data Layer"
        M[Questions Database] --> N[Personal Questions]
        M --> O[Medical History]
        M --> P[Lifestyle Habits]
        M --> Q[Diabetes Symptoms]
        
        R[Google Sheets] --> S[Patient Data Storage]
        R --> T[Clinical Records]
    end
    
    subgraph "External Services"
        U[Google Gemini API] --> I
        V[Google Sheets API] --> R
    end
    
    A --> E
    E --> I
    E --> M
    E --> R
    I --> U
    R --> V
    
    style A fill:#e1f5fe
    style I fill:#f3e5f5
    style R fill:#e8f5e8
    style U fill:#fff3e0
    style V fill:#fff3e0
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de Google Cloud Platform
- API Key de Google Gemini
- Cuenta de Google Sheets

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd Chatbotv2
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crear archivo `.streamlit/secrets.toml`:

```toml
[GEMINI_API_KEY]
api_key = "tu_api_key_de_gemini"

[gcp_service_account]
type = "service_account"
project_id = "tu_proyecto_id"
private_key_id = "tu_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\ntu_private_key\n-----END PRIVATE KEY-----\n"
client_email = "tu_service_account@tu_proyecto.iam.gserviceaccount.com"
client_id = "tu_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/tu_service_account%40tu_proyecto.iam.gserviceaccount.com"
```

## ⚙️ Configuración

### 1. Google Gemini API

1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crear una nueva API Key
3. Copiar la key al archivo `secrets.toml`

### 2. Google Sheets API

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto o seleccionar existente
3. Habilitar Google Sheets API y Google Drive API
4. Crear una Service Account
5. Descargar el archivo JSON de credenciales
6. Convertir el JSON a formato TOML para `secrets.toml`
7. Crear una hoja de cálculo en Google Sheets llamada "Lina"
8. Compartir la hoja con el email de la Service Account

### 3. Estructura de Google Sheets

La hoja debe tener las siguientes columnas (se crean automáticamente):

```
nombre_completo | edad | sexo | fecha_nacimiento | domicilio | telefono | ocupacion | estado_civil | contacto_emergencia | diagnosticado_diabetes | fecha_diagnostico | medicamento_actual | hipertension | colesterol | cardiaco | renal | vision | piel | neuropatias | hospitalizaciones | fam_diabetes | fam_hipertension | fam_cardiaco | fam_renal | fam_obesidad | familiares_diagnosticados | fuma | cigarrillos_dia | alcohol | frecuencia_alcohol | actividad_fisica | tipo_actividad | frecuencia_actividad | glucosa_en_casa | frecuencia_glucosa | promedio_glucosa | plan_alimenticio | sed_excesiva | miccion_frecuente | hambre_excesiva | cansancio_constante | perdida_peso | hormigueo
```

## 🎯 Uso

### Ejecutar la Aplicación

```bash
streamlit run chatbot_v2_gemini.py
```

### Flujo de Uso

1. **Aceptar Aviso de Privacidad**
   - El usuario debe aceptar el aviso antes de continuar

2. **Cuestionario Base**
   - 20+ preguntas estructuradas sobre:
     - Datos personales
     - Antecedentes médicos
     - Hábitos de vida
     - Síntomas de diabetes

3. **Resumen Clínico**
   - Generación automática con IA
   - Visible en el sidebar

4. **Preguntas Complementarias**
   - 5 preguntas dinámicas personalizadas
   - Basadas en el contexto del paciente

5. **Almacenamiento**
   - Guardado automático en Google Sheets

### Controles de la Interfaz

- **Chat Input**: Escribir respuestas
- **Botón Regresar**: Corregir respuesta anterior
- **Sidebar**: Ver progreso y resumen clínico

## 📁 Estructura del Proyecto

```
Chatbotv2/
├── chatbot_v2_gemini.py          # Aplicación principal
├── connector_gemini.py           # Conector de IA
├── google_sheets_connector.py    # Conector de Google Sheets
├── preguntas/
│   └── Preguntas.py              # Base de datos de preguntas
├── requirements.txt              # Dependencias
├── README.md                     # Documentación
└── .streamlit/
    └── secrets.toml              # Configuración (crear)
```

### Descripción de Archivos

#### `chatbot_v2_gemini.py`
- **Propósito**: Aplicación principal de Streamlit
- **Funciones principales**:
  - Gestión de sesión y estado
  - Interfaz de usuario
  - Control de flujo del cuestionario
  - Integración con IA y Google Sheets

#### `connector_gemini.py`
- **Propósito**: Conector para Google Gemini API
- **Clases principales**:
  - `GeminiConnector`: Conector principal
  - `GenerarResumen`: Wrapper para resúmenes
  - `GenerarPregunta`: Wrapper para preguntas

#### `google_sheets_connector.py`
- **Propósito**: Integración con Google Sheets
- **Funcionalidades**:
  - Autenticación con Service Account
  - Guardado de datos de pacientes
  - Manejo de estructura de columnas

#### `preguntas/Preguntas.py`
- **Propósito**: Base de datos de preguntas médicas
- **Categorías**:
  - `preguntas_personales`: Datos demográficos
  - `pregunta_prediagnostico`: Diagnóstico de diabetes
  - `preguntas_antecedentes`: Historial médico
  - `fumar`, `alcohol`, `actividad`: Hábitos de vida
  - `glucosa`: Monitoreo de glucosa
  - `alimenticio`: Síntomas diabéticos

## 📚 API Reference

### Clase `GeminiConnector`

#### `__init__()`
Inicializa el conector con la API key de Gemini.

#### `generar_resumen(historial: str) -> Optional[str]`
Genera un resumen clínico del historial médico.

**Parámetros:**
- `historial`: Conversación completa doctor-paciente

**Retorna:**
- Resumen clínico en formato profesional (máximo 100 palabras)

#### `generar_pregunta_complementaria(resumen: str, ultimas_preguntas: list, numero_pregunta: int) -> Optional[str]`
Genera una pregunta complementaria basada en el contexto.

**Parámetros:**
- `resumen`: Resumen clínico del paciente
- `ultimas_preguntas`: Lista de las últimas preguntas/respuestas
- `numero_pregunta`: Número de pregunta (1-5)

**Retorna:**
- Pregunta médica relevante y específica

#### `validar_respuesta(pregunta: str, respuesta: str) -> tuple[bool, str]`
Valida si una respuesta es apropiada médicamente.

**Parámetros:**
- `pregunta`: La pregunta realizada
- `respuesta`: La respuesta del paciente

**Retorna:**
- `(es_valida, mensaje_feedback)`

### Clase `GoogleSheetsConnector`

#### `__init__(sheet_name: str)`
Inicializa el conector con el nombre de la hoja.

#### `guardar_fila(datos: dict)`
Guarda los datos del paciente en Google Sheets.

**Parámetros:**
- `datos`: Diccionario con las respuestas del paciente

### Funciones de Preguntas

#### Preguntas Condicionales
Las preguntas pueden tener respuestas condicionales que insertan preguntas adicionales:

```python
{
    "texto": "¿Fumas actualmente?",
    "clave": "fuma",
    "condicional": {
        "si": [{"texto": "¿Cuántos cigarrillos al día?", "clave": "cigarrillos_dia"}],
        "sí": [{"texto": "¿Cuántos cigarrillos al día?", "clave": "cigarrillos_dia"}]
    }
}
```

## 🔧 Desarrollo

### Agregar Nuevas Preguntas

1. Editar `preguntas/Preguntas.py`
2. Agregar la nueva pregunta a la lista correspondiente
3. Definir la clave única para la pregunta
4. Agregar lógica condicional si es necesario

### Modificar la Lógica de IA

1. Editar `connector_gemini.py`
2. Modificar los prompts en las funciones correspondientes
3. Ajustar los parámetros de validación

### Personalizar la Interfaz

1. Editar `chatbot_v2_gemini.py`
2. Modificar la configuración de Streamlit
3. Ajustar los estilos y componentes

## 🐛 Solución de Problemas

### Error de API Key
```
Error al inicializar Gemini: Invalid API key
```
**Solución**: Verificar que la API key esté correctamente configurada en `secrets.toml`

### Error de Google Sheets
```
Error al guardar en Google Sheets: Access denied
```
**Solución**: Verificar que la Service Account tenga permisos de escritura en la hoja

### Error de Dependencias
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solución**: Instalar las dependencias con `pip install -r requirements.txt`

## 📊 Monitoreo y Logs

El sistema incluye logging básico para:
- Errores de API
- Fallos de conexión
- Respuestas vacías de IA

Los logs se muestran en la consola de Streamlit.

## 🔒 Seguridad

### Datos Sensibles
- Los datos personales se excluyen del historial clínico
- Las credenciales se almacenan en `secrets.toml`
- No se almacenan logs de conversaciones

### Privacidad
- Aviso de privacidad obligatorio
- Uso exclusivo para fines médicos
- Tratamiento confidencial y anónimo

## 🚀 Despliegue

### Streamlit Cloud
1. Conectar repositorio a Streamlit Cloud
2. Configurar secrets en la interfaz web
3. Desplegar automáticamente

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "chatbot_v2_gemini.py"]
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Changelog

### v2.0.0
- Integración con Gemini 2.5 Flash
- Preguntas complementarias dinámicas
- Resúmenes clínicos automáticos
- Mejoras en la interfaz de usuario

### v1.0.0
- Cuestionario médico básico
- Integración con Google Sheets
- Interfaz de Streamlit

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

**Diego Robles García**
- Proyecto: Chatbot Lina v2.0
- Especialización: Sistemas médicos con IA

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contactar a través de:
- Issues en GitHub
- Email: [diegoroblesgarcia347@gmail.com]

---

**⚠️ Aviso Legal**: Este software es para uso médico y científico únicamente. No reemplaza la consulta médica profesional.
