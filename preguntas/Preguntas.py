# archivo: Preguntas.py
# autor: robles garcia diego
# descripcion: diccionarios de preguntas
# version : 1.0

# Preguntas personales
preguntas_personales = [
    {"texto": "¿Cuál es tu nombre completo?", "clave": "nombre_completo"},
    {"texto": "¿Cuál es tu edad?", "clave": "edad"},
    {"texto": "¿Cuál es tu sexo?", "clave": "sexo"},
    {"texto": "¿Cuál es tu fecha de nacimiento (dd/mm/aaaa)?", "clave": "fecha_nacimiento"},
    {"texto": "¿Cuál es tu CURP?", "clave": "curp"},
    {"texto": "¿Cuál es tu domicilio?", "clave": "domicilio"},
    {"texto": "¿Cuál es tu número de teléfono?", "clave": "telefono"},
    {"texto": "¿Cuál es tu ocupación?", "clave": "ocupacion"},
    {"texto": "¿Cuál es tu estado civil?", "clave": "estado_civil"},
    {"texto": "¿Quién es tu contacto de emergencia y cuál es su teléfono?", "clave": "contacto_emergencia"},
]

# Prediagnóstico de diabetes con condicional
pregunta_prediagnostico = [
    {
        "texto": "¿Ha sido diagnosticado previamente con diabetes?",
        "clave": "diagnosticado_diabetes",
        "condicional": {
            "sí": [
                {"texto": "¿Desde cuándo fue diagnosticado?", "clave": "fecha_diagnostico"},
                {"texto": "¿Está tomando algún medicamento actualmente?", "clave": "medicamento_actual"}
            ],
            "si": [
                {"texto": "¿Desde cuándo fue diagnosticado?", "clave": "fecha_diagnostico"},
                {"texto": "¿Está tomando algún medicamento actualmente?", "clave": "medicamento_actual"}
            ]
        }
    }
]

# Antecedentes
preguntas_antecedentes = [
    {"texto": "¿Tiene antecedentes de hipertensión?", "clave": "hipertension"},
    {"texto": "¿Tiene antecedentes de colesterol/triglicéridos altos?", "clave": "colesterol"},
    {"texto": "¿Tiene antecedentes de enfermedades cardíacas?", "clave": "cardiaco"},
    {"texto": "¿Tiene antecedentes de enfermedad renal?", "clave": "renal"},
    {"texto": "¿Tiene antecedentes de problemas de la visión?", "clave": "vision"},
    {"texto": "¿Tiene antecedentes de problemas en la piel (heridas que no sanan)?", "clave": "piel"},
    {"texto": "¿Tiene antecedentes de neuropatías (hormigueo, adormecimiento)?", "clave": "neuropatias"},
    {"texto": "¿Ha tenido hospitalizaciones previas? (Fechas y motivo)", "clave": "hospitalizaciones"},
    {"texto": "¿Alguien en su familia padece o ha padecido diabetes?", "clave": "fam_diabetes"},
    {"texto": "¿Alguien en su familia padece o ha padecido hipertensión?", "clave": "fam_hipertension"},
    {"texto": "¿Alguien en su familia padece o ha padecido enfermedades cardiovasculares?", "clave": "fam_cardiaco"},
    {"texto": "¿Alguien en su familia padece o ha padecido enfermedades renales?", "clave": "fam_renal"},
    {"texto": "¿Alguien en su familia padece o ha padecido obesidad?", "clave": "fam_obesidad"},
    {"texto": "¿Quiénes y a qué edad fueron diagnosticados?", "clave": "familiares_diagnosticados"},
]

# Hábitos
fumar = [
    {
        "texto": "¿Fumas actualmente?",
        "clave": "fuma",
        "condicional": {
            "sí": [{"texto": "¿Cuántos cigarrillos al día?", "clave": "cigarrillos_dia"}],
            "si": [{"texto": "¿Cuántos cigarrillos al día?", "clave": "cigarrillos_dia"}]
        }
    }
]

alcohol = [
    {
        "texto": "¿Consumes alcohol?",
        "clave": "alcohol",
        "condicional": {
            "sí": [{"texto": "¿Con qué frecuencia?", "clave": "frecuencia_alcohol"}],
            "si": [{"texto": "¿Con qué frecuencia?", "clave": "frecuencia_alcohol"}]
        }
    }
]

actividad = [
    {
        "texto": "¿Realiza actividad física?",
        "clave": "actividad_fisica",
        "condicional": {
            "sí": [
                {"texto": "¿Qué tipo?", "clave": "tipo_actividad"},
                {"texto": "¿Cuántas veces por semana?", "clave": "frecuencia_actividad"}
            ],
            "si": [
                {"texto": "¿Qué tipo?", "clave": "tipo_actividad"},
                {"texto": "¿Cuántas veces por semana?", "clave": "frecuencia_actividad"}
            ]
        }
    }
]

glucosa = [
    {
        "texto": "¿Se toma la glucosa en casa?",
        "clave": "glucosa_en_casa",
        "condicional": {
            "sí": [
                {"texto": "¿Con qué frecuencia?", "clave": "frecuencia_glucosa"},
                {"texto": "¿Cuál es su nivel promedio?", "clave": "promedio_glucosa"}
            ],
            "si": [
                {"texto": "¿Con qué frecuencia?", "clave": "frecuencia_glucosa"},
                {"texto": "¿Cuál es su nivel promedio?", "clave": "promedio_glucosa"}
            ]
        }
    }
]

# Datos alimenticios
alimenticio = [
    {"texto": "¿Sabe contar carbohidratos o sigue un plan alimenticio especial?", "clave": "plan_alimenticio"},
    {"texto": "¿Con qué frecuencia presenta sed excesiva?", "clave": "sed_excesiva"},
    {"texto": "¿Con qué frecuencia presenta micción frecuente?", "clave": "miccion_frecuente"},
    {"texto": "¿Con qué frecuencia presenta hambre excesiva?", "clave": "hambre_excesiva"},
    {"texto": "¿Con qué frecuencia presenta cansancio constante?", "clave": "cansancio_constante"},
    {"texto": "¿Con qué frecuencia presenta visión borrosa?", "clave": "vision_borrosa"},
    {"texto": "¿Con qué frecuencia presenta pérdida de peso sin causa aparente?", "clave": "perdida_peso"},
    {"texto": "¿Con qué frecuencia presenta hormigueo en manos/pies?", "clave": "hormigueo"},
    {"texto": "¿Con qué frecuencia presenta heridas que no cicatrizan?", "clave": "heridas_no_cicatrizan"},
]