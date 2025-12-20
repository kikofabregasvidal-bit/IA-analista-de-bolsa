import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def analyze_stock(ticker: str, start_date: str):
    try:
        # =========================
        # DESCARGA DE DATOS
        # =========================
        data = yf.download(ticker, start=start_date, progress=False)

        if data.empty:
            return None, None

        # Forzar a Series (CLAVE para evitar errores)
        close = data["Close"].squeeze()

        # =========================
        # INDICADORES TÉCNICOS
        # =========================

        # Medias móviles
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()

        # RSI
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_last = float(rsi.iloc[-1])

        # Bandas de Bollinger
        std20 = close.rolling(20).std()
        bb_upper = ma20 + 2 * std20
        bb_lower = ma20 - 2 * std20

        # =========================
        # ÚLTIMOS VALORES
        # =========================
        last_price = float(close.iloc[-1])
        ma20_last = float(ma20.iloc[-1])
        ma50_last = float(ma50.iloc[-1])

        # =========================
        # EVALUACIÓN "IA"
        # =========================
        if ma20_last > ma50_last and rsi_last < 70:
            decision = "Escenario favorable 📈\nTendencia alcista sin sobrecompra."
        elif rsi_last > 70:
            decision = "Escenario de riesgo ⚠️\nRSI en sobrecompra."
        elif rsi_last < 30:
            decision = "Escenario especulativo 🔄\nRSI en sobreventa."
        else:
            decision = "Escenario neutral ⏸️\nSin señal clara."

        # =========================
        # GRÁFICO
        # =========================
        os.makedirs("results/plots", exist_ok=True)

        plt.figure(figsize=(10, 5))
        plt.plot(close, label="Precio", color="white")
        plt.plot(ma20, label="MA20", color="orange")
        plt.plot(ma50, label="MA50", color="green")
        plt.plot(bb_upper, linestyle="--", color="red", alpha=0.6)
        plt.plot(bb_lower, linestyle="--", color="red", alpha=0.6)
        plt.title(f"Análisis técnico - {ticker}")
        plt.legend()
        plt.grid(alpha=0.3)

        plot_path = f"results/plots/{ticker}_grafico.png"
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()

        # =========================
        # INFORME TEXTO
        # =========================
        report = f"""
ANÁLISIS TÉCNICO — {ticker}

Precio actual: {last_price:.2f}
MA20: {ma20_last:.2f}
MA50: {ma50_last:.2f}
RSI: {rsi_last:.2f}

Evaluación:
{decision}

⚠️ Análisis educativo. No es una recomendación de inversión.
"""

        return report, plot_path

    except Exception as e:
        print("ERROR EN ANALYZE_STOCK:", e)
        return None, None




