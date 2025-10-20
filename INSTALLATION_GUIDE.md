# 🚀 Guía de Instalación - Chatbot Lina v2.0

Esta guía te llevará paso a paso para configurar y ejecutar el Chatbot Lina en tu sistema.

## 📋 Prerrequisitos

### Software Requerido
- **Python 3.8+** (recomendado: Python 3.9 o 3.10)
- **Git** para clonar el repositorio
- **Navegador web** moderno (Chrome, Firefox, Safari, Edge)

### Cuentas Necesarias
- **Google Cloud Platform** (cuenta gratuita)
- **Google AI Studio** (para Gemini API)
- **Google Sheets** (cuenta de Google)

## 🔧 Instalación Paso a Paso

### Paso 1: Clonar el Repositorio

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Chatbotv2

# Verificar que estás en el directorio correcto
ls -la
```

Deberías ver:
```
chatbot_v2_gemini.py
connector_gemini.py
google_sheets_connector.py
preguntas/
requirements.txt
README.md
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Verificar que está activado (deberías ver (venv) al inicio)
which python
```

### Paso 3: Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

Deberías ver:
```
streamlit>=1.28.0
gspread>=5.11.0
google-auth>=2.23.0
pytz>=2023.3
google-genai>=1.0.0
```

### Paso 4: Configurar Google Gemini API

#### 4.1 Obtener API Key

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la API key generada

#### 4.2 Configurar la API Key

```bash
# Crear directorio de configuración
mkdir -p .streamlit

# Crear archivo de configuración
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edita el archivo `.streamlit/secrets.toml`:

```toml
[GEMINI_API_KEY]
api_key = "tu_api_key_real_aqui"
```

### Paso 5: Configurar Google Sheets

#### 5.1 Crear Proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Anota el **Project ID**

#### 5.2 Habilitar APIs

1. En el menú lateral, ve a "APIs & Services" > "Library"
2. Busca y habilita:
   - **Google Sheets API**
   - **Google Drive API**

#### 5.3 Crear Service Account

1. Ve a "APIs & Services" > "Credentials"
2. Haz clic en "Create Credentials" > "Service Account"
3. Completa:
   - **Name**: `chatbot-lina-service`
   - **Description**: `Service account for Chatbot Lina`
4. Haz clic en "Create and Continue"
5. En "Grant access", selecciona "Editor" y continúa
6. Haz clic en "Done"

#### 5.4 Generar Credenciales

1. En la lista de Service Accounts, haz clic en el que acabas de crear
2. Ve a la pestaña "Keys"
3. Haz clic en "Add Key" > "Create new key"
4. Selecciona "JSON" y haz clic en "Create"
5. Descarga el archivo JSON

#### 5.5 Convertir JSON a TOML

El archivo JSON descargado tiene esta estructura:
```json
{
  "type": "service_account",
  "project_id": "tu-proyecto-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "chatbot-lina-service@tu-proyecto.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

Convierte este JSON al formato TOML en `.streamlit/secrets.toml`:

```toml
[GEMINI_API_KEY]
api_key = "tu_api_key_de_gemini"

[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto-id"
private_key_id = "tu_private_key_id"
private_key = """-----BEGIN PRIVATE KEY-----
tu_private_key_completa
-----END PRIVATE KEY-----"""
client_email = "chatbot-lina-service@tu-proyecto.iam.gserviceaccount.com"
client_id = "tu_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/chatbot-lina-service%40tu-proyecto.iam.gserviceaccount.com"
```

#### 5.6 Crear Hoja de Google Sheets

1. Ve a [Google Sheets](https://sheets.google.com/)
2. Crea una nueva hoja de cálculo
3. Nómbrala **"Lina"** (exactamente así)
4. Comparte la hoja con el email de tu Service Account:
   - Email: `chatbot-lina-service@tu-proyecto.iam.gserviceaccount.com`
   - Permisos: **Editor**

### Paso 6: Verificar Configuración

#### 6.1 Probar Conexión a Gemini

```bash
# Crear script de prueba
cat > test_gemini.py << 'EOF'
import streamlit as st
from connector_gemini import GeminiConnector

try:
    connector = GeminiConnector()
    print("✅ Conexión a Gemini exitosa")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
EOF

python test_gemini.py
```

#### 6.2 Probar Conexión a Google Sheets

```bash
# Crear script de prueba
cat > test_sheets.py << 'EOF'
import streamlit as st
from google_sheets_connector import GoogleSheetsConnector

try:
    gsheets = GoogleSheetsConnector("Lina")
    print("✅ Conexión a Google Sheets exitosa")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
EOF

python test_sheets.py
```

### Paso 7: Ejecutar la Aplicación

```bash
# Ejecutar el chatbot
streamlit run chatbot_v2_gemini.py
```

Si todo está configurado correctamente, deberías ver:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## 🧪 Pruebas de Funcionamiento

### Prueba 1: Interfaz de Usuario
1. Abre http://localhost:8501 en tu navegador
2. Deberías ver el aviso de privacidad
3. Haz clic en "Continuar"

### Prueba 2: Cuestionario
1. Responde las primeras preguntas
2. Verifica que el botón "Regresar" funcione
3. Completa el cuestionario base

### Prueba 3: IA y Almacenamiento
1. Verifica que se genere el resumen clínico
2. Responde las preguntas complementarias
3. Verifica que los datos se guarden en Google Sheets

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Causa**: Streamlit no está instalado o el entorno virtual no está activado.

**Solución**:
```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Error: "Error al inicializar Gemini: Invalid API key"

**Causa**: API key incorrecta o no configurada.

**Solución**:
1. Verifica que el archivo `.streamlit/secrets.toml` existe
2. Verifica que la API key esté correctamente copiada
3. Asegúrate de que no haya espacios extra en la API key

### Error: "Error al guardar en Google Sheets: Access denied"

**Causa**: La Service Account no tiene permisos o la hoja no está compartida.

**Solución**:
1. Verifica que la hoja "Lina" existe
2. Comparte la hoja con el email de la Service Account
3. Verifica que las credenciales estén correctas

### Error: "No such file or directory: '.streamlit/secrets.toml'"

**Causa**: El archivo de configuración no existe.

**Solución**:
```bash
# Crear directorio y archivo
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Editar el archivo con tus credenciales
nano .streamlit/secrets.toml  # o tu editor preferido
```

### Error: "Port 8501 is already in use"

**Causa**: Otra instancia de Streamlit está ejecutándose.

**Solución**:
```bash
# Opción 1: Usar otro puerto
streamlit run chatbot_v2_gemini.py --server.port 8502

# Opción 2: Matar proceso existente
# En Windows:
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F

# En macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)

### Tutoriales Relacionados
- [Configurar Google Cloud Service Account](https://cloud.google.com/iam/docs/service-accounts)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

## 🆘 Soporte

Si encuentras problemas no cubiertos en esta guía:

1. Revisa los logs de error en la consola
2. Verifica que todas las dependencias estén instaladas
3. Confirma que las credenciales estén correctas
4. Consulta la documentación oficial de las APIs

---

**¡Felicitaciones!** 🎉 Si llegaste hasta aquí, tu Chatbot Lina debería estar funcionando correctamente.
