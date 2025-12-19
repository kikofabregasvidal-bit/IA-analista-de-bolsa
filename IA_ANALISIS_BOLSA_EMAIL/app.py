import streamlit as st
import os
from analysis.model import analyze_stock, create_pdf

st.set_page_config(
    page_title="IA de Análisis Bursátil",
    layout="centered"
)

st.title("📈 IA de Análisis Bursátil")
st.write("Análisis técnico educativo (MA20, MA50 y RSI)")
st.caption("Basado en datos históricos hasta el último cierre disponible")

# Selector de empresa
ticker = st.selectbox(
    "Selecciona una empresa:",
    [
        "ITX.MC", "SAN.MC", "BBVA.MC", "IBE.MC",
        "AAPL", "MSFT", "NVDA", "TSLA"
    ]
)

# Botón principal
if st.button("Analizar"):
    with st.spinner("Analizando datos..."):
        report, plot_path = analyze_stock(ticker, "2020-01-01")

    if report is None:
        st.error("No se ha podido realizar el análisis.")
    else:
        st.success("Análisis completado")

        # Mostrar gráfico
        st.image(plot_path)

        # Mostrar texto
        st.text(report)

        # Crear PDF
        os.makedirs("results/reports", exist_ok=True)
        pdf_path = f"results/reports/informe_{ticker}.pdf"
        create_pdf(report, plot_path, pdf_path)

        # Botón de descarga
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Descargar informe en PDF",
                data=pdf_file,
                file_name=f"informe_{ticker}.pdf",
                mime="application/pdf"
            )
