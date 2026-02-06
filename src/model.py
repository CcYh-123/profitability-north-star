import pandas as pd
import numpy as np

def load_data(filepath='data/maestro.csv'):
    """
    Loads the master data file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe. Ejecuta ingest.py primero.")
    return pd.read_csv(filepath, parse_dates=['date'])

def calculate_kpis(df):
    """
    Calculates primary financial KPIs: Contribution Margin, Net Profit, MER.
    """
    # Financial Calculations
    df['contribution_margin'] = df['revenue'] - df['cogs'] - df['ad_spend'] - df['gateway_fees']
    
    # Avoid division by zero
    df['mer'] = np.where(df['ad_spend'] > 0, df['revenue'] / df['ad_spend'], 0)
    
    # Net Profit (assuming CM is the main proxy for this level, or add fixed costs if needed)
    # For this model, Contribution Margin ~ Net Profit (Operational)
    df['net_profit'] = df['contribution_margin']
    
    return df

def detect_anomalies(df, mer_threshold=3.0):
    """
    Flags rows with financial anomalies.
    """
    df['anomaly_low_mer'] = df['mer'] < mer_threshold
    return df

def apply_attribution_logic(df):
    """
    Applies business logic for attribution/profitability.
    """
    df = calculate_kpis(df)
    df = detect_anomalies(df)
    return df

if __name__ == "__main__":
    import os
    print("🧠 Ejecutando Lógica Financiera...")
    
    try:
        df = load_data()
        df = apply_attribution_logic(df)
        
        # Output verification
        print(f"✅ Lógica aplicada. Muestra de {len(df)} días.")
        print(df[['date', 'mer', 'contribution_margin', 'anomaly_low_mer']].tail())
        
        # Save processed data for dashboard (optional, or dashboard can call this logic)
        df.to_csv('data/processed_financials.csv', index=False)
        print("💾 Datos procesados guardados en data/processed_financials.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
