import streamlit as st
from analysis.model import analyze_stock

# ===============================
# CONFIGURACIÓN DE LA PÁGINA
# ===============================
st.set_page_config(
    page_title="IA de Análisis Bursátil",
    page_icon="📈",
    layout="centered"
)

# ===============================
# CABECERA
# ===============================
st.markdown(
    """
    <h1 style="text-align:center;">📈 IA de Análisis Bursátil</h1>
    <p style="text-align:center; font-size:18px;">
        Análisis técnico educativo basado en <b>MA20, MA50 y RSI</b><br>
        <span style="font-size:14px;">Datos históricos hasta el último cierre disponible</span>
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ===============================
# SELECTOR DE EMPRESA
# ===============================
st.subheader("🏢 Selecciona una empresa")

ticker = st.selectbox(
    "Empresa",
    [
        "ITX.MC",   # Inditex
        "SAN.MC",   # Santander
        "BBVA.MC",
        "IBE.MC",
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA"
    ]
)

# ===============================
# BOTÓN DE ANÁLISIS
# ===============================
st.markdown("<br>", unsafe_allow_html=True)
analyze = st.button("🔍 Analizar empresa", use_container_width=True)

# ===============================
# RESULTADOS
# ===============================
if analyze:
    with st.spinner("Analizando datos y generando informe..."):
        report, plot_path, pdf_path = analyze_stock(
            ticker=ticker,
            start_date="2020-01-01"
        )

    if report is None:
        st.error("❌ No se ha podido realizar el análisis.")
    else:
        st.success("✅ Análisis completado")

        # ----- GRÁFICO -----
        st.subheader("📊 Gráfico técnico")
        st.image(plot_path, use_column_width=True)

        # ----- TEXTO DEL INFORME -----
        st.subheader("🧠 Evaluación del análisis")
        st.text(report)

        # ----- DESCARGA PDF -----
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Descargar informe en PDF",
                    data=f,
                    file_name=pdf_path.split("/")[-1],
                    mime="application/pdf",
                    use_container_width=True
                )

# ===============================
# PIE DE PÁGINA
# ===============================
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:13px;">
        ⚠️ Proyecto educativo · No constituye recomendación de inversión<br>
        Creado con Python · Streamlit · yfinance
    </p>
    """,
    unsafe_allow_html=True
)
