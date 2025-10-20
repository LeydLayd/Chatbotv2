# chatbot Lina basado en reglas + IA (Gemini)
# archivo: chatbot_v2_gemini.py
# autor: robles garcia diego
# descripcion: Chatbot médico con Gemini 1.5 Flash
# version: 2.0

from datetime import datetime
import pytz
import streamlit as st
import preguntas.Preguntas as prg
from google_sheets_connector import GoogleSheetsConnector
from connector_gemini import GeminiConnector

# ------------ FUNCIONES AUXILIARES ------------ #
def saludo() -> str:
    mexico_tz = pytz.timezone('America/Mexico_City')
    now_mexico = datetime.now(mexico_tz)
    hora_actual_mexico = int(now_mexico.strftime("%H"))

    if 6 <= hora_actual_mexico < 12:
        return "Buenos días"
    elif 12 <= hora_actual_mexico < 18:
        return "Buenas tardes"
    else:
        return "Buenas noches"

# ------------ INICIALIZACIÓN DE SESIÓN ------------ #
def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "aviso_aceptado" not in st.session_state:
        st.session_state.aviso_aceptado = False
        
    if "historial" not in st.session_state:
        st.session_state.historial = ""
    
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}

    if "bot_iniciado" not in st.session_state:
        st.session_state.bot_iniciado = False

    if "cuestionario_terminado" not in st.session_state:
        st.session_state.cuestionario_terminado = False

    if "pregunta_actual" not in st.session_state:
        st.session_state.pregunta_actual = 0

    if "preguntas" not in st.session_state:
        Preguntas_totales = []
        Preguntas_totales += prg.preguntas_personales
        Preguntas_totales += prg.pregunta_prediagnostico
        Preguntas_totales += prg.preguntas_antecedentes
        Preguntas_totales += prg.fumar
        Preguntas_totales += prg.alcohol
        Preguntas_totales += prg.actividad
        Preguntas_totales += prg.glucosa
        Preguntas_totales += prg.alimenticio
        st.session_state.preguntas = Preguntas_totales
        
    if "complementarias_activas" not in st.session_state:
        st.session_state.complementarias_activas = False

    if "contador_complementarias" not in st.session_state:
        st.session_state.contador_complementarias = 0

    if "respuestas_complementarias" not in st.session_state:
        st.session_state.respuestas_complementarias = []

    if "pregunta_complementaria_actual" not in st.session_state:
        st.session_state.pregunta_complementaria_actual = ""
        
    if "resumen_listo" not in st.session_state:
        st.session_state.resumen_listo = False

    if "resumen_texto" not in st.session_state:
        st.session_state.resumen_texto = ""
        
    # Inicializar conector de Gemini
    if "gemini_connector" not in st.session_state:
        try:
            st.session_state.gemini_connector = GeminiConnector()
        except Exception as e:
            st.error(f"❌ Error al inicializar Gemini: {e}")
            st.stop()

# ------------ FUNCIÓN PARA GENERAR RESUMEN ------------ #
def generar_resumen():
    """Genera resumen clínico usando Gemini"""
    if not st.session_state.historial:
        return
    
    with st.spinner("🤖 Generando resumen clínico con IA..."):
        try:
            connector = st.session_state.gemini_connector
            resumen = connector.generar_resumen(st.session_state.historial)
            
            if resumen:
                st.session_state.resumen_texto = resumen
                st.session_state.resumen_listo = True
            else:
                st.error("⚠️ No se pudo generar el resumen. Continuando sin él.")
                st.session_state.resumen_texto = "Resumen no disponible"
                st.session_state.resumen_listo = True
                
        except Exception as e:
            st.error(f"❌ Error al generar resumen: {e}")
            st.session_state.resumen_texto = "Error al generar resumen"
            st.session_state.resumen_listo = True

# ------------ FUNCIÓN PARA GUARDAR HISTORIAL ------------ #
def historial(pregunta, respuesta):
    """Guarda la conversación en el historial (excluyendo datos personales)"""
    campos_excluidos = {
        "nombre_completo", "fecha_nacimiento", "domicilio",
        "telefono", "contacto_emergencia"
    }
    
    clave = pregunta.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
    
    if clave not in campos_excluidos:
        st.session_state.historial += f"\nDoctor: {pregunta.get('texto', '')}"
        st.session_state.historial += f"\nPaciente: {respuesta}"

