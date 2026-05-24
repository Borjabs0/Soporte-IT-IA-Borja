"""
app.py
Interfaz web del Asistente de Soporte Técnico IT
Desarrollada con Streamlit + CSS personalizado
Conecta con backend_aws.py para procesar incidencias via AWS Bedrock + RAG
"""

import sys
import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

# Asegurar que src/ está en el path para importar los módulos locales
sys.path.insert(0, os.path.dirname(__file__))

from backend_aws import procesar_incidencia

# ── Configuración de la página ───────────────────────────────────────────────

st.set_page_config(
    page_title="Soporte TIC — IES La Mar",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS personalizado ────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

  /* Reset y base */
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
  }

  /* Fondo general */
  .stApp {
    background-color: #0f1117;
    color: #e0e0e0;
  }

  /* Cabecera principal */
  .header-block {
    background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 60%, #0d2137 100%);
    border-bottom: 2px solid #2a7ae2;
    padding: 2rem 2.5rem 1.5rem;
    margin: -1rem -1rem 2rem -1rem;
  }
  .header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0 0 0.2rem 0;
  }
  .header-sub {
    font-size: 0.85rem;
    color: #7aabda;
    font-weight: 300;
    letter-spacing: 0.5px;
  }

  /* Etiqueta de urgencia */
  .badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 3px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .badge-critica { background: #3d0000; color: #ff4444; border: 1px solid #ff4444; }
  .badge-alta    { background: #3d1a00; color: #ff8c00; border: 1px solid #ff8c00; }
  .badge-media   { background: #2d2500; color: #ffd000; border: 1px solid #ffd000; }
  .badge-baja    { background: #002d00; color: #44cc44; border: 1px solid #44cc44; }

  .badge-hardware { background: #00142d; color: #4da6ff; border: 1px solid #4da6ff; }
  .badge-software { background: #1a002d; color: #b36aff; border: 1px solid #b36aff; }
  .badge-redes    { background: #002d1a; color: #33cc99; border: 1px solid #33cc99; }

  /* Tarjetas de resultado */
  .result-card {
    background: #161b27;
    border: 1px solid #2a3550;
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
  }
  .result-card-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #4a7aaa;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid #2a3550;
    padding-bottom: 0.5rem;
  }

  /* Pasos de la hoja de ruta */
  .paso {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 0.6rem;
    padding: 0.5rem 0.6rem;
    border-radius: 4px;
    background: #0f1420;
    border-left: 3px solid #2a7ae2;
    font-size: 0.92rem;
    line-height: 1.5;
  }
  .paso-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #2a7ae2;
    font-weight: 600;
    min-width: 1.8rem;
    padding-top: 0.1rem;
  }

  /* Correo */
  .correo-box {
    background: #0a0f1a;
    border: 1px solid #2a3550;
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c8d8e8;
    white-space: pre-wrap;
  }

  /* Botón copiar correo */
  .copy-hint {
    font-size: 0.75rem;
    color: #4a7aaa;
    margin-top: 0.5rem;
    font-style: italic;
  }

  /* Input textarea */
  .stTextArea textarea {
    background-color: #161b27 !important;
    color: #e0e0e0 !important;
    border: 1px solid #2a3550 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.95rem !important;
  }
  .stTextArea textarea:focus {
    border-color: #2a7ae2 !important;
    box-shadow: 0 0 0 2px rgba(42, 122, 226, 0.2) !important;
  }

  /* Botón principal */
  .stButton > button {
    background: #2a7ae2 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    transition: background 0.2s !important;
  }
  .stButton > button:hover {
    background: #1a5ab8 !important;
  }

  /* Spinner */
  .stSpinner > div { border-top-color: #2a7ae2 !important; }

  /* Error */
  .error-box {
    background: #2d0000;
    border: 1px solid #ff4444;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    color: #ff8888;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
  }

  /* Ejemplos */
  .ejemplo-btn {
    display: inline-block;
    background: #161b27;
    border: 1px solid #2a3550;
    border-radius: 4px;
    padding: 0.35rem 0.8rem;
    font-size: 0.82rem;
    color: #7aabda;
    cursor: pointer;
    margin: 0.25rem 0.25rem 0.25rem 0;
  }

  /* Ocultar elementos por defecto de Streamlit */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Cabecera ─────────────────────────────────────────────────────────────────

st.markdown("""
<div class="header-block">
  <div class="header-title">🖥️ &nbsp;Asistente de Soporte TIC</div>
  <div class="header-sub">IES La Mar — Sistema RAG sobre AWS Bedrock &nbsp;|&nbsp; Clasificación automática de incidencias</div>
</div>
""", unsafe_allow_html=True)

# ── Layout: columna izquierda (entrada) y derecha (resultado) ─────────────────

col_entrada, col_resultado = st.columns([1, 1.2], gap="large")

# ── COLUMNA IZQUIERDA: formulario ─────────────────────────────────────────────

with col_entrada:
    st.markdown("#### Describe la incidencia")

    # Incidencias de ejemplo
    ejemplos = [
        "El proyector parpadea en azul y no detecta el portátil.",
        "Un alumno no puede iniciar sesión en su cuenta.",
    ]

    st.markdown("<div style='margin-bottom:0.4rem; font-size:0.8rem; color:#4a7aaa;'>EJEMPLOS RÁPIDOS</div>", unsafe_allow_html=True)

    ejemplo_seleccionado = None
    for i, ej in enumerate(ejemplos):
        if st.button(f"↗  {ej}", key=f"ej_{i}", use_container_width=True):
            ejemplo_seleccionado = ej

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # Inicializar el estado del textarea
    if "texto_incidencia" not in st.session_state:
        st.session_state.texto_incidencia = ""

    if ejemplo_seleccionado:
        st.session_state.texto_incidencia = ejemplo_seleccionado

    incidencia = st.text_area(
        label="Texto de la incidencia",
        value=st.session_state.texto_incidencia,
        height=160,
        placeholder="Describe el problema con el mayor detalle posible: qué equipo es, qué síntomas tiene, cuándo empezó...",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    procesar = st.button("ANALIZAR INCIDENCIA →", use_container_width=True)

# ── COLUMNA DERECHA: resultados ───────────────────────────────────────────────

with col_resultado:
    st.markdown("#### Resultado del análisis")

    if procesar and incidencia.strip():
        with st.spinner("Consultando el manual y procesando con AWS Bedrock..."):
            resultado = procesar_incidencia(incidencia.strip())

        if "error" in resultado:
            st.markdown(f"""
            <div class='error-box'>
              ⚠️ Error al procesar la incidencia:<br><br>
              {resultado['error']}
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── Clasificación ────────────────────────────────────────
            cat = resultado.get("clasificacion", {}).get("categoria", "—")
            urg = resultado.get("clasificacion", {}).get("urgencia", "—")

            badge_urg_class = {
                "Crítica": "badge-critica",
                "Alta":    "badge-alta",
                "Media":   "badge-media",
                "Baja":    "badge-baja",
            }.get(urg, "badge-baja")

            badge_cat_class = {
                "Hardware": "badge-hardware",
                "Software": "badge-software",
                "Redes":    "badge-redes",
            }.get(cat, "badge-hardware")

            st.markdown(f"""
            <div class='result-card'>
              <div class='result-card-title'>Clasificación</div>
              <div style='display:flex; gap:0.75rem; align-items:center; flex-wrap:wrap;'>
                <span class='badge {badge_cat_class}'>{cat}</span>
                <span class='badge {badge_urg_class}'>Urgencia: {urg}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Hoja de ruta (Solución robusta: Formateo nativo en una sola llamada) ──
            pasos = resultado.get("hoja_de_ruta", [])
            pasos_interiores_html = ""
            
            for i, paso in enumerate(pasos, 1):
                texto_paso = paso
                if texto_paso.lower().startswith(f"paso {i}:"):
                    texto_paso = texto_paso[len(f"paso {i}:"):].strip()
                
                # Construimos el string plano de los items
                pasos_interiores_html += (
                    "<div class='paso'>"
                      f"<span class='paso-num'>#{i:02d}</span>"
                      f"<span>{texto_paso}</span>"
                    "</div>"
                )

            # Inyectamos todo el esqueleto HTML estructurado de un solo golpe atómico
            hoja_ruta_completa = (
                "<div class='result-card'>"
                  "<div class='result-card-title'>Hoja de ruta para el técnico</div>"
                  f"<div style='display: flex; flex-direction: column; gap: 0.5rem;'>{pasos_interiores_html}</div>"
                "</div>"
            )

            st.markdown(hoja_ruta_completa, unsafe_allow_html=True)

            # ── Correo automático ────────────────────────────────────
            correo = resultado.get("correo_respuesta", "")
            st.markdown(f"""
            <div class='result-card'>
              <div class='result-card-title'>Correo automático al usuario</div>
              <div class='correo-box'>{correo}</div>
              <div class='copy-hint'>Copia el texto y envíalo directamente al usuario.</div>
            </div>
            """, unsafe_allow_html=True)

    elif procesar and not incidencia.strip():
        st.warning("Por favor, describe la incidencia antes de analizar.")

    else:
        # Estado vacío — instrucciones visuales
        st.markdown("""
        <div style='
          height: 380px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          border: 1px dashed #2a3550;
          border-radius: 6px;
          color: #2a3550;
          text-align: center;
          padding: 2rem;
        '>
          <div style='font-size:3rem; margin-bottom:1rem;'>🖥️</div>
          <div style='font-family: IBM Plex Mono, monospace; font-size:0.85rem; color:#3a5070; line-height:1.8;'>
            Introduce una incidencia a la izquierda<br>
            o selecciona uno de los ejemplos rápidos.<br><br>
            El sistema consultará el Manual de<br>
            Procedimientos IT y generará<br>
            la clasificación, hoja de ruta<br>
            y correo automáticamente.
          </div>
        </div>
        """, unsafe_allow_html=True)