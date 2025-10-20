import requests
from typing import Optional

class GenerarResumen:
    def __init__(self, historial: str, url: str = "https://61f42bdaa85b.ngrok-free.app//generate"):
        self.url = url
        self.historial = historial
        
    def obtener_resumen(self) -> Optional[str]:
        prompt = f"""
        A partir de la siguiente conversación médico-paciente, genera un resumen clínico en un párrafo claro, estructurado y profesional, mencionando antecedentes médicos, síntomas actuales y factores de riesgo, lo más corto posible, no más de 100 palabras.
        
        Conversación:
        {self.historial}
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