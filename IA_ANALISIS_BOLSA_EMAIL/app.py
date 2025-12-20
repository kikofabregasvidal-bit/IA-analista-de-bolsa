import streamlit as st
from analysis.model import analyze_stock
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import tempfile
import os
from datetime import date

# ===============================
# CONFIGURACIÓN DE PÁGINA
# ===============================
st.set_page_config(
    page_title="IA de Análisis Bursátil",
    page_icon="📈",
    layout="centered"
)

# ===============================
# FUNCIÓN PARA CREAR PDF
# ===============================
def create_pdf(report_text, plot_path, ticker):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    width, height = A4

    # ---- PORTADA ----
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 3 * cm, "INFORME DE ANÁLISIS BURSÁTIL")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 4.5 * cm, f"Empresa: {ticker}")

    c.setFont("Helvetica", 11)
    c.drawCentredString(
        width / 2,
        height - 6 * cm,
        f"Fecha del informe: {date.today().strftime('%d/%m/%Y')}"
    )

    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(
        width / 2,
        height - 8 * cm,
        "Análisis técnico educativo basado en datos históricos"
    )

    c.showPage()

    # ---- INFORME ----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 2 * cm, "Informe técnico")

    text = c.beginText(2 * cm, height - 3.5 * cm)
    text.setFont("Helvetica", 10)

    for line in report_text.split("\n"):
        text.textLine(line)

        if text.getY() < 2 * cm:
            c.drawText(text)
            c.showPage()
            text = c.beginText(2 * cm, height - 2 * cm)
            text.setFont("Helvetica", 10)

    c.drawText(text)
    c.showPage()

    # ---- GRÁFICO ----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 2 * cm, "Gráfico técnico")

    c.drawImage(
        plot_path,
        2 * cm,
        4 * cm,
        width=width - 4 * cm,
        preserveAspectRatio=True,
        mask="auto"
    )

    # ---- AVISO LEGAL ----
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        2 * cm,
        2 * cm,
        "Aviso: Este informe es educativo y no constituye una recomendación de inversión."
    )

    c.save()
    return temp_pdf.name


# ===============================
# CABECERA
# ===============================
st.title("📈 IA de Análisis Bursátil")
st.write(
    "Aplicación de **análisis técnico profesional** basada en datos históricos "
    "hasta el último cierre disponible."
)

st.markdown(
    """
**Indicadores incluidos:**
- Media móvil 20 sesiones (MA20)
- Media móvil 50 sesiones (MA50)
- Índice de Fuerza Relativa (RSI)
- Tendencia general y escenario técnico
"""
)

st.divider()

# ===============================
# SELECTOR DE EMPRESA
# ===============================
ticker = st.selectbox(
    "Selecciona una empresa:",
    [
        "ITX.MC",
        "SAN.MC",
        "BBVA.MC",
        "IBE.MC",
        "ALM.MC",
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA"
    ]
)

# ===============================
# BOTÓN
# ===============================
analyze = st.button("🔍 Analizar empresa")

# ===============================
# RESULTADOS
# ===============================
if analyze:
    with st.spinner("Analizando datos históricos y generando informe profesional..."):
        report, plot_path = analyze_stock(
            ticker=ticker,
            start_date="2020-01-01"
        )

    if report is None or plot_path is None:
        st.error("❌ Error al realizar el análisis.")
    else:
        st.success("✅ Análisis completado")

        # ---- GRÁFICO ----
        st.subheader("📊 Gráfico técnico completo")
        st.image(plot_path, use_container_width=True)

        # ---- INFORME ----
        st.subheader("📝 Informe profesional")
        st.text(report)

        # ---- PDF ----
        st.subheader("⬇️ Descargar informe completo")

        pdf_path = create_pdf(report, plot_path, ticker)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Descargar informe en PDF",
                data=pdf_file,
                file_name=f"informe_{ticker}.pdf",
                mime="application/pdf"
            )

        # ---- AVISO ----
        st.info(
            "⚠️ Este análisis es educativo y no constituye una recomendación de inversión. "
            "Los mercados financieros conllevan riesgo."
        )




