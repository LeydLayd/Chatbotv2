# archivo: connector_gemini.py
# autor: robles garcia diego
# descripcion: Conector unificado para Gemini 2.5 Flash
# version: 2.0

from google import genai
from typing import Optional
import streamlit as st
import time

class GeminiConnector:
    """
    Conector unificado para interactuar con Gemini 1.5 Flash.
    Maneja tanto generación de resúmenes como preguntas complementarias.
    """
    
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.5-flash"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents="Hola Gemini"
            )
            print(response.text)
        except Exception as e:
            raise Exception(f"Error al inicializar Gemini: {e}")

    def _llamar_con_reintentos(self, prompt: str, max_reintentos: int = 3) -> Optional[str]:
        for intento in range(max_reintentos):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                else:
                    print(f"Advertencia: Respuesta vacía en intento {intento + 1}")
            except Exception as e:
                print(f"Error en intento {intento + 1}/{max_reintentos}: {e}")
                if intento < max_reintentos - 1:
                    time.sleep(2 ** intento)
        return None

    
    def generar_resumen(self, historial: str) -> Optional[str]:
        """
        Genera un resumen clínico conciso del historial médico.
        
        Args:
            historial: Conversación completa doctor-paciente
            
        Returns:
            Resumen clínico en formato profesional
        """
        prompt = f"""Eres un médico especialista en diabetes. Analiza la siguiente conversación y genera un resumen clínico profesional.

**INSTRUCCIONES:**
- Máximo 100 palabras
- Estructura: Antecedentes → Síntomas actuales → Factores de riesgo
- Usa terminología médica apropiada
- Sé conciso y objetivo
- No repitas información

**CONVERSACIÓN:**
{historial}

**RESUMEN CLÍNICO:**"""
        print(prompt)
        
        return self._llamar_con_reintentos(prompt)
    
    def generar_pregunta_complementaria(
        self, 
        resumen: str, 
        ultimas_preguntas: list,
        numero_pregunta: int
    ) -> Optional[str]:
        """
        Genera una pregunta médica complementaria basada en el contexto.
        
        Args:
            resumen: Resumen clínico del paciente
            ultimas_preguntas: Lista de las últimas 3 preguntas/respuestas
            numero_pregunta: Número de pregunta complementaria (1-5)
            
        Returns:
            Pregunta médica relevante y específica
        """
        
        # Unir las últimas preguntas en formato legible
        contexto_reciente = "\n".join(ultimas_preguntas) if ultimas_preguntas else "Sin contexto previo"
        
        prompt = f"""Eres un médico entrevistando a un paciente con posible riesgo de diabetes.

**CONTEXTO DEL PACIENTE:**
{resumen}

**ÚLTIMAS INTERACCIONES:**
{contexto_reciente}

**TU TAREA:**
Genera la pregunta complementaria #{numero_pregunta} de 5. Esta pregunta debe:
- Profundizar en aspectos no cubiertos aún
- Ser específica y clara
- Ayudar a completar el diagnóstico
- Evitar repetir información ya obtenida
- Ser una pregunta corta (máximo 20 palabras)

**ÁREAS A EXPLORAR:**
- Síntomas específicos no mencionados
- Calidad de sueño y estrés
- Detalles de alimentación
- Historial de peso
- Síntomas neurológicos o visuales

**PREGUNTA:**"""

        return self._llamar_con_reintentos(prompt)
    
    def validar_respuesta(self, pregunta: str, respuesta: str) -> tuple[bool, str]:
        """
        Valida si una respuesta del paciente es apropiada para la pregunta médica.
        
        Args:
            pregunta: La pregunta realizada
            respuesta: La respuesta del paciente
            
        Returns:
            (es_valida, mensaje_feedback)
        """
        prompt = f"""Eres un asistente médico validando respuestas de pacientes.

**PREGUNTA:** {pregunta}
**RESPUESTA DEL PACIENTE:** {respuesta}

**TAREA:** Determina si la respuesta es válida y útil médicamente.

Responde SOLO con uno de estos formatos:
- "VÁLIDA: [respuesta es apropiada]"
- "INVÁLIDA: [explicación breve de por qué y cómo debería responder]"

**EVALUACIÓN:**"""

        resultado = self._llamar_con_reintentos(prompt)
        
        if resultado:
            if resultado.startswith("VÁLIDA"):
                return True, "✅ Respuesta registrada"
            else:
                return False, resultado.replace("INVÁLIDA:", "").strip()
        
        return True, "✅ Respuesta registrada"  # Default: aceptar si falla la validación


# ============================================
# CLASES DE COMPATIBILIDAD (para mantener código existente)
# ============================================

class GenerarResumen:
    """Wrapper de compatibilidad para código existente"""
    
    def __init__(self, historial: str, url: str = None):
        self.historial = historial
        self.connector = GeminiConnector()
    
    def obtener_resumen(self) -> Optional[str]:
        return self.connector.generar_resumen(self.historial)


class GenerarPregunta:
    """Wrapper de compatibilidad para código existente"""
    
    def __init__(self, resumen: str, ultimas_preguntas: list, url: str = None):
        self.resumen = resumen
        self.ultimas_preguntas = ultimas_preguntas
        self.connector = GeminiConnector()
        self.numero_pregunta = 1
    
    def obtener_nueva_pregunta(self) -> Optional[str]:
        pregunta = self.connector.generar_pregunta_complementaria(
            self.resumen,
            self.ultimas_preguntas,
            self.numero_pregunta
        )
        self.numero_pregunta += 1
        return pregunta


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def inicializar_gemini_en_session():
    """
    Inicializa el conector de Gemini en la sesión de Streamlit.
    Llama esto una vez al inicio de tu aplicación.
    """
    if "gemini_connector" not in st.session_state:
        try:
            st.session_state.gemini_connector = GeminiConnector()
            return True
        except Exception as e:
            st.error(f"❌ Error al inicializar Gemini: {e}")
            return False
    return True


def obtener_conector() -> Optional[GeminiConnector]:
    """
    Obtiene el conector de Gemini desde la sesión.
    
    Returns:
        GeminiConnector o None si no está inicializado
    """
    return st.session_state.get("gemini_connector", None)