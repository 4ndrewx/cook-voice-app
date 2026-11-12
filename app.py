import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from ultralytics import YOLO

# Configuración de la página con estética de libro de cocina
st.set_page_config(
    page_title="CookVoice - Libro de Cocina Inteligente con YOLO",
    page_icon="📖",
    layout="centered"
)

# Cargar el modelo YOLOv8 ligero (se descarga automáticamente la primera vez)
@st.cache_resource
def cargar_modelo_yolo():
    return YOLO("yolov8n.pt")

modelo_yolo = cargar_modelo_yolo()

# Estilos CSS personalizados para dar estética de libro de cocina
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
st.markdown("<h1 class='book-title'>📖 CookVoice: Recetario, Visión YOLO & IoT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Asistente multimodal con detección de objetos YOLOv8 en tiempo real y control físico.</p>", unsafe_allow_html=True)

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

# Selección de receta
st.markdown("### 🔍 Índice de Recetas (Catálogo ChatPDF)")
receta_seleccionada = st.selectbox("Elige una receta del catálogo:", list(recetas.keys()))
receta_info = recetas[receta_seleccionada]

# Mostrar tarjeta de la receta
st.markdown(f"""
<div class='recipe-card'>
    <h2>{receta_seleccionada}</h2>
    <p><b>⏱️ Tiempo:</b> {receta_info['tiempo']} | <b>📊 Dificultad:</b> {receta_info['dificultad']}</p>
    <h4>Ingredientes necesarios:</h4>
    <ul>
        {''.join([f"<li>{ing}</li>" for ing in receta_info['ingredientes']])}
    </ul>
</div>
""", unsafe_allow_html=True)

# SECCIÓN DE VISIÓN ARTIFICIAL EN TIEMPO REAL CON YOLOv8
st.markdown("### 👁️ Escáner de Cocina en Tiempo Real (YOLOv8)")
st.markdown("<div class='vision-panel'>Haz clic en <b>START</b> para encender la cámara. El modelo YOLOv8 detectará alimentos y utensilios en vivo (ej. tazas, tazones, frutas, botellas, cuchillos, tenedores).</div>", unsafe_allow_html=True)

# Configuración STUN para asegurar conexión de video en Streamlit Cloud
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class YOLOVideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Ejecutar inferencia real con YOLOv8 (confianza mínima 40%)
        resultados = modelo_yolo(img, conf=0.40, verbose=False)
        
        # Dibujar automáticamente los recuadros (bounding boxes) y etiquetas detectadas
        img_anotada = resultados[0].plot()
        
        return av.VideoFrame.from_ndarray(img_anotada, format="bgr24")

webrtc_streamer(
    key="yolo-cocina-live",
    video_processor_factory=YOLOVideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

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
