import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.model import load_data, apply_attribution_logic
from src.advisor import generate_insights, simulate_scenarios

# Page Config
st.set_page_config(page_title="Profitability North Star", page_icon="⭐", layout="wide")

# Dark Mode custom CSS implies Streamlit's default dark theme, but we can enforce some styles
st.markdown("""
<style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #30333d;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("⭐ Profitability North Star")
    st.markdown("### The Financial Truth (BMS)")

    # 1. Ingest & Process
    try:
        raw_df = load_data()
        df = apply_attribution_logic(raw_df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # 2. Sidebar Controls
    st.sidebar.header("⚙️ Configuración")
    
    # Date Filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input(
        "Rango de Fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

    # Scenario Selector
    scenario = st.sidebar.selectbox("Escenario", ["Realista", "Pesimista (-20% Rev)", "Optimista (+20% Rev)"])
    if scenario == "Pesimista (-20% Rev)":
        df_filtered['revenue'] *= 0.8
        df_filtered['contribution_margin'] = df_filtered['revenue'] - df_filtered['cogs'] - df_filtered['ad_spend'] - df_filtered['gateway_fees']
    elif scenario == "Optimista (+20% Rev)":
        df_filtered['revenue'] *= 1.2
        df_filtered['contribution_margin'] = df_filtered['revenue'] - df_filtered['cogs'] - df_filtered['ad_spend'] - df_filtered['gateway_fees']

    # 3. KPIs (North Star metrics)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_revenue = df_filtered['revenue'].sum()
    total_spend = df_filtered['ad_spend'].sum()
    total_profit = df_filtered['contribution_margin'].sum()
    global_mer = total_revenue / total_spend if total_spend > 0 else 0
    
    kpi1.metric("💰 Net Revenue", f"${total_revenue:,.0f}")
    kpi2.metric("📉 Ad Spend", f"${total_spend:,.0f}")
    kpi3.metric("⭐ Net Profit (CM)", f"${total_profit:,.0f}", delta_color="normal")
    kpi4.metric("🎯 MER Global", f"{global_mer:.2f}")

    st.markdown("---")

    # 4. CFO Advisor Section
    st.subheader("🤖 CFO Advisor: Estrategia & Proyecciones")
    
    # Generate insights based on filtered data (or global, but filtered makes sense for time periods)
    insights = generate_insights(df_filtered)
    scenarios = simulate_scenarios(df_filtered)
    
    c_adv1, c_adv2 = st.columns([1, 1])
    
    with c_adv1:
        st.info("### 💡 Insights Estratégicos")
        for i in insights:
            st.markdown(i)
            
    with c_adv2:
        st.success("### 🔮 Proyección de Escenarios (Profit)")
        # Display scenarios as a small dataframe or metrics
        scen_df = pd.DataFrame.from_dict(scenarios, orient='index')
        st.dataframe(scen_df.style.format({"Profit": "${:,.0f}"}))

    st.markdown("---")

    # 4. Charts
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("Evolución Diaria: Gasto vs. Beneficio")
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['contribution_margin'], mode='lines', name='Net Profit', line=dict(color='#00CC96', width=3)))
        fig_trend.add_trace(go.Bar(x=df_filtered['date'], y=df_filtered['ad_spend'], name='Ad Spend', marker_color='#EF553B', opacity=0.6))
        
        fig_trend.update_layout(
            template="plotly_dark",
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=0, r=0, t=0, b=0),
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Composición (Simulada)")
        # Simulating Channel split for visualization as per requirements request
        # In a real scenario, this would come from ingest.py with proper channel tags
        channels = ['Meta Ads', 'Google Ads', 'TikTok']
        spend_dist = [total_spend * 0.6, total_spend * 0.3, total_spend * 0.1]
        
        fig_pie = px.pie(names=channels, values=spend_dist, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 5. Data Table
    with st.expander("Ver Datos Detallados"):
        st.dataframe(df_filtered.style.format({
            'revenue': "${:,.2f}",
            'ad_spend': "${:,.2f}",
            'contribution_margin': "${:,.2f}",
            'mer': "{:.2f}"
        }))

if __name__ == "__main__":
    main()
