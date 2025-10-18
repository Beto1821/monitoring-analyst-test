import streamlit as st
import simpy
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import sqlite3
import os
import sys

# Adicionar path parent para importar módulos do projeto
sys.path.append('..')

from checkout_simulation import CheckoutSimulation
from anomaly_simulation import AnomalySimulation
from scenario_simulation import ScenarioSimulation

# 🔧 Configuração da página (apenas quando executado individualmente)
try:
    st.set_page_config(
        page_title="🎮 Simulações SimPy",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # Já foi configurado pelo main.py
    pass

# 🎨 Header moderno
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
     padding: 2rem; border-radius: 15px; margin-bottom: 2rem; 
     box-shadow: 0 8px 32px rgba(0,0,0,0.1);'>
    <h1 style='color: white; text-align: center; margin: 0; 
        font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        🎮 Simulações SimPy
    </h1>
    <p style='color: rgba(255,255,255,0.9); text-align: center; 
        margin: 0.5rem 0 0 0; font-size: 1.3rem;'>
        Modelagem e Simulação de Checkouts com SimPy
    </p>
</div>
""", unsafe_allow_html=True)

# 📊 Carregar dados reais para comparação
@st.cache_data
def load_real_data():
    """Carrega dados reais dos bancos SQLite para comparação"""
    try:
        # Tentar carregar dados do SQLite
        db_path = '../Analyze_data/data.db'
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM data_table", conn)
            conn.close()
            return df
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados reais: {str(e)}")
    
    # Dados sintéticos como fallback
    hours = list(range(24))
    return pd.DataFrame({
        'time': [f"{h:02d}h" for h in hours],
        'today': np.random.randint(10, 50, 24),
        'yesterday': np.random.randint(8, 45, 24),
        'same_day_last_week': np.random.randint(12, 48, 24)
    })

# Sidebar - Controles de simulação
st.sidebar.header("🎮 Controles de Simulação")

# Tipo de simulação
simulation_type = st.sidebar.selectbox(
    "🎯 Tipo de Simulação:",
    ["🛒 Simulação de Checkouts", "🚨 Simulação de Anomalias", 
     "🔍 Análise de Cenários", "📊 Comparação Real vs Simulado"]
)

# Parâmetros globais
duration_hours = st.sidebar.slider("⏰ Duração (horas)", 1, 72, 24)
random_seed = st.sidebar.number_input("🎲 Seed Aleatória", 0, 1000, 42)

# Botão principal
run_simulation = st.sidebar.button("🚀 Executar Simulação", type="primary")

if run_simulation:
    # Configurar seed para reprodutibilidade
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    with st.spinner(f"🎯 Executando {simulation_type}..."):
        
        if simulation_type == "🛒 Simulação de Checkouts":
            # === SIMULAÇÃO DE CHECKOUTS ===
            st.header("🛒 Simulação de Checkouts")
            
            # Parâmetros específicos
            col1, col2 = st.columns(2)
            with col1:
                checkout1_capacity = st.sidebar.number_input("Capacidade Checkout 1", 1, 5, 1)
                arrival_rate = st.sidebar.slider("Taxa Chegada (clientes/h)", 5, 50, 20)
            with col2:
                checkout2_capacity = st.sidebar.number_input("Capacidade Checkout 2", 1, 5, 1)
                service_time_multiplier = st.sidebar.slider("Multiplicador Tempo Serviço C2", 1.0, 5.0, 2.0)
            
            # Executar simulação
            sim = CheckoutSimulation(
                checkout1_capacity=checkout1_capacity,
                checkout2_capacity=checkout2_capacity,
                service_time_multiplier=service_time_multiplier
            )
            results_df = sim.run_simulation(duration_hours)
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_customers = len(results_df)
                st.metric("👥 Total Clientes", total_customers)
            
            with col2:
                avg_wait = results_df['wait_time'].mean()
                st.metric("⏰ Tempo Espera Médio", f"{avg_wait:.1f} min")
            
            with col3:
                c1_usage = len(results_df[results_df['checkout'] == 1])
                usage_pct = (c1_usage / total_customers) * 100
                st.metric("📊 Uso Checkout 1", f"{usage_pct:.1f}%")
            
            with col4:
                max_wait = results_df['wait_time'].max()
                st.metric("⏰ Maior Tempo Espera", f"{max_wait:.1f} min")
            
            # Gráficos
            tabs = st.tabs(["📊 Transações por Hora", "⏰ Tempos de Espera", "📈 Utilização"])
            
            with tabs[0]:
                # Transações por hora
                hourly_data = results_df.groupby(['hour', 'checkout']).size().reset_index(name='count')
                
                fig = px.bar(
                    hourly_data, 
                    x='hour', 
                    y='count', 
                    color='checkout',
                    title="📊 Distribuição de Transações por Hora",
                    labels={'hour': 'Hora do Dia', 'count': 'Número de Transações'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tabs[1]:
                # Tempos de espera
                fig = px.box(
                    results_df, 
                    x='checkout', 
                    y='wait_time',
                    title="⏰ Distribuição dos Tempos de Espera",
                    labels={'checkout': 'Checkout', 'wait_time': 'Tempo de Espera (min)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tabs[2]:
                # Utilização por hora
                utilization = results_df.groupby(['hour', 'checkout']).agg({
                    'service_time': 'sum',
                    'wait_time': 'mean'
                }).reset_index()
                
                fig = px.line(
                    utilization, 
                    x='hour', 
                    y='service_time', 
                    color='checkout',
                    title="📈 Utilização dos Checkouts por Hora",
                    labels={'hour': 'Hora', 'service_time': 'Tempo Total de Serviço (min)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            if st.checkbox("📋 Mostrar Dados Detalhados"):
                st.dataframe(results_df.head(100))
        
        elif simulation_type == "🚨 Simulação de Anomalias":
            # === SIMULAÇÃO DE ANOMALIAS ===
            st.header("🚨 Simulação de Anomalias")
            
            # Parâmetros específicos
            mtbf_c1 = st.sidebar.slider("MTBF Checkout 1 (horas)", 4, 24, 12)
            mtbf_c2 = st.sidebar.slider("MTBF Checkout 2 (horas)", 2, 16, 6)
            network_failure_rate = st.sidebar.slider("Taxa Falha Rede (%)", 0, 20, 5)
            
            # Executar simulação
            anomaly_sim = AnomalySimulation(
                mtbf_checkout1=mtbf_c1,
                mtbf_checkout2=mtbf_c2,
                network_failure_rate=network_failure_rate/100
            )
            anomalies_df = anomaly_sim.run_simulation(duration_hours)
            
            if not anomalies_df.empty:
                # Métricas de anomalias
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_anomalies = len(anomalies_df)
                    st.metric("🚨 Total Anomalias", total_anomalies)
                
                with col2:
                    critical_count = len(anomalies_df[anomalies_df['severity'] == 'critical'])
                    st.metric("🔴 Críticas", critical_count)
                
                with col3:
                    avg_duration = anomalies_df['duration'].mean()
                    st.metric("⏰ Duração Média", f"{avg_duration:.1f}h")
                
                with col4:
                    c2_issues = len(anomalies_df[anomalies_df['checkout'] == 2])
                    st.metric("🛒 Problemas C2", c2_issues)
                
                # Timeline de anomalias
                fig = px.timeline(
                    anomalies_df,
                    x_start='start_time',
                    x_end='end_time',
                    y='checkout',
                    color='severity',
                    title="📅 Timeline de Anomalias",
                    labels={'start_time': 'Início', 'end_time': 'Fim'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Distribuição por tipo
                type_dist = anomalies_df['type'].value_counts()
                fig_pie = px.pie(
                    values=type_dist.values,
                    names=type_dist.index,
                    title="📊 Distribuição por Tipo de Anomalia"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Tabela de anomalias
                st.subheader("📋 Registro de Anomalias")
                st.dataframe(anomalies_df)
            else:
                st.info("✅ Nenhuma anomalia detectada na simulação!")
        
        elif simulation_type == "🔍 Análise de Cenários":
            # === ANÁLISE DE CENÁRIOS ===
            st.header("🔍 Análise de Cenários")
            
            scenario_sim = ScenarioSimulation()
            scenarios_results = scenario_sim.run_all_scenarios(duration_hours)
            
            # Comparação de cenários
            scenario_metrics = []
            for scenario_name, results in scenarios_results.items():
                metrics = {
                    'Cenário': scenario_name,
                    'Clientes Atendidos': len(results['transactions']),
                    'Tempo Espera Médio': results['transactions']['wait_time'].mean(),
                    'Anomalias': len(results['anomalies']),
                    'Disponibilidade': results['availability']
                }
                scenario_metrics.append(metrics)
            
            metrics_df = pd.DataFrame(scenario_metrics)
            
            # Mostrar tabela comparativa
            st.subheader("📊 Comparação de Cenários")
            st.dataframe(metrics_df.style.highlight_min(
                subset=['Tempo Espera Médio', 'Anomalias']).highlight_max(
                subset=['Clientes Atendidos', 'Disponibilidade']))
            
            # Gráfico de comparação
            fig = px.bar(
                metrics_df,
                x='Cenário',
                y=['Clientes Atendidos', 'Anomalias'],
                title="📊 Comparação de Performance por Cenário",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Análise de ROI
            st.subheader("💰 Análise de ROI")
            roi_data = scenario_sim.calculate_roi(scenarios_results)
            
            col1, col2 = st.columns(2)
            with col1:
                fig_roi = px.bar(
                    x=list(roi_data.keys()),
                    y=list(roi_data.values()),
                    title="💰 ROI por Cenário (%)",
                    labels={'x': 'Cenário', 'y': 'ROI (%)'}
                )
                st.plotly_chart(fig_roi, use_container_width=True)
            
            with col2:
                # Recomendações
                best_scenario = max(roi_data, key=roi_data.get)
                st.success(f"🏆 Melhor Cenário: **{best_scenario}**")
                st.info(f"💰 ROI: {roi_data[best_scenario]:.1f}%")
                
                # Recomendações específicas
                recommendations = scenario_sim.get_recommendations(scenarios_results)
                st.subheader("💡 Recomendações")
                for rec in recommendations:
                    st.write(f"• {rec}")
        
        else:  # Comparação Real vs Simulado
            # === COMPARAÇÃO REAL VS SIMULADO ===
            st.header("📊 Comparação: Dados Reais vs Simulação")
            
            # Carregar dados reais
            real_data = load_real_data()
            
            # Executar simulação para comparação
            sim = CheckoutSimulation()
            sim_results = sim.run_simulation(duration_hours)
            
            # Agregar dados simulados por hora
            sim_hourly = sim_results.groupby('hour').agg({
                'customer_id': 'count',
                'wait_time': 'mean',
                'service_time': 'mean'
            }).reset_index()
            
            # Gráfico comparativo
            fig = go.Figure()
            
            # Dados reais
            if 'today' in real_data.columns:
                fig.add_trace(go.Scatter(
                    x=real_data.index,
                    y=real_data['today'],
                    mode='lines+markers',
                    name='📊 Dados Reais',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ))
            
            # Dados simulados
            fig.add_trace(go.Scatter(
                x=sim_hourly['hour'],
                y=sim_hourly['customer_id'],
                mode='lines+markers',
                name='🎮 Simulação SimPy',
                line=dict(color='red', width=3, dash='dot'),
                marker=dict(size=8, symbol='diamond')
            ))
            
            fig.update_layout(
                title="📊 Comparação: Dados Reais vs Simulação SimPy",
                xaxis_title="Hora do Dia",
                yaxis_title="Número de Transações",
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Métricas de comparação
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'today' in real_data.columns:
                    real_total = real_data['today'].sum()
                    st.metric("📊 Total Real", real_total)
                
            with col2:
                sim_total = sim_hourly['customer_id'].sum()
                st.metric("🎮 Total Simulado", sim_total)
            
            with col3:
                if 'today' in real_data.columns:
                    accuracy = (1 - abs(real_total - sim_total) / real_total) * 100
                    st.metric("🎯 Precisão", f"{accuracy:.1f}%")
            
            # Análise de correlação
            if 'today' in real_data.columns and len(real_data) == len(sim_hourly):
                correlation = np.corrcoef(real_data['today'][:len(sim_hourly)], 
                                       sim_hourly['customer_id'])[0, 1]
                st.info(f"📈 Correlação Real vs Simulado: {correlation:.3f}")

else:
    # Estado inicial - mostrar informações
    st.info("👆 Configure os parâmetros na barra lateral e clique em '🚀 Executar Simulação'")
    
    # Mostrar exemplos do que cada simulação faz
    st.subheader("🎯 Tipos de Simulação Disponíveis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛒 Simulação de Checkouts
        - **Modelagem de filas** e tempos de atendimento
        - **Capacidade configurável** dos checkouts
        - **Padrões de chegada** realísticos
        - **Análise de utilização** e eficiência
        
        ### 🚨 Simulação de Anomalias
        - **Falhas de hardware** (MTBF configurável)
        - **Problemas de software** (glitches)
        - **Falhas de rede** (outages)
        - **Timeline de incidentes**
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Análise de Cenários
        - **Cenário Atual** vs **Melhorado**
        - **Análise de ROI** das melhorias
        - **Redundância** e **manutenção preventiva**
        - **Recomendações** baseadas em dados
        
        ### 📊 Comparação Real vs Simulado
        - **Validação** dos modelos
        - **Calibração** de parâmetros
        - **Análise de correlação**
        - **Métricas de precisão**
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    🎮 <strong>Simulações SimPy</strong> | Powered by SimPy, Streamlit & Python
</div>
""", unsafe_allow_html=True)