# ------------ INICIAR PREGUNTAS COMPLEMENTARIAS ------------ #        
def iniciar_preguntas_complementarias():
    """Inicia el flujo de preguntas complementarias con IA"""
    # Primero generar el resumen
    generar_resumen()
    
    st.session_state.complementarias_activas = True
    st.session_state.contador_complementarias = 0
    st.session_state.respuestas_complementarias = []
    
    # Generar primera pregunta complementaria
    generar_pregunta_complementaria()

# ------------ GENERAR PREGUNTA COMPLEMENTARIA ------------ #        
def generar_pregunta_complementaria():
    """Genera una pregunta complementaria usando Gemini"""
    if not st.session_state.resumen_listo:
        agregar_mensaje_bot("⌛ Esperando resumen clínico...")
        return

    with st.spinner("🤖 Generando pregunta complementaria..."):
        try:
            # Obtener contexto reciente
            temp = st.session_state.historial
            contexto = temp.splitlines()[-6:] if temp else []
            
            connector = st.session_state.gemini_connector
            nueva_pregunta = connector.generar_pregunta_complementaria(
                resumen=st.session_state.resumen_texto,
                ultimas_preguntas=contexto,
                numero_pregunta=st.session_state.contador_complementarias + 1
            )
            
            if nueva_pregunta:
                st.session_state.pregunta_complementaria_actual = nueva_pregunta
                agregar_mensaje_bot(nueva_pregunta)
            else:
                # Si falla, terminar preguntas complementarias
                st.session_state.complementarias_activas = False
                agregar_mensaje_bot("He terminado con las preguntas complementarias.")
                
        except Exception as e:
            st.error(f"❌ Error al generar pregunta: {e}")
            st.session_state.complementarias_activas = False

# ------------ FUNCIONES DE MENSAJES ------------ #
def agregar_mensaje_bot(mensaje) -> None:
    st.session_state.messages.append({"role": "bot", "content": mensaje})

def agregar_mensaje_usuario(mensaje) -> None:
    st.session_state.messages.append({"role": "user", "content": mensaje})

# ------------ PROCESAR RESPUESTA ------------ #
def procesar_respuesta(respuesta) -> None:
    if not st.session_state.cuestionario_terminado:
        pregunta_actual = st.session_state.preguntas[st.session_state.pregunta_actual]
        clave = pregunta_actual.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
        
        # Guardar en historial
        historial(pregunta_actual, respuesta.strip().lower())
        st.session_state.respuestas[clave] = respuesta.strip().lower()

        # Insertar preguntas condicionales
        if "condicional" in pregunta_actual:
            respuesta_key = respuesta.strip().lower()
            preguntas_extra = pregunta_actual["condicional"].get(respuesta_key)
            if preguntas_extra:
                index = st.session_state.pregunta_actual + 1
                st.session_state.preguntas = (
                    st.session_state.preguntas[:index]
                    + preguntas_extra
                    + st.session_state.preguntas[index:]
                )

        st.session_state.pregunta_actual += 1

        # Verificar si terminó el cuestionario base
        if st.session_state.pregunta_actual >= len(st.session_state.preguntas):
            st.session_state.cuestionario_terminado = True
            agregar_mensaje_bot("¡Perfecto! He terminado de recopilar tu información básica.")
            agregar_mensaje_bot("Ahora te haré algunas preguntas complementarias para completar tu expediente. 🔍")
            
            # Guardar en Google Sheets
            gsheets = GoogleSheetsConnector("Lina")
            try:
                gsheets.guardar_fila(st.session_state.respuestas)
            except Exception as e:
                st.error(f"❌ Error al guardar en Google Sheets: {e}")

            # Iniciar preguntas complementarias
            iniciar_preguntas_complementarias()
        else:
            siguiente_pregunta = st.session_state.preguntas[st.session_state.pregunta_actual]
            agregar_mensaje_bot(siguiente_pregunta["texto"])

