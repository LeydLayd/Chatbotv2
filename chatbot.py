# chatbot Lina basado en reglas
# archivo: chatbot.py
# autor: robles garcia diego
# descripcion: script con la aplicacion web del chatbot
# version : 1.1

from datetime import datetime
import pytz
import streamlit as st
import streamlit.components.v1 as components
import preguntas.Preguntas as prg
from google_sheets_connector import GoogleSheetsConnector

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

# ------------ INICIALIZACIÓN DE SESION ------------ #
def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

        st.session_state.respuestas[clave] = respuesta.strip().lower()

        # Insertar preguntas condicionales si aplica
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

        if st.session_state.pregunta_actual >= len(st.session_state.preguntas):
            st.session_state.cuestionario_terminado = True
            agregar_mensaje_bot("¡Perfecto! He terminado de recopilar tu información. Tu expediente ha sido guardado exitosamente.")
            gsheets = GoogleSheetsConnector("Lina")
            try:
                gsheets.guardar_fila(st.session_state.respuestas)
            except Exception as e:
                st.error(f"❌ Error al guardar en Google Sheets: {e}")
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
        else:
            if "gracias" in texto.lower():
                agregar_mensaje_bot("¡De nada! Fue un placer ayudarte. Que tengas un excelente día.")

        st.session_state.input_text = ""  

# ------------ PAGINA CONFIGURACION ------------ #
st.set_page_config(page_title="Chatbot Lina", page_icon="🤖")
init_session()

st.title("Chatbot Lina 🤖")

if not st.session_state.bot_iniciado:
    agregar_mensaje_bot(f"Hola {saludo()}, mi nombre es Lina, soy tu asistente virtual.")
    agregar_mensaje_bot("Te voy a realizar un cuestionario de rutina para generar tu expediente.")

    if st.session_state.preguntas:
        primera_pregunta = st.session_state.preguntas[0]
        agregar_mensaje_bot(primera_pregunta["texto"])

    st.session_state.bot_iniciado = True

# ------------ CONTENEDOR DE CHAT CON SCROLL AUTOMÁTICO ------------ #
chat_container = st.container(height=500)

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "bot":
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])


# ------------ ENTRADA DE TEXTO ------------ #
container_txt = st.container(height=80,border=False)
prompt = container_txt.chat_input()
if prompt:
    enviar_callback(respuesta=prompt)
    st.rerun()
