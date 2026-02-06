import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def normalize_columns(df):
    """
    Standardizes column names to snake_case.
    """
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def generate_mock_data(days=90):
    """
    Generates simulated data for Shopify Sales and Ad Platforms.
    """
    np.random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    for date in dates:
        # Simulate Revenue (Daily Volatility)
        base_revenue = 2000
        seasonality = 1 + np.sin(date.dayofyear / 365 * 2 * np.pi) * 0.2
        noise = np.random.normal(0, 300)
        revenue = max(0, (base_revenue * seasonality) + noise)
        
        # Simulate Ad Spend (Marketing Efficiency Ratio fluctuating betweem 3 and 6)
        mer_target = np.random.uniform(3.0, 6.0)
        ad_spend = revenue / mer_target
        
        # Simulate COGS (approx 30-40% of revenue)
        cogs_pct = np.random.uniform(0.30, 0.40)
        cogs = revenue * cogs_pct
        
        # Simulate Gateway Fees (approx 2-3% of revenue)
        gateway_pct = np.random.uniform(0.02, 0.03)
        gateway_fees = revenue * gateway_pct
        
        # New Customers (Simulated metric)
        new_customers = int(revenue / 150) # Approx $150 AOV
        
        data.append({
            'Date': date,
            'Revenue': round(revenue, 2),
            'Ad Spend': round(ad_spend, 2),
            'COGS': round(cogs, 2),
            'Gateway Fees': round(gateway_fees, 2),
            'New Customers': new_customers
        })
        
    df = pd.DataFrame(data)
    return normalize_columns(df)

def main():
    print("🚀 Inciando Ingesta de Datos Simulada...")
    
    df = generate_mock_data()
    
    # Validation
    assert not df.empty, "El DataFrame está vacío"
    assert (df['revenue'] >= 0).all(), "Error: Ingresos negativos detectados"
    
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'maestro.csv')
    df.to_csv(output_path, index=False)
    
    print(f"✅ Datos generados exitosamente en: {output_path}")
    print(df.head())

if __name__ == "__main__":
    main()
