import requests
from typing import Optional

class GenerarPregunta:
    def __init__(self, resumen: str,ultimas_preguntas, url: str = "https://eac9168d3420.ngrok-free.app/generate"):
        self.url = url
        self.resumen = resumen
        self.ultimas_preguntas = ultimas_preguntas
        
    def obtener_nueva_pregunta(self) -> Optional[str]:
        prompt = f"""
        Eres un médico entrevistando a un paciente.Aqui esta un resumen de la conversacion que tuviste:
        {self.resumen}
        Estas son las ultimas 3 preguntas/repuestas de la conversacion:
        {self.ultimas_preguntas}
        Basado en el resumen y las ultimas 3 preguntas del diálogo, genera la próxima pregunta médica relevante.
        """
        
        try:
            response = requests.post(
                self.url, 
                json={"prompt": prompt},
                #timeout=30  # Timeout de 30 segundos
            )
            
            # Verificar que la respuesta sea exitosa
            response.raise_for_status()
            
            # Extraer el contenido del resumen
            data = response.json()
            return data.get('response', data.get('text', ''))
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servicio: {e}")
            return None
        except ValueError as e:
            print(f"Error al procesar la respuesta JSON: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None