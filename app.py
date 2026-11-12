import streamlit as st

# Configuración de la página con estética de libro de cocina
st.set_page_config(
    page_title="CookVoice - Libro de Cocina Inteligente",
    page_icon="📖",
    layout="centered"
)

# Estilos CSS personalizados para dar estética de libro de cocina rústico/moderno
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF7;
        color: #2C221E;
        font-family: 'Georgia', serif;
    }
    .book-title {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #4A3B32;
        border-bottom: 2px solid #D4A373;
        padding-bottom: 10px;
    }
    .recipe-card {
        background-color: #F4F1EA;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #D4A373;
        margin-bottom: 20px;
    }
    .iot-panel {
        background-color: #E9EDC9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #CCD5AE;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal estilo libro
st.markdown("<h1 class='book-title'>📖 CookVoice: Recetario & IoT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Tu asistente de cocina manos libres, conectado al entorno físico.</p>", unsafe_allow_html=True)

# Base de datos de recetas (Catálogo estructurado estilo ChatPDF)
recetas = {
    "Pasta Alfredo Casera": {
        "tiempo": "20 minutos",
        "dificultad": "Fácil",
        "ingredientes": [
            "200g de pasta Fettuccine",
            "100ml de crema de leche",
            "50g de mantequilla",
            "2 dientes de ajo picados",
            "Queso parmesano al gusto"
        ],
        "pasos": [
            "Paso 1: Pon a hervir una olla grande con agua y sal. Cuando hierva, añade la pasta y cocina por 10 minutos.",
            "Paso 2: En una sartén grande, derrama la mantequilla a fuego medio y sofríe los dos dientes de ajo picados hasta que doren.",
            "Paso 3: Vierte la crema de leche sobre el sofrito de ajo, baja el fuego y mezcla suavemente durante 3 minutos.",
            "Paso 4: Integra la pasta cocida directamente a la salsa, espolvorea el queso parmesano y sirve caliente."
        ]
    },
    "Ensalada César con Pollo": {
        "tiempo": "15 minutos",
        "dificultad": "Muy Fácil",
        "ingredientes": [
            "1 pechuga de pollo en tiras",
            "1 lechuga romana lavada y picada",
            "Croutones de pan",
            "Queso parmesano rallado",
            "Aderezo César"
        ],
        "pasos": [
            "Paso 1: Cocina las tiras de pechuga de pollo en una sartén con un chorrito de aceite, sal y pimienta hasta que estén doradas.",
            "Paso 2: En un bol grande, coloca la lechuga romana limpia y picada como base principal.",
            "Paso 3: Agrega los croutones de pan crujiente y el queso parmesano rallado sobre la lechuga.",
            "Paso 4: Añade el pollo tibio encima, baña con el aderezo César al gusto y mezcla antes de servir."
        ]
    },
    "Waffles Caseros Esponjosos": {
        "tiempo": "25 minutos",
        "dificultad": "Media",
        "ingredientes": [
            "2 tazas de harina de trigo",
            "2 huevos",
            "1 y 1/2 tazas de leche",
            "1/2 taza de mantequilla derretida",
            "1 cucharada de polvo para hornear"
        ],
        "pasos": [
            "Paso 1: En un recipiente hondo, mezcla la harina de trigo junto con el polvo para hornear.",
            "Paso 2: En otro tazón, bate los huevos, añade la leche y la mantequilla derretida.",
            "Paso 3: Incorpora los ingredientes líquidos en los secos batiendo suavemente hasta obtener una mezcla homogénea sin grumos.",
            "Paso 4: Vierte la mezcla en la waflera caliente y hornea durante 4 o 5 minutos hasta que estén dorados."
        ]
    }
}

# Selección de receta en la interfaz (Estilo índice del libro)
st.markdown("### 🔍 Índice de Recetas")
receta_seleccionada = st.selectbox("Elige una receta del catálogo:", list(recetas.keys()))

receta_info = recetas[receta_seleccionada]

# Mostrar tarjeta de la receta
st.markdown(f"""
<div class='recipe-card'>
    <h2>{receta_seleccionada}</h2>
    <p><b>⏱️ Tiempo:</b> {receta_info['tiempo']} | <b>📊 Dificultad:</b> {receta_info['dificultad']}</p>
    <h4>Ingredientes:</h4>
    <ul>
        {''.join([f"<li>{ing}</li>" for ing in receta_info['ingredientes']])}
    </ul>
</div>
""", unsafe_allow_html=True)

# Sección de Control de Hardware IoT (Foco y Extractor simulados)
st.markdown("### 🔌 Panel de Automatización Física (Wokwi / IoT)")
st.markdown("<div class='iot-panel'>Controla los actuadores de tu cocina automáticamente al iniciar la receta.</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    foco_estado = st.toggle("💡 Encender Foco del Mesón", value=True)
with col2:
    extractor_estado = st.toggle("🌀 Encender Extractor de Humos", value=False)

if foco_estado:
    st.success("Estado Físico: Foco iluminando el mesón de trabajo.")
else:
    st.info("Estado Físico: Foco apagado.")

if extractor_estado:
    st.warning("Estado Físico: Extractor funcionando (extrayendo vapor).")
else:
    st.info("Estado Físico: Extractor en reposo.")

# Sección de Modo Cocina con Asistente de Voz Integrado (JavaScript + Web Speech API)
st.markdown("### 🎙️ Modo Cocina Manos Libres (Micrófono)")
st.markdown("Haz clic en el botón de abajo para activar el reconocimiento de voz. Di **'siguiente'** para avanzar de paso o **'repetir'** para escuchar de nuevo.")

# Pasos de la receta en formato JSON seguro para JavaScript
pasos_js = str(receta_info['pasos']).replace("'", '"')

# Componente HTML + JavaScript embebido en Streamlit para el manejo del micrófono y síntesis de voz (Text-to-Speech)
voz_html = f"""
<div style="background-color:#FAF0CA; padding:20px; border-radius:10px; text-align:center;">
    <h3 style="color:#333;">Asistente de Voz Activo</h3>
    <p id="instruccion-actual" style="font-size:18px; font-weight:bold; color:#D4A373;">Presiona el botón y di "Siguiente"</p>
    <button onclick="iniciarAsistente()" style="background-color:#D4A373; color:white; border:none; padding:12px 24px; font-size:16px; border-radius:8px; cursor:pointer;">🎤 Iniciar Control por Voz</button>
</div>

<script>
const pasos = {pasos_js};
let indiceActual = 0;

function hablar(texto) {{
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = 'es-ES';
    window.speechSynthesis.speak(utterance);
}}

function iniciarAsistente() {{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {{
        alert("Tu navegador no soporta reconocimiento de voz. Usa Google Chrome.");
        return;
    }}
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = false;
    
    document.getElementById("instruccion-actual").innerText = pasos[indiceActual];
    hablar(pasos[indiceActual]);
    
    recognition.onresult = function(event) {{
        const comando = event.results[0][0].transcript.toLowerCase();
        console.log("Comando detectado: ", comando);
        
        if (comando.includes("siguiente") || comando.includes("avanzar")) {{
            if (indiceActual < pasos.length - 1) {{
                indiceActual++;
                document.getElementById("instruccion-actual").innerText = pasos[indiceActual];
                hablar(pasos[indiceActual]);
            }} else {{
                hablar("Has finalizado la receta. ¡Buen provecho!");
                document.getElementById("instruccion-actual").innerText = "¡Receta finalizada!";
            }}
        }} else if (comando.includes("repetir") || comando.includes("otra vez")) {{
            hablar(pasos[indiceActual]);
        }}
    }};
    
    recognition.onend = function() {{
        // Reiniciar escucha automáticamente para manos libres continuo
        try {{
            recognition.start();
        }} catch(e) {{}}
    }};
    
    recognition.start();
}}
</script>
"""

st.components.v1.html(voz_html, height=220)