# ------------ CALLBACK PARA ENVIAR ------------ #
def enviar_callback(respuesta):
    texto = respuesta
    if texto:
        agregar_mensaje_usuario(texto)

        if not st.session_state.cuestionario_terminado:
            procesar_respuesta(texto)

        elif st.session_state.complementarias_activas:
            # Guardar respuesta complementaria
            pregunta = {"texto": st.session_state.pregunta_complementaria_actual}
            historial(pregunta, texto.strip().lower())
            st.session_state.respuestas_complementarias.append(texto.strip().lower())
            st.session_state.contador_complementarias += 1

            # Verificar si ya completó las 5 preguntas
            if st.session_state.contador_complementarias < 5:
                generar_pregunta_complementaria()
            else:
                st.session_state.complementarias_activas = False
                agregar_mensaje_bot("✅ ¡Excelente! He terminado de recopilar toda la información.")
                agregar_mensaje_bot("Tu expediente completo ha sido guardado. Gracias por tu colaboración. 🙏")
        else:
            if "gracias" in texto.lower():
                agregar_mensaje_bot("¡De nada! Fue un placer ayudarte. Que tengas un excelente día. 😊")

def recarga() -> None:
    st.rerun()

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Chatbot Lina con IA",
    page_icon="🤖",
    layout="centered"
)

init_session()

# ------------ AVISO DE PRIVACIDAD ------------ #
if not st.session_state.aviso_aceptado:
    st.markdown("""
        ### 🧬 Proyecto de Investigación - Aviso de Privacidad

        Esta herramienta forma parte de un estudio de investigación académica.  
        Todos los datos proporcionados serán utilizados exclusivamente con fines médicos y científicos,  
        y serán tratados bajo estricta confidencialidad y anonimato.

        **🤖 Esta versión utiliza Inteligencia Artificial (Gemini 1.5 Flash) para:**
        - Generar resúmenes clínicos automáticos
        - Formular preguntas complementarias personalizadas

        Tu participación en este cuestionario es completamente voluntaria y representa una valiosa contribución para esta investigación.  
        Al continuar, aceptas formar parte del estudio de manera libre y consciente.  
        **¡Gracias por tu apoyo!**
        """)

    if st.button("✅ Continuar"):
        st.session_state.aviso_aceptado = True
        st.rerun()
    st.text("⬆️ Presiona el botón para continuar")

# ------------ INTERFAZ DEL CHATBOT ------------ #
else:
    st.title("🤖 Chatbot Lina (v2.0 con IA)")
    st.caption("💡 Potenciado por Gemini 1.5 Flash")

    if not st.session_state.bot_iniciado:
        agregar_mensaje_bot(f"Hola {saludo()}, mi nombre es Lina, soy tu asistente virtual. 👋")
        agregar_mensaje_bot("Te voy a realizar un cuestionario de rutina para generar tu expediente médico.")

        if st.session_state.preguntas:
            primera_pregunta = st.session_state.preguntas[0]
            agregar_mensaje_bot(primera_pregunta["texto"])

        st.session_state.bot_iniciado = True

    # ------------ CONTENEDOR DE CHAT ------------ #
    chat_container = st.container(height=450)

    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "bot":
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.write(message["content"])

    # ------------ CONTROLES ------------ #
    col1, col2 = st.columns([1, 4])
    
    with col1:
        button_regresar = st.button("⏪ Regresar", type="primary")
        
    if st.session_state.pregunta_actual > 0 and not st.session_state.cuestionario_terminado:
        if button_regresar:
            st.session_state.pregunta_actual -= 1
            pregunta_anterior = st.session_state.preguntas[st.session_state.pregunta_actual]
            clave_anterior = pregunta_anterior.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
            
            if clave_anterior in st.session_state.respuestas:
                del st.session_state.respuestas[clave_anterior]
            
            agregar_mensaje_bot("(Editando respuesta anterior)")
            agregar_mensaje_bot(pregunta_anterior["texto"])
            recarga()
    
    with col2:
        st.caption("¿Cometiste un error? Usa el botón **Regresar** para corregir.")

    # ------------ ENTRADA DE TEXTO ------------ #
    container_txt = st.container(height=80, border=False)
    prompt = container_txt.chat_input("Escribe tu respuesta aquí...")
    
    if prompt:
        enviar_callback(respuesta=prompt)
        recarga()

    # ------------ INDICADORES DE ESTADO ------------ #
    if st.session_state.cuestionario_terminado:
        st.sidebar.success("✅ Cuestionario base completado")
        
        if st.session_state.resumen_listo:
            with st.sidebar.expander("📄 Ver Resumen Clínico"):
                st.write(st.session_state.resumen_texto)
        
        if st.session_state.complementarias_activas:
            st.sidebar.info(f"🔍 Pregunta complementaria {st.session_state.contador_complementarias + 1}/5")