# 📝 Changelog - Chatbot Lina

Todas las notables cambios a este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-XX

### ✨ Añadido
- Integración completa con Google Gemini 2.5 Flash
- Sistema de preguntas complementarias dinámicas generadas por IA
- Generación automática de resúmenes clínicos profesionales
- Validación inteligente de respuestas médicas
- Sistema robusto de reintentos para APIs externas
- Mejoras significativas en la interfaz de usuario
- Indicadores visuales de progreso mejorados
- Sidebar con resumen clínico visible
- Sistema de logging mejorado
- Documentación completa del proyecto

### 🔄 Cambiado
- Migración de sistema de preguntas estáticas a dinámicas
- Refactorización completa del conector de IA
- Mejora en el manejo de errores y excepciones
- Optimización del flujo de trabajo del cuestionario
- Actualización de dependencias a versiones más recientes

### 🐛 Corregido
- Problemas de sincronización con Google Sheets
- Errores en el manejo de preguntas condicionales
- Mejoras en la estabilidad de la sesión de Streamlit
- Corrección de bugs en el sistema de regreso de preguntas

### 🔒 Seguridad
- Mejoras en el manejo de datos sensibles
- Exclusión automática de datos personales del historial clínico
- Validación mejorada de credenciales de API

### 📚 Documentación
- README.md completo con guías de instalación
- Documentación de arquitectura del sistema
- Guía paso a paso de instalación
- Ejemplos de configuración
- API Reference detallada

## [1.0.0] - 2023-XX-XX

### ✨ Añadido
- Sistema básico de cuestionario médico
- Integración inicial con Google Sheets
- Interfaz de usuario con Streamlit
- Preguntas estructuradas para evaluación de diabetes
- Sistema de preguntas condicionales básico
- Almacenamiento automático de respuestas
- Aviso de privacidad y consentimiento
- Sistema de navegación entre preguntas

### 🏗️ Arquitectura Inicial
- Estructura modular del proyecto
- Separación de responsabilidades por archivos
- Sistema de gestión de sesión básico
- Conectores para servicios externos

---

## Tipos de Cambios

- **✨ Añadido** - Para nuevas funcionalidades
- **🔄 Cambiado** - Para cambios en funcionalidades existentes
- **🐛 Corregido** - Para correcciones de bugs
- **🔒 Seguridad** - Para mejoras de seguridad
- **📚 Documentación** - Para cambios en documentación
- **🏗️ Arquitectura** - Para cambios estructurales
- **⚡ Rendimiento** - Para mejoras de rendimiento
- **🧪 Testing** - Para cambios en pruebas
- **🔧 Configuración** - Para cambios de configuración

## Convenciones de Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Cambios incompatibles en la API
- **MINOR** (0.X.0): Funcionalidades nuevas compatibles hacia atrás
- **PATCH** (0.0.X): Correcciones de bugs compatibles hacia atrás

## Notas de Versión

### v2.0.0 - "Inteligencia Artificial"
Esta versión representa un salto significativo en las capacidades del chatbot, introduciendo inteligencia artificial para generar preguntas personalizadas y resúmenes clínicos automáticos. Es una actualización mayor que mejora sustancialmente la experiencia del usuario y la calidad de los datos recopilados.

### v1.0.0 - "Fundación"
La versión inicial estableció las bases del sistema con un cuestionario médico estructurado y funcional, sentando las bases para futuras mejoras con IA.

## Roadmap Futuro

### v2.1.0 - "Mejoras de UX"
- [ ] Interfaz de usuario más intuitiva
- [ ] Mejores indicadores de progreso
- [ ] Soporte para múltiples idiomas
- [ ] Temas personalizables

### v2.2.0 - "Analytics"
- [ ] Dashboard de administración
- [ ] Estadísticas de uso
- [ ] Reportes automáticos
- [ ] Métricas de calidad

### v3.0.0 - "Integración Avanzada"
- [ ] Integración con sistemas de salud
- [ ] Soporte para múltiples especialidades médicas
- [ ] API REST para integraciones externas
- [ ] Sistema de notificaciones

## Contribuciones

Para contribuir al proyecto, por favor:

1. Revisa las [guías de contribución](CONTRIBUTING.md)
2. Sigue las convenciones de código establecidas
3. Actualiza este changelog con tus cambios
4. Incluye tests para nuevas funcionalidades

## Contacto

Para preguntas sobre versiones o cambios:
- **Autor**: Diego Robles García
- **Proyecto**: Chatbot Lina v2.0
- **Especialización**: Sistemas médicos con IA
