import streamlit as st
import av
import threading
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from ultralytics import YOLO

# Configuración de la página con estética de libro de cocina
st.set_page_config(
    page_title="CookVoice - Libro de Cocina Inteligente con YOLO",
    page_icon="📖",
    layout="centered"
)

# Cargar el modelo YOLOv8 ligero
@st.cache_resource
def cargar_modelo_yolo():
    return YOLO("yolov8n.pt")

modelo_yolo = cargar_modelo_yolo()

# Diccionario de etiquetas específicas en español para utensilios de cocina
NOMBRES_UTENSILIOS_ES = {
    "bowl": "Tazón para mezclar",
    "cup": "Taza medidora",
    "knife": "Cuchillo de cocina",
    "spoon": "Cuchara mezcladora",
    "fork": "Tenedor de cocina",
    "bottle": "Botella de aceite/líquidos",
    "wine glass": "Recipiente/copa medidora",
    "banana": "Ingrediente: Plátano",
    "apple": "Ingrediente: Manzana",
    "orange": "Ingrediente: Naranja",
    "carrot": "Ingrediente: Zanahoria",
    "broccoli": "Ingrediente: Brócoli",
    "sandwich": "Preparación: Sándwich",
    "pizza": "Preparación: Pizza",
    "donut": "Preparación: Masa/Dona",
    "cake": "Preparación: Pastel/Mezcla",
    "cell phone": "Temporizador / Asistente móvil"
}

# Lock y conjunto compartido seguro entre hilos de video y UI
lock_deteccion = threading.Lock()
if "detectados_set" not in st.session_state:
    st.session_state.detectados_set = set()
DETECTADOS_COMPARTIDOS = st.session_state.detectados_set

# Estilos CSS con estética de libro de cocina rústico
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
    .tachado {
        text-decoration: line-through;
        color: #2D6A4F;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal estilo libro
st.markdown("<h1 class='book-title'>📖 CookVoice: Recetario, Visión YOLO & IoT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Detección rápida de utensilios con nombres específicos, voz manos libres y control físico.</p>", unsafe_allow_html=True)

# Base de datos de recetas con utensilios específicos
recetas = {
    "Pasta Alfredo Casera": {
        "tiempo": "20 minutos",
        "dificultad": "Fácil",
        "ingredientes": ["200g de Pasta Fettuccine", "100ml de Crema de leche", "50g de Mantequilla", "2 dientes de Ajo", "Queso parmesano"],
        "implementos": [
            ("bowl", "Tazón hondo para pasta"),
            ("knife", "Cuchillo para picar ajo"),
            ("spoon", "Cuchara de madera para salsa"),
            ("fork", "Tenedor para servir pasta"),
            ("wine glass", "Copa/vaso medidor de crema")
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
        "ingredientes": ["1 Pechuga de pollo", "Lechuga romana", "Croutones de pan", "Queso parmesano rallado", "Aderezo César"],
        "implementos": [
            ("bowl", "Ensaladera honda"),
            ("knife", "Cuchillo de corte para pollo y lechuga"),
            ("fork", "Tenedor de cocina"),
            ("spoon", "Cuchara para aderezo"),
            ("bottle", "Botella de aceite o aderezo")
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
        "ingredientes": ["2 tazas de Harina de trigo", "2 Huevos", "1 y 1/2 tazas de Leche", "1/2 taza de Mantequilla", "Polvo para hornear"],
        "implementos": [
            ("bowl", "Tazón batidor de mezcla"),
            ("cup", "Taza medidora de ingredientes"),
            ("spoon", "Cuchara medidora de polvo hornear"),
            ("fork", "Tenedor batidor de huevos"),
            ("bottle", "Botella de leche o esencia")
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

# Reiniciar utensilios detectados al cambiar de receta
if "receta_actual" not in st.session_state or st.session_state.receta_actual != receta_seleccionada:
    st.session_state.receta_actual = receta_seleccionada
    with lock_deteccion:
        DETECTADOS_COMPARTIDOS.clear()

# Mostrar tarjeta de la receta
st.markdown(f"""
<div class='recipe-card'>
    <h2>{receta_seleccionada}</h2>
    <p><b>⏱️ Tiempo:</b> {receta_info['tiempo']} | <b>📊 Dificultad:</b> {receta_info['dificultad']}</p>
    <h4>Ingredientes:</h4>
    <ul>
        {''.join([f"<li>{ing}</li>" for ing in receta_info['ingredientes']])}
    </ul>
    <h4>🛠️ Utensilios específicos requeridos:</h4>
</div>
""", unsafe_allow_html=True)

# Fragmento que actualiza la lista tachada rápidamente sin recargar toda la app
@st.fragment(run_every=1.0)
def mostrar_checklist_utensilios(implementos):
    with lock_deteccion:
        detectados_snapshot = set(DETECTADOS_COMPARTIDOS)

    cols = st.columns(len(implementos))
    for idx, (clase_yolo, nombre_especifico) in enumerate(implementos):
        with cols[idx]:
            if clase_yolo in detectados_snapshot:
                st.markdown(f"<p class='tachado'>✅ {nombre_especifico}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: #7A6A5E;'>⏳ {nombre_especifico}</p>", unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("🔄 Reiniciar lista de utensilios"):
            with lock_deteccion:
                DETECTADOS_COMPARTIDOS.clear()
            st.rerun(scope="fragment")

mostrar_checklist_utensilios(receta_info["implementos"])

# SECCIÓN DE VISIÓN ARTIFICIAL RÁPIDA EN TIEMPO REAL CON YOLOv8
st.markdown("### 👁️ Escáner Rápido de Utensilios en Vivo (YOLOv8)")
st.markdown("<div class='vision-panel'>Haz clic en <b>START</b> para activar la cámara. El modelo analiza en alta velocidad con resolución optimizada y etiqueta cada utensilio con su nombre específico.</div>", unsafe_allow_html=True)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

clases_objetivo_actual = {clase for clase, _ in receta_info["implementos"]}

class FastYOLOVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame_idx = 0
        self.ultimo_anotado = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_idx += 1

        # Procesar 1 de cada 2 fotogramas con imgsz=320 para máxima fluidez en la nube
        if self.frame_idx % 2 == 1 or self.ultimo_anotado is None:
            resultados = modelo_yolo(img, imgsz=320, conf=0.28, iou=0.45, verbose=False)
            resultado = resultados[0]

            # Reemplazar nombres genéricos por nombres específicos de cocina en las etiquetas
            nombres_personalizados = {}
            detectados_en_frame = set()

            for cls_id, nombre_orig in modelo_yolo.names.items():
                nombres_personalizados[cls_id] = NOMBRES_UTENSILIOS_ES.get(
                    nombre_orig, f"Utensilio: {nombre_orig.capitalize()}"
                )

            if resultado.boxes is not None:
                for box in resultado.boxes:
                    cls_id = int(box.cls[0])
                    nombre_orig = modelo_yolo.names[cls_id]
                    if nombre_orig in clases_objetivo_actual:
                        detectados_en_frame.add(nombre_orig)

            if detectados_en_frame:
                with lock_deteccion:
                    DETECTADOS_COMPARTIDOS.update(detectados_en_frame)

            resultado.names = nombres_personalizados
            self.ultimo_anotado = resultado.plot(line_width=2, font_size=1.0)

        return av.VideoFrame.from_ndarray(self.ultimo_anotado, format="bgr24")

webrtc_streamer(
    key="yolo-cocina-fast",
    video_processor_factory=FastYOLOVideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video": {"width": {"ideal": 640}, "height": {"ideal": 480}},
        "audio": False,
    },
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
