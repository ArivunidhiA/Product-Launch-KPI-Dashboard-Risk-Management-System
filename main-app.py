import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.kpi_dashboard import KPIDashboard
from src.risk_management.risk_analyzer import RiskAnalyzer
from src.utils.helpers import load_data

def main():
    st.set_page_config(page_title="Product Launch Dashboard", layout="wide")
    st.title("Product Launch KPI Dashboard & Risk Management System")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select a Page",
        ["KPI Dashboard", "Risk Management", "Retail Readiness"]
    )

    # Load data
    product_data = load_data('data/sample_data/product_data.csv')
    launch_milestones = load_data('data/sample_data/launch_milestones.csv')
    risks_data = load_data('data/sample_data/risks.csv')
    retail_data = load_data('data/sample_data/retail_readiness.csv')

    if page == "KPI Dashboard":
        display_kpi_dashboard(product_data, launch_milestones)
    elif page == "Risk Management":
        display_risk_management(risks_data)
    else:
        display_retail_readiness(retail_data)

def display_kpi_dashboard(product_data, launch_milestones):
    dashboard = KPIDashboard(product_data, launch_milestones)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products", dashboard.get_total_products())
    with col2:
        st.metric("On-Track Launches", dashboard.get_ontrack_launches())
    with col3:
        st.metric("Completion Rate", f"{dashboard.get_completion_rate()}%")

    # Timeline Progress
    st.subheader("Launch Timeline Progress")
    fig = dashboard.create_timeline_chart()
    st.plotly_chart(fig, use_container_width=True)

def display_risk_management(risks_data):
    risk_analyzer = RiskAnalyzer(risks_data)
    
    st.subheader("Risk Matrix")
    fig = risk_analyzer.create_risk_matrix()
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Risks")
    st.table(risk_analyzer.get_top_risks())

def display_retail_readiness(retail_data):
    st.subheader("Retail Readiness Status")
    
    # Display readiness metrics
    readiness_df = pd.DataFrame(retail_data)
    fig = px.bar(readiness_df, x='category', y='completion_percentage',
                 title='Retail Readiness by Category')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
