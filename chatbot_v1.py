# chatbot Lina basado en reglas
# archivo: chatbot.py
# autor: robles garcia diego
# descripcion: script con la aplicacion web del chatbot
# version : 1.0

from datetime import datetime
import pytz
import streamlit as st
import streamlit.components.v1 as components
import preguntas.Preguntas as prg
from google_sheets_connector_1 import GoogleSheetsConnector
from connector_mistral import GenerarResumen
from connector_falcon import GenerarPregunta

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


#metrica rouges        
        
# ------------ FUNCION para obtener el resumen ------------ #
#cambiar hacia asyc      
def resumen():
    st.session_state.resumen_listo = False
    conector = GenerarResumen(st.session_state.historial)
    resultado = conector.obtener_resumen()  # puede tardar
    st.session_state.resumen_texto = resultado
    st.session_state.resumen_listo = True
    #st.experimental_rerun()



# ------------ FUNCIONE para guardar el historial ------------ #
def historial(pregunta, respuesta):
    campos_excluidos = {
        "nombre_completo",
        "fecha_nacimiento", 
        "domicilio",
        "telefono",
        "contacto_emergencia"
    }
    
    clave = pregunta.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
    
    if clave not in campos_excluidos:
        st.session_state.historial += f"\nDoctor: {pregunta.get('texto', f'pregunta_{st.session_state.pregunta_actual}')}"
        st.session_state.historial += f"\nPaciente: {respuesta}"
        
# ------------ FUNCION PARA INICIAR VARIABLES COMPLEMENTARIAS ------------ #        
def iniciar_preguntas_complementarias():
    st.session_state.complementarias_activas = True
    st.session_state.contador_complementarias = 0
    st.session_state.respuestas_complementarias = []
    generar_pregunta_complementaria()
        
# ------------ FUNCION PARA GENERAR PREGUNTAS COMPLEMENTARIAS ------------ #        
def generar_pregunta_complementaria():
    if not st.session_state.resumen_listo:
        agregar_mensaje_bot("⌛ Esperando a que se genere el resumen clínico antes de continuar...")
        return

    respuestas_totales = {
        **st.session_state.respuestas,
        **{f"extra_{i+1}": r for i, r in enumerate(st.session_state.respuestas_complementarias)}
    }

    temp = st.session_state.historial
    contexto = temp.splitlines()[-6:]
    

    generador = GenerarPregunta(resumen=st.session_state.resumen_texto,ultimas_preguntas=contexto)
    nueva_pregunta = generador.obtener_nueva_pregunta()
    
    st.session_state.pregunta_complementaria_actual = nueva_pregunta
    agregar_mensaje_bot(nueva_pregunta)



# ------------ FUNCIONES DE MENSAJES ------------ #
def agregar_mensaje_bot(mensaje) -> None:
    st.session_state.messages.append({"role": "bot", "content": mensaje})

def agregar_mensaje_usuario(mensaje) -> None:
    st.session_state.messages.append({"role": "user", "content": mensaje})
   
#def actualizar_encabezados(sheet, claves):
#    hoja = sheet.sheet
#    encabezados_actuales = hoja.row_values(1)
#    if set(claves) != set(encabezados_actuales):
#        hoja.update('A1', [claves]) 
#"""

