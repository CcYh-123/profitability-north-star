import pandas as pd
import numpy as np

def generate_insights(df):
    """
    Generates strategic financial advice based on the provided dataframe.
    Returns a list of advice strings.
    """
    insights = []
    
    # Calculate global metrics for the period
    total_revenue = df['revenue'].sum()
    total_spend = df['ad_spend'].sum()
    total_margin = df['contribution_margin'].sum()
    global_mer = total_revenue / total_spend if total_spend > 0 else 0
    margin_pct = total_margin / total_revenue if total_revenue > 0 else 0
    
    # 1. Break-even / Profitability Analysis
    if global_mer < 3.0:
        required_mer = 3.0
        # If MER is low, we need more revenue for the same spend, or less spend for same revenue.
        # Implying CPA needs to drop. (MER = AOV / CPA). If MER < 3, CPA is too high given AOV.
        # To get MER 3, CPA must be AOV / 3. Current CPA is AOV / MER.
        # Reduction factor = (AOV/3) / (AOV/MER) = MER / 3
        # Ex: MER 2.0. Need 3.0. Reduction = 2/3 = 0.66 -> Drop CPA by 33%.
        reduction_needed = 1 - (global_mer / required_mer)
        
        insight = f"🔴 **ALERTA DE RENTABILIDAD**: El MER Global ({global_mer:.2f}) está por debajo del objetivo (3.0). " \
                  f"Para recuperar el equilibrio, necesitas **reducir tu CPA en un {reduction_needed:.0%}** " \
                  f"o aumentar tu AOV proporcionalmente."
        insights.append(insight)
    else:
        insights.append(f"🟢 **Salud Financiera**: El MER Global ({global_mer:.2f}) es saludable. Estás imprimiendo beneficio.")

    # 2. Margin Protection (Emergency Scenario)
    if margin_pct < 0.15:
        insights.append(f"⚠️ **PROTOCOL DE EMERGENCIA**: El Margen de Contribución Global es {margin_pct:.1%}. "
                        "Acción Recomendada: **Pausar canales con MER < 2.0 inmediatamente** y revisar estructura de COGS.")
    
    # 3. Scaling Scenario (Opportunity)
    # Identify best day of week or simple growth advice
    if global_mer > 4.0:
        insights.append(f"🚀 **Oportunidad de Escala**: Tienes exceso de eficiencia (MER {global_mer:.2f}). "
                        "Recomendación: **Aumentar presupuesto un 20%** en tus campañas top performers.")
    else:
         insights.append(f"⚖️ **Estrategia**: Mantener presupuesto actual y optimizar creativos para mejorar el CTR.")

    return insights

def simulate_scenarios(df):
    """
    Returns a dictionary with financial projections for 3 scenarios.
    """
    total_profit = df['contribution_margin'].sum()
    
    scenarios = {
        "Conservador (Actual)": total_profit,
        "Escalamiento (+20% Spend Eficiente)": total_profit * 1.15, # Simplifying: Spend up, slightly lower marginal return but higher profit mass
        "Emergencia (Corte de Gasto)": total_profit * 0.9 # Usually cutting spend protects margin % but drops absolute profit dollars initially
    }
    
    # Refine Scaling Logic: If we spend 20% more, and assuming strictly linear returns (simulated)
    # Realistically, efficiency drops. Let's model: Spend +20% -> Revenue +15% -> Profit change?
    # For now, per instructions, we just output the projections. 
    # Let's keep it simple arithmetic based on the prompt's implied logic.
    
    metrics = {
        "Conservador": {
            "Profit": total_profit, 
            "Desc": "Mantener ritmo actual."
        },
        "Escalamiento": {
            "Profit": total_profit * 1.25 if df['mer'].mean() > 4 else total_profit * 1.10,
            "Desc": "Aumentar inversión 20% en High-MER."
        },
        "Emergencia": {
            "Profit": total_profit * 0.8, # Assuming we cut bad spend but lose volume
            "Desc": "Pausar ads con MER < 1.5." # Drastic cut
        }
    }
    return metrics
