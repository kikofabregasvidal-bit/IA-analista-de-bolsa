import os
import streamlit as st
from analysis.model import analyze_stock, create_pdf

# -------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title="IA de Análisis Bursátil",
    page_icon="📈",
    layout="centered"
)

st.title("📈 IA de Análisis Bursátil")
st.write("Análisis técnico educativo basado en **MA20, MA50 y RSI**")
st.caption("Datos históricos hasta el último cierre disponible")

st.divider()

# -------------------------------------------------
# SELECTOR DE EMPRESA
# -------------------------------------------------
ticker = st.selectbox(
    "Selecciona una empresa:",
    [
        "ITX.MC", "SAN.MC", "BBVA.MC", "IBE.MC",
        "AAPL", "MSFT", "NVDA", "TSLA"
    ]
)

analyze = st.button("🔍 Analizar")

# -------------------------------------------------
# RESULTADOS
# -------------------------------------------------
if analyze:
    with st.spinner("Analizando datos y generando informe..."):
        report, plot_path = analyze_stock(
            ticker=ticker,
            start_date="2020-01-01"
        )

    if report is None or plot_path is None:
        st.error("❌ No se ha podido generar el análisis.")
    else:
        # Mostrar resultados
        st.success("✅ Análisis completado")
        st.image(plot_path, caption=f"Gráfico técnico de {ticker}")
        st.text(report)

        # -------------------------------------------------
        # CREAR PDF
        # -------------------------------------------------
        os.makedirs("results/reports", exist_ok=True)
        pdf_path = f"results/reports/informe_{ticker}.pdf"

        create_pdf(report, plot_path, pdf_path)

        # -------------------------------------------------
        # BOTÓN DE DESCARGA
        # -------------------------------------------------
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Descargar informe en PDF",
                data=f,
                file_name=f"informe_{ticker}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