# ------------ PROCESAR RESPUESTA ------------ #
def procesar_respuesta(respuesta) -> None:
    if not st.session_state.cuestionario_terminado:
        pregunta_actual = st.session_state.preguntas[st.session_state.pregunta_actual]
        clave = pregunta_actual.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
        
        #print(pregunta_actual)
        #print(respuesta.strip().lower())
        
        historial(pregunta_actual,respuesta.strip().lower())

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
        if clave == "hambre_excesiva":
            ##resumen()
            pass

        st.session_state.pregunta_actual += 1

        if st.session_state.pregunta_actual >= len(st.session_state.preguntas):
            st.session_state.cuestionario_terminado = True
            print(f"Respuestas recogidas:", st.session_state.respuestas)
            agregar_mensaje_bot("¡Perfecto! He terminado de recopilar tu información basica, ahora apoyame contestando las siguientes preguntas para complementar mi informacion sobre ti.")
            gsheets = GoogleSheetsConnector("credentials/credenciales.json", "Lina")
            try:
                gsheets.guardar_fila(st.session_state.respuestas)
            except Exception as e:
                st.error(f"❌ Error al guardar en Google Sheets: {e}")

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
            # Guardar en historial también
            pregunta = {"texto": st.session_state.pregunta_complementaria_actual}
            historial(pregunta, texto.strip().lower())
            # Guardar respuesta y generar la siguiente
            st.session_state.respuestas_complementarias.append(texto.strip().lower())
            st.session_state.contador_complementarias += 1

            if st.session_state.contador_complementarias < 5:
                generar_pregunta_complementaria()
            else:
                st.session_state.complementarias_activas = False
                agregar_mensaje_bot("Gracias. He terminado también con las preguntas complementarias.")
        
        else:
            if "gracias" in texto.lower():
                agregar_mensaje_bot("¡De nada! Fue un placer ayudarte. Que tengas un excelente día.")


def recarga()->None:
    st.rerun()


# ------------ PAGINA CONFIGURACION ------------ #
st.set_page_config(page_title="Chatbot Lina", page_icon="🤖")
init_session()

if not st.session_state.aviso_aceptado:
    st.markdown("""
        ### 🧬 Proyecto de Investigación - Aviso de Privacidad

        Esta herramienta forma parte de un estudio de investigación académica.  
        Todos los datos proporcionados serán utilizados exclusivamente con fines médicos y científicos,  
        y serán tratados bajo estricta confidencialidad y anonimato.

        Tu participación en este cuestionario es completamente voluntaria y representa una valiosa contribución para esta investigación.  
        Al continuar, aceptas formar parte del estudio de manera libre y consciente.  
        **¡Gracias por tu apoyo!**
        """)



    if st.button("✅ Continuar"):
        st.session_state.aviso_aceptado = True
        st.rerun()
    st.text("⬆️ Presione el boton para continuar")

# Si ya aceptó, mostrar el chatbot
else:
    st.title("Chatbot Lina 🤖")
    st.write    ("Todos los datos seran usados con fines medicos")

    if not st.session_state.bot_iniciado:
        agregar_mensaje_bot(f"Hola {saludo()}, mi nombre es Lina, soy tu asistente virtual.")
        agregar_mensaje_bot("Te voy a realizar un cuestionario de rutina para generar tu expediente.")

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
                    
    # ------------ BOTÓN REGRESAR ------------ #
    button_regresar = st.button("⏪ Regresar",type="primary")
    if st.session_state.pregunta_actual > 0 and not st.session_state.cuestionario_terminado:
        if button_regresar:
            st.session_state.pregunta_actual -= 1
            pregunta_anterior = st.session_state.preguntas[st.session_state.pregunta_actual]
            clave_anterior = pregunta_anterior.get("clave", f"pregunta_{st.session_state.pregunta_actual}")
            
            # Elimina la respuesta anterior si existe
            if clave_anterior in st.session_state.respuestas:
                del st.session_state.respuestas[clave_anterior]
            
            # Mostrar de nuevo la pregunta anterior
            agregar_mensaje_bot(f"(Editando respuesta anterior)")
            agregar_mensaje_bot(pregunta_anterior["texto"])
            recarga()
            
    st.write("¿Cometiste un error? Usa el botón **Regresar** para corregir tu respuesta.")
    # ------------ ENTRADA DE TEXTO ------------ #
    container_txt = st.container(height=80,border=False)
    prompt = container_txt.chat_input()
    if prompt:
        enviar_callback(respuesta=prompt)
        recarga()


   

