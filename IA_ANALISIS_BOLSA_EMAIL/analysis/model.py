import os
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


# =========================
# FUNCIÓN PRINCIPAL
# =========================
def analyze_stock(ticker, start_date="2020-01-01"):
    print("📥 Descargando datos...")

    data = yf.download(ticker, start=start_date)

    if data.empty:
        print("❌ No se han podido descargar datos")
        return None, None

    # =========================
    # INDICADORES
    # =========================
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    # RSI
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # Últimos valores (⚠️ convertir a float)
    last_close = float(data["Close"].iloc[-1])
    ma20 = float(data["MA20"].iloc[-1])
    ma50 = float(data["MA50"].iloc[-1])
    rsi = float(data["RSI"].iloc[-1])

    # =========================
    # EVALUACIÓN "IA"
    # =========================
    if ma20 > ma50 and rsi < 70:
        decision = (
            "ESCENARIO FAVORABLE 📈\n"
            "La tendencia es alcista (MA20 > MA50).\n"
            "El RSI no muestra sobrecompra.\n"
            "Podría ser un contexto positivo para invertir, "
            "aunque siempre con gestión del riesgo."
        )
    elif rsi > 70:
        decision = (
            "ESCENARIO DE RIESGO ⚠️\n"
            "El RSI indica sobrecompra.\n"
            "El precio podría corregir en el corto plazo.\n"
            "Conviene extremar la prudencia."
        )
    elif rsi < 30:
        decision = (
            "ESCENARIO ESPECULATIVO 🔄\n"
            "El RSI indica sobreventa.\n"
            "Podría producirse un rebote, "
            "pero el riesgo sigue siendo elevado."
        )
    else:
        decision = (
            "ESCENARIO NEUTRAL ⚖️\n"
            "No hay una señal técnica clara.\n"
            "El mercado se encuentra en fase de indecisión."
        )

    # =========================
    # TEXTO DEL INFORME
    # =========================
    report = f"""
INFORME DE ANÁLISIS BURSÁTIL (IA)

Empresa analizada: {ticker}

Precio actual: {last_close:.2f} €
Media móvil 20 sesiones (MA20): {ma20:.2f}
Media móvil 50 sesiones (MA50): {ma50:.2f}
RSI (14): {rsi:.2f}

Evaluación técnica:
{decision}

Conclusión:
Este análisis se basa en datos históricos y en indicadores técnicos.
No constituye una recomendación de inversión.
"""

    # =========================
    # GRÁFICO
    # =========================
    os.makedirs("results/plots", exist_ok=True)

    plot_path = "results/plots/grafico.png"

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Close"], label="Precio")
    plt.plot(data.index, data["MA20"], label="MA20")
    plt.plot(data.index, data["MA50"], label="MA50")
    plt.title(f"Análisis técnico - {ticker}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (€)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return report, plot_path


# =========================
# PDF
# =========================
def create_pdf(report_text, image_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "Informe de Análisis Bursátil (IA)")

    # Texto
    c.setFont("Helvetica", 10)
    text = c.beginText(2 * cm, height - 3.5 * cm)

    for line in report_text.split("\n"):
        text.textLine(line)

    c.drawText(text)

    # Nueva página para gráfico
    c.showPage()

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 2 * cm, "Gráfico técnico")

    c.drawImage(
        image_path,
        2 * cm,
        height / 2 - 2 * cm,
        width=16 * cm,
        preserveAspectRatio=True,
        mask="auto",
    )

    c.save()



