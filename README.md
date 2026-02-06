# ⭐ Profitability North Star (BMS)

> **Soberanía Técnica**: Este activo es la "Fuente de Verdad" financiera, diseñada para desacoplar las decisiones de negocio de las métricas vanidosas de las plataformas publicitarias (ROAS).

## 🎯 Impacto Financiero
Este sistema calcula la rentabilidad real del negocio en tiempo real, integrando:
- **Contribution Margin**: (Revenue - COGS - AdSpend - GatewayFees).
- **MER (Marketing Efficiency Ratio)**: El indicador macro de eficiencia.
- **Detección de Anomalías**: Alerta temprana cuando el MER cae por debajo del umbral de rentabilidad (3.0).

## 🏗️ Arquitectura
- `src/ingest.py`: Motor de ingesta y normalización (Simulación Híbrida).
- `src/model.py`: Lógica financiera pura (Pandas/NumPy).
- `app.py`: Dashboard de mando C-Level (Streamlit).

## 🚀 Ejecución

1. **Instalar**:
   ```powershell
   pip install -r requirements.txt
   ```
2. **Generar Datos**:
   ```powershell
   python src/ingest.py
   ```
3. **Lanzar Dashboard**:
   ```powershell
   streamlit run app.py
   ```

## 🛡️ Soberanía de Datos
Los datos crudos residen localmente en `/data` y **NO** se sincronizan con este repositorio para garantizar privacidad y cumplimiento.
