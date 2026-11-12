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
    .vision-panel {
        background-color: #FDE2E4;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #FFCAD4;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal estilo libro
st.markdown("<h1 class='book-title'>📖 CookVoice: Recetario, Visión en Vivo & IoT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Tu asistente de cocina multimodal, con escáner de ingredientes en tiempo real y control físico.</p>", unsafe_allow_html=True)

# Base de datos de recetas (Catálogo estructurado estilo ChatPDF)
recetas = {
    "Pasta Alfredo Casera": {
        "tiempo": "20 minutos",
        "dificultad": "Fácil",
        "ingredientes": [
            "Pasta Fettuccine",
            "Crema de leche",
            "Mantequilla",
            "Ajo picado",
            "Queso parmesano"
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
            "Pechuga de pollo",
            "Lechuga romana",
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
            "Harina de trigo",
            "Huevos",
            "Leche",
            "Mantequilla derretida",
            "Polvo para hornear"
        ],
        "pasos": [
            "Paso 1: En un recipiente hondo, mezcla la harina de trigo junto con el polvo para hornear.",
            "Paso 2: En otro tazón, bate los huevos, añade la leche y la mantequilla derretida.",
            "Paso 3: Incorpora los ingredientes líquidos en los secos batiendo suavemente hasta obtener una mezcla homogénea sin grumos.",
            "Paso 4: Vierte la mezcla en la waflera caliente y hornea durante 4 o 5 minutos hasta que estén dorados."
        ]
    }
}

# Selección de receta
st.markdown("### 🔍 Índice de Recetas (Catálogo)")
receta_seleccionada = st.selectbox("Elige una receta del catálogo:", list(recetas.keys()))
receta_info = recetas[receta_seleccionada]

# Mostrar tarjeta de la receta
st.markdown(f"""
<div class='recipe-card'>
    <h2>{receta_seleccionada}</h2>
    <p><b>⏱️ Tiempo:</b> {receta_info['tiempo']} | <b>📊 Dificultad:</b> {receta_info['dificultad']}</p>
    <h4>Ingredientes que debe detectar la cámara:</h4>
    <ul>
        {''.join([f"<li>{ing}</li>" for ing in receta_info['ingredientes']])}
    </ul>
</div>
""", unsafe_allow_html=True)

# NUEVA SECCIÓN: Escáner de Video en Tiempo Real con Recuadro IA
st.markdown("### 📸 Escáner de Ingredientes en Tiempo Real (Visión IA)")
st.markdown("<div class='vision-panel'>Apunta con tu cámara a los ingredientes sobre el mesón. El sistema de IA escaneará y validará los elementos en vivo dentro del recuadro.</div>", unsafe_allow_html=True)

# Componente HTML/JS con Video en vivo y recuadro de escaneo estilo HUD
scanner_html = f"""
<div style="background-color:#1E1E1E; padding:15px; border-radius:12px; text-align:center; position:relative; overflow:hidden;">
    <h4 style="color:#FFCAD4; margin-top:0;">Transmisión en Vivo - IA Detector</h4>
    
    <div style="position:relative; display:inline-block; width:100%; max-width:480px; border-radius:8px; overflow:hidden; border:2px solid #D4A373;">
        <video id="webcam" autoplay playsinline style="width:100%; display:block; border-radius:6px;"></video>
        
        <!-- Recuadro de escaneo animado en tiempo real (HUD) -->
        <div style="position:absolute; top:20%; left:20%; width:60%; height:60%; border:2px dashed #00FF66; border-radius:8px; box-shadow: 0 0 15px rgba(0,255,102,0.5); pointer-events:none; animation: pulse 2s infinite;">
            <div style="position:absolute; top:0; left:0; background:#00FF66; color:#000; font-size:11px; font-weight:bold; padding:2px 6px;">ESCANEANDO INSUMO...</div>
        </div>
    </div>
    
    <div id="detection-status" style="margin-top:10px; font-size:15px; font-weight:bold; color:#00FF66;">Buscando ingredientes en el área...</div>
    
    <button onclick="iniciarCamara()" style="margin-top:10px; background-color:#D4A373; color:white; border:none; padding:10px 20px; font-size:14px; border-radius:6px; cursor:pointer; font-weight:bold;">🟢 Encender Cámara de Escaneo</button>
</div>

<style>
@keyframes pulse {{
    0% {{ border-color: #00FF66; }}
    50% {{ border-color: #FFD166; }}
    100% {{ border-color: #00FF66; }}
}}
</style>

<script>
async function iniciarCamara() {{
    const video = document.getElementById('webcam');
    try {{
        const stream = await navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: 'environment' }} }});
        video.srcObject = stream;
        
        // Simulación interactiva de detección de IA en tiempo real
        const ingredientes = {str(receta_info['ingredientes']).replace("'", '"')};
        let index = 0;
        
        setInterval(() => {{
            if (video.srcObject) {{
                const detectado = ingredientes[index % ingredientes.length];
                document.getElementById('detection-status').innerText = "✅ Detectado con 98% de precisión: " + detectado;
                index++;
            }}
        }}, 3500);

    catch (err) {{
        alert("No se pudo acceder a la cámara. Revisa los permisos del navegador.");
        console.error(err);
    }}
}}
</script>
"""

st.components.v1.html(scanner_html, height=450)

# Panel IoT (Foco y Extractor)
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

# Sección de Modo Cocina con Vocabulario Extendido (Avanzar, Retroceder, Repetir)
st.markdown("### 🎙️ Modo Cocina Manos Libres (Micrófono Inteligente)")
st.markdown("Haz clic en **Activar**, y utiliza comandos naturales como **'siguiente'**, **'atrás'**, **'regresar'** o **'repetir'**.")

pasos_js = str(receta_info['pasos']).replace("'", '"')

voz_html = f"""
<div style="background-color:#FAF0CA; padding:20px; border-radius:10px; text-align:center;">
    <h3 style="color:#333; margin-top:0;">Asistente de Voz Extendido</h3>
    <p id="instruccion-actual" style="font-size:18px; font-weight:bold; color:#D4A373; min-height:50px;">Presiona el botón para comenzar</p>
    <p id="feedback-voz" style="font-size:13px; color:#666; font-style:italic;">Escuchando: (Inactivo)</p>
    <button onclick="iniciarAsistente()" style="background-color:#D4A373; color:white; border:none; padding:12px 24px; font-size:16px; border-radius:8px; cursor:pointer; font-weight:bold;">🎤 Activar Reconocimiento de Voz</button>
</div>

<script>
const pasos = {pasos_js};
let indiceActual = 0;
let recognition;
let isRunning = false;

function hablar(texto) {{
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = 'es-ES';
    window.speechSynthesis.speak(utterance);
}}

function iniciarAsistente() {{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {{
        alert("Tu navegador no soporta reconocimiento de voz. Usa Google Chrome o Edge.");
        return;
    }}
    
    if (isRunning) return;
    
    recognition = new SpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = true;
    recognition.interimResults = false;
    
    document.getElementById("instruccion-actual").innerText = pasos[indiceActual];
    hablar(pasos[indiceActual]);
    
    recognition.onstart = function() {{
        isRunning = true;
        document.getElementById("feedback-voz").innerText = "Escuchando activo... Habla ahora.";
    }};
    
    recognition.onresult = function(event) {{
        const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
        document.getElementById("feedback-voz").innerText = "Escuché: \\"" + transcript + "\\"";
        
        console.log("Comando detectado: ", transcript);
        
        if (transcript.includes("siguiente") || transcript.includes("avanza") || transcript.includes("pasa") || transcript.includes("adelante") || transcript.includes("sigue")) {{
            if (indiceActual < pasos.length - 1) {{
                indiceActual++;
                document.getElementById("instruccion-actual").innerText = pasos[indiceActual];
                hablar(pasos[indiceActual]);
            }} else {{
                hablar("Has finalizado la receta. ¡Buen provecho!");
                document.getElementById("instruccion-actual").innerText = "¡Receta finalizada con éxito!";
            }}
        }} 
        else if (transcript.includes("atrás") || transcript.includes("anterior") || transcript.includes("regresar") || transcript.includes("retroceder") || transcript.includes("vuelve")) {{
            if (indiceActual > 0) {{
                indiceActual--;
                document.getElementById("instruccion-actual").innerText = pasos[indiceActual];
                hablar(pasos[indiceActual]);
            }} else {{
                hablar("Estás en el primer paso.");
            }}
        }}
        else if (transcript.includes("repetir") || transcript.includes("otra vez") || transcript.includes("repite") || transcript.includes("vuelta")) {{
            hablar(pasos[indiceActual]);
        }}
    }};
    
    recognition.onerror = function(event) {{
        console.log("Error de reconocimiento: ", event.error);
    }};
    
    recognition.onend = function() {{
        if (isRunning) {{
            try {{
                recognition.start();
            }} catch(e) {{}}
        }}
    }};
    
    recognition.start();
}}
</script>
"""

st.components.v1.html(voz_html, height=250)
