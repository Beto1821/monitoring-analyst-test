import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os

# 🎨 Configuração da página (apenas quando executado individualmente)
try:
    st.set_page_config(
        page_title="🚨 Sistema de Alertas e Incidentes",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # Já foi configurado pelo main.py
    pass

# Função para detectar o caminho correto dos dados
def get_data_path(filename):
    """Detecta o caminho correto dos arquivos de dados"""
    # Primeiro, tenta o caminho relativo atual
    if os.path.exists(filename):
        return filename
    
    # Se executado a partir do main.py, ajusta o caminho
    alert_path = os.path.join("Alert_Incident", filename)
    if os.path.exists(alert_path):
        return alert_path
    
    # Caminho absoluto como fallback
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(current_dir, filename)
    if os.path.exists(abs_path):
        return abs_path
    
    # Se nada funcionar, retorna o caminho original para mostrar o erro
    return filename

# 📊 Carregar os dados
@st.cache_data
def load_data():
    df1 = pd.read_csv(get_data_path('data/transactions_1.csv'))
    df2 = pd.read_csv(get_data_path('data/transactions_2.csv'))
    return df1, df2

df1, df2 = load_data()

# 🎨 Header com estilo
st.markdown("""
<div style='background: linear-gradient(90deg, #ff6b6b, #feca57); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        🚨 Sistema de Alertas e Incidentes - Tarefa 2
    </h1>
    <p style='color: white; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>
        Monitoramento Inteligente de Transações e Detecção de Anomalias
    </p>
</div>
""", unsafe_allow_html=True)

# 📊 Métricas principais no topo
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_trans_1 = len(df1)
    st.metric("📊 Total Transações T1", total_trans_1, delta=f"+{(total_trans_1/1000):.1f}K")

with col2:
    total_trans_2 = len(df2)
    st.metric("📊 Total Transações T2", total_trans_2, delta=f"+{(total_trans_2/1000):.1f}K")

with col3:
    approved_rate_1 = (df1['status'] == 'approved').mean() * 100
    st.metric("✅ Taxa Aprovação T1", f"{approved_rate_1:.1f}%", delta=f"{approved_rate_1-85:.1f}%")

with col4:
    failed_rate_2 = (df2['status'] == 'failed').mean() * 100 
    st.metric("❌ Taxa Falhas T2", f"{failed_rate_2:.1f}%", delta=f"-{failed_rate_2:.1f}%")

st.markdown("---")

# 🎮 Controles interativos na sidebar
st.sidebar.header("🎮 Controles do Dashboard")
st.sidebar.markdown("---")

# Seleção de dataset
dataset_option = st.sidebar.selectbox(
    "📊 Selecionar Dataset:",
    ["Ambos", "Transactions 1", "Transactions 2"]
)

# Filtros de status
st.sidebar.subheader("🔍 Filtros de Status")
all_statuses = list(set(df1['status'].unique()) | set(df2['status'].unique()))
selected_statuses = st.sidebar.multiselect(
    "Status para análise:",
    all_statuses,
    default=all_statuses
)

# Tipo de visualização
chart_type = st.sidebar.selectbox(
    "📈 Tipo de Gráfico:",
    ["Barras Interativas", "Pizza", "Sunburst", "Treemap"]
)

st.sidebar.markdown("---")
show_detailed = st.sidebar.checkbox("📋 Mostrar Análise Detalhada", value=True)

# 📊 GRÁFICOS MODERNOS E INTERATIVOS
st.header("📊 Visualizações Interativas")

# Filtrar dados pelos status selecionados
df1_filtered = df1[df1['status'].isin(selected_statuses)]
df2_filtered = df2[df2['status'].isin(selected_statuses)]

if dataset_option == "Ambos" or dataset_option == "Transactions 1":
    st.subheader("📈 Transactions 1 - Distribuição de Status")
    
    if chart_type == "Barras Interativas":
        # Gráfico de barras moderno com cores customizadas
        status_counts_1 = df1_filtered['status'].value_counts()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=status_counts_1.index,
                y=status_counts_1.values,
                marker_color=colors[:len(status_counts_1)],
                text=status_counts_1.values,
                textposition='auto',
                hovertemplate='<b>Status:</b> %{x}<br><b>Quantidade:</b> %{y}<extra></extra>'
            )
        ])
        
        fig1.update_layout(
            title={
                'text': "Distribuição de Status - Transactions 1",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title="Status da Transação",
            yaxis_title="Quantidade",
            template="plotly_white",
            showlegend=False,
            height=500
        )
        
    elif chart_type == "Pizza":
        status_counts_1 = df1_filtered['status'].value_counts()
        fig1 = px.pie(
            values=status_counts_1.values,
            names=status_counts_1.index,
            title="Distribuição de Status - Transactions 1",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
    elif chart_type == "Sunburst":
        # Criar dados hierárquicos para sunburst
        df1_sun = df1_filtered.copy()
        df1_sun['dataset'] = 'Transactions 1'
        fig1 = px.sunburst(
            df1_sun, 
            path=['dataset', 'status'], 
            title="Análise Hierárquica - Transactions 1",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    
    elif chart_type == "Treemap":
        status_counts_1 = df1_filtered['status'].value_counts()
        fig1 = px.treemap(
            names=status_counts_1.index,
            values=status_counts_1.values,
            title="Mapa de Árvore - Transactions 1",
            color=status_counts_1.values,
            color_continuous_scale="Viridis"
        )
    
    st.plotly_chart(fig1, use_container_width=True)

if dataset_option == "Ambos" or dataset_option == "Transactions 2":
    st.subheader("📈 Transactions 2 - Distribuição de Status")
    
    if chart_type == "Barras Interativas":
        status_counts_2 = df2_filtered['status'].value_counts()
        
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12', '#9b59b6', '#1abc9c', '#e74c3c']
        
        fig2 = go.Figure(data=[
            go.Bar(
                x=status_counts_2.index,
                y=status_counts_2.values,
                marker_color=colors[:len(status_counts_2)],
                text=status_counts_2.values,
                textposition='auto',
                hovertemplate='<b>Status:</b> %{x}<br><b>Quantidade:</b> %{y}<extra></extra>'
            )
        ])
        
        fig2.update_layout(
            title={
                'text': "Distribuição de Status - Transactions 2",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title="Status da Transação",
            yaxis_title="Quantidade",
            template="plotly_white",
            showlegend=False,
            height=500
        )
        
    elif chart_type == "Pizza":
        status_counts_2 = df2_filtered['status'].value_counts()
        fig2 = px.pie(
            values=status_counts_2.values,
            names=status_counts_2.index,
            title="Distribuição de Status - Transactions 2",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
    elif chart_type == "Sunburst":
        df2_sun = df2_filtered.copy()
        df2_sun['dataset'] = 'Transactions 2'
        fig2 = px.sunburst(
            df2_sun, 
            path=['dataset', 'status'], 
            title="Análise Hierárquica - Transactions 2",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
    elif chart_type == "Treemap":
        status_counts_2 = df2_filtered['status'].value_counts()
        fig2 = px.treemap(
            names=status_counts_2.index,
            values=status_counts_2.values,
            title="Mapa de Árvore - Transactions 2",
            color=status_counts_2.values,
            color_continuous_scale="Plasma"
        )
    
    st.plotly_chart(fig2, use_container_width=True)

# 📈 ANÁLISE TEMPORAL AVANÇADA
st.markdown("---")
st.header("📈 Análise Temporal de Transações")

# Reorganizar os dados usando pivot_table
try:
    df1_pivot = df1.pivot_table(index='time', columns='status', values='f0_',
                                aggfunc='sum', fill_value=0).reset_index()
    df2_pivot = df2.pivot_table(index='time', columns='status', values='count',
                                aggfunc='sum', fill_value=0).reset_index()
    
    # Criar gráficos temporais interativos
    temporal_tab1, temporal_tab2, comparison_tab = st.tabs(["📊 Transactions 1", "📊 Transactions 2", "🔄 Comparação"])
    
    with temporal_tab1:
        st.subheader("⏰ Evolução Temporal - Transactions 1")
        
        # Gráfico de linha temporal moderno
        fig_temp1 = go.Figure()
        
        status_colors = {
            'approved': '#2ecc71',
            'denied': '#e74c3c', 
            'refunded': '#f39c12',
            'reversed': '#9b59b6',
            'backend_reversed': '#34495e',
            'failed': '#c0392b'
        }
        
        for status in df1_pivot.columns[1:]:  # Skip 'time' column
            if status in df1_pivot.columns:
                fig_temp1.add_trace(go.Scatter(
                    x=df1_pivot['time'],
                    y=df1_pivot[status],
                    mode='lines+markers',
                    name=status.title(),
                    line=dict(color=status_colors.get(status, '#3498db'), width=3),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{status.title()}</b><br>Tempo: %{{x}}<br>Quantidade: %{{y}}<extra></extra>'
                ))
        
        fig_temp1.update_layout(
            title='Evolução Temporal dos Status - Transactions 1',
            xaxis_title='Horário',
            yaxis_title='Número de Transações',
            template='plotly_white',
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_temp1, use_container_width=True)
    
    with temporal_tab2:
        st.subheader("⏰ Evolução Temporal - Transactions 2")
        
        # Gráfico de linha temporal moderno
        fig_temp2 = go.Figure()
        
        for status in df2_pivot.columns[1:]:  # Skip 'time' column
            if status in df2_pivot.columns:
                fig_temp2.add_trace(go.Scatter(
                    x=df2_pivot['time'],
                    y=df2_pivot[status],
                    mode='lines+markers',
                    name=status.title(),
                    line=dict(color=status_colors.get(status, '#3498db'), width=3),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{status.title()}</b><br>Tempo: %{{x}}<br>Quantidade: %{{y}}<extra></extra>'
                ))
        
        fig_temp2.update_layout(
            title='Evolução Temporal dos Status - Transactions 2',
            xaxis_title='Horário',
            yaxis_title='Número de Transações',
            template='plotly_white',
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_temp2, use_container_width=True)
    
    with comparison_tab:
        st.subheader("🔄 Comparação entre Datasets")
        
        # Comparação side-by-side
        fig_comparison = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Transactions 1', 'Transactions 2'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Adicionar dados para transactions 1
        for status in ['approved', 'failed', 'denied']:
            if status in df1_pivot.columns:
                fig_comparison.add_trace(
                    go.Scatter(x=df1_pivot['time'], y=df1_pivot[status], 
                              name=f'T1-{status}', line=dict(color=status_colors.get(status))),
                    row=1, col=1
                )
        
        # Adicionar dados para transactions 2
        for status in ['approved', 'failed', 'denied']:
            if status in df2_pivot.columns:
                fig_comparison.add_trace(
                    go.Scatter(x=df2_pivot['time'], y=df2_pivot[status], 
                              name=f'T2-{status}', line=dict(color=status_colors.get(status), dash='dash')),
                    row=1, col=2
                )
        
        fig_comparison.update_layout(height=600, title_text="Comparação Temporal entre Datasets")
        st.plotly_chart(fig_comparison, use_container_width=True)
        
except Exception as e:
    st.error(f"Erro na análise temporal: {str(e)}")
    st.info("Verificando estrutura dos dados para análise temporal...")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Estrutura Transactions 1")
        st.write("Colunas:", df1.columns.tolist())
        st.write("Amostra:", df1.head(3))
    
    with col2:
        st.subheader("Estrutura Transactions 2") 
        st.write("Colunas:", df2.columns.tolist())
        st.write("Amostra:", df2.head(3))

# 🚨 SISTEMA INTELIGENTE DE ALERTAS E ANÁLISES
st.markdown("---")
st.header("🚨 Sistema Inteligente de Detecção de Anomalias")

# Análise automática de anomalias
def detect_anomalies(df, dataset_name):
    """Detecta anomalias automaticamente nos dados"""
    analysis = {
        'total_transactions': len(df),
        'approved_rate': (df['status'] == 'approved').mean() * 100,
        'failed_rate': (df['status'] == 'failed').mean() * 100,
        'denied_rate': (df['status'] == 'denied').mean() * 100,
        'dataset_name': dataset_name
    }
    
    # Detecção de alertas baseada em thresholds
    alerts = []
    if analysis['failed_rate'] > 10:
        alerts.append(('🔴 CRÍTICO', f"Alta taxa de falhas: {analysis['failed_rate']:.1f}%"))
    if analysis['denied_rate'] > 15:
        alerts.append(('🟡 ATENÇÃO', f"Taxa elevada de negações: {analysis['denied_rate']:.1f}%"))
    if analysis['approved_rate'] < 70:
        alerts.append(('🟠 ALERTA', f"Taxa de aprovação baixa: {analysis['approved_rate']:.1f}%"))
    
    return analysis, alerts

# Análise para ambos datasets
analysis_1, alerts_1 = detect_anomalies(df1, "Transactions 1")
analysis_2, alerts_2 = detect_anomalies(df2, "Transactions 2")

# Dashboard de alertas
alert_col1, alert_col2 = st.columns(2)

with alert_col1:
    st.subheader("🔍 Análise Transactions 1")
    
    if alerts_1:
        for level, message in alerts_1:
            if "CRÍTICO" in level:
                st.error(f"{level}: {message}")
            elif "ATENÇÃO" in level:
                st.warning(f"{level}: {message}")
            else:
                st.info(f"{level}: {message}")
    else:
        st.success("✅ Nenhuma anomalia crítica detectada")
    
    # Resumo das métricas
    st.markdown(f"""
    <div style='background-color: #34495e; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;'>
    <h5>📊 Métricas Principais:</h5>
    <ul>
    <li><strong>Total de Transações:</strong> {analysis_1['total_transactions']:,}</li>
    <li><strong>Taxa de Aprovação:</strong> {analysis_1['approved_rate']:.1f}%</li>
    <li><strong>Taxa de Falhas:</strong> {analysis_1['failed_rate']:.1f}%</li>
    <li><strong>Taxa de Negação:</strong> {analysis_1['denied_rate']:.1f}%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with alert_col2:
    st.subheader("🔍 Análise Transactions 2")
    
    if alerts_2:
        for level, message in alerts_2:
            if "CRÍTICO" in level:
                st.error(f"{level}: {message}")
            elif "ATENÇÃO" in level:
                st.warning(f"{level}: {message}")
            else:
                st.info(f"{level}: {message}")
    else:
        st.success("✅ Nenhuma anomalia crítica detectada")
    
    # Resumo das métricas
    st.markdown(f"""
    <div style='background-color: #34495e; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;'>
    <h5>📊 Métricas Principais:</h5>
    <ul>
    <li><strong>Total de Transações:</strong> {analysis_2['total_transactions']:,}</li>
    <li><strong>Taxa de Aprovação:</strong> {analysis_2['approved_rate']:.1f}%</li>
    <li><strong>Taxa de Falhas:</strong> {analysis_2['failed_rate']:.1f}%</li>
    <li><strong>Taxa de Negação:</strong> {analysis_2['denied_rate']:.1f}%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# 💡 RECOMENDAÇÕES INTELIGENTES
st.markdown("---")
st.header("💡 Recomendações Inteligentes")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.subheader("🎯 Ações Imediatas")
    
    immediate_actions = []
    if analysis_1['failed_rate'] > 10 or analysis_2['failed_rate'] > 10:
        immediate_actions.append("🔧 Verificar sistema de pagamento")
        immediate_actions.append("📞 Contatar suporte técnico")
    
    if analysis_1['denied_rate'] > 15 or analysis_2['denied_rate'] > 15:
        immediate_actions.append("🔍 Revisar regras de validação")
        immediate_actions.append("📋 Analisar logs de negação")
    
    if not immediate_actions:
        immediate_actions.append("✅ Sistema operando normalmente")
        immediate_actions.append("📊 Manter monitoramento ativo")
    
    for action in immediate_actions:
        st.markdown(f"• {action}")

with rec_col2:
    st.subheader("📈 Ações Preventivas")
    
    preventive_actions = [
        "🔄 Implementar alertas automáticos",
        "📊 Criar dashboard de monitoramento",
        "🎯 Definir SLAs para cada status",
        "🔍 Análise de tendências semanais",
        "💾 Backup automático de logs",
        "🚀 Otimização de performance"
    ]
    
    for action in preventive_actions:
        st.markdown(f"• {action}")

# 📊 COMPARAÇÃO AVANÇADA
if show_detailed:
    st.markdown("---")
    st.header("📊 Comparação Detalhada entre Datasets")
    
    # Criar gráfico de comparação
    comparison_data = {
        'Métrica': ['Taxa Aprovação', 'Taxa Falhas', 'Taxa Negação', 'Total Transações'],
        'Transactions 1': [analysis_1['approved_rate'], analysis_1['failed_rate'], 
                          analysis_1['denied_rate'], analysis_1['total_transactions']],
        'Transactions 2': [analysis_2['approved_rate'], analysis_2['failed_rate'], 
                          analysis_2['denied_rate'], analysis_2['total_transactions']]
    }
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Transactions 1',
        x=comparison_data['Métrica'][:3],  # Excluir total para esta visualização
        y=comparison_data['Transactions 1'][:3],
        marker_color='#3498db'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Transactions 2',
        x=comparison_data['Métrica'][:3],
        y=comparison_data['Transactions 2'][:3],
        marker_color='#e74c3c'
    ))
    
    fig_comparison.update_layout(
        title='Comparação de Métricas Principais (%)',
        xaxis_title='Métricas',
        yaxis_title='Porcentagem (%)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

# 📋 ANÁLISE EXPLORATÓRIA DE DADOS
if show_detailed:
    st.markdown("---")
    st.header("📋 Análise Exploratória dos Dados")
    
    data_tab1, data_tab2, stats_tab = st.tabs(["📊 Dataset 1", "📊 Dataset 2", "📈 Estatísticas"])
    
    with data_tab1:
        st.subheader("🔍 Transactions 1 - Amostra dos Dados")
        
        # Filtros interativos
        col1, col2 = st.columns([2, 1])
        with col1:
            n_rows = st.slider("Número de linhas para exibir:", 5, min(100, len(df1)), 10)
        with col2:
            show_all_cols = st.checkbox("Mostrar todas as colunas", False)
        
        if show_all_cols:
            st.dataframe(df1.head(n_rows), use_container_width=True)
        else:
            display_cols = ['time', 'status'] + [col for col in df1.columns if col not in ['time', 'status']][:3]
            st.dataframe(df1[display_cols].head(n_rows), use_container_width=True)
        
        # Informações do dataset
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Registros", len(df1))
        with col2:
            st.metric("📝 Colunas", len(df1.columns))
        with col3:
            unique_status = df1['status'].nunique()
            st.metric("🏷️ Status Únicos", unique_status)
    
    with data_tab2:
        st.subheader("🔍 Transactions 2 - Amostra dos Dados")
        
        # Filtros interativos
        col1, col2 = st.columns([2, 1])
        with col1:
            n_rows_2 = st.slider("Número de linhas para exibir:", 5, min(100, len(df2)), 10, key="rows_2")
        with col2:
            show_all_cols_2 = st.checkbox("Mostrar todas as colunas", False, key="cols_2")
        
        if show_all_cols_2:
            st.dataframe(df2.head(n_rows_2), use_container_width=True)
        else:
            display_cols_2 = ['time', 'status'] + [col for col in df2.columns if col not in ['time', 'status']][:3]
            st.dataframe(df2[display_cols_2].head(n_rows_2), use_container_width=True)
        
        # Informações do dataset
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Registros", len(df2))
        with col2:
            st.metric("📝 Colunas", len(df2.columns))
        with col3:
            unique_status_2 = df2['status'].nunique()
            st.metric("🏷️ Status Únicos", unique_status_2)
    
    with stats_tab:
        st.subheader("📈 Estatísticas Descritivas")
        
        # Análise de colunas numéricas
        numeric_cols_1 = df1.select_dtypes(include=['int64', 'float64']).columns
        numeric_cols_2 = df2.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols_1) > 0:
            st.markdown("**📊 Transactions 1 - Estatísticas Numéricas:**")
            st.dataframe(df1[numeric_cols_1].describe(), use_container_width=True)
        
        if len(numeric_cols_2) > 0:
            st.markdown("**📊 Transactions 2 - Estatísticas Numéricas:**")
            st.dataframe(df2[numeric_cols_2].describe(), use_container_width=True)
        
        # Distribuição de status
        st.markdown("---")
        st.subheader("📊 Distribuição Detalhada de Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Transactions 1:**")
            status_dist_1 = df1['status'].value_counts()
            status_df_1 = pd.DataFrame({
                'Status': status_dist_1.index,
                'Quantidade': status_dist_1.values,
                'Percentual': (status_dist_1.values / len(df1) * 100).round(2)
            })
            st.dataframe(status_df_1, use_container_width=True)
        
        with col2:
            st.markdown("**Transactions 2:**")
            status_dist_2 = df2['status'].value_counts()
            status_df_2 = pd.DataFrame({
                'Status': status_dist_2.index,
                'Quantidade': status_dist_2.values,
                'Percentual': (status_dist_2.values / len(df2) * 100).round(2)
            })
            st.dataframe(status_df_2, use_container_width=True)

# 🎯 CONCLUSÕES E INSIGHTS
st.markdown("---")
st.header("🎯 Conclusões e Insights Principais")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.subheader("🔍 Insights Transactions 1")
    
    insights_1 = [
        f"✅ **Taxa de Aprovação:** {analysis_1['approved_rate']:.1f}% - " + 
        ("Excelente" if analysis_1['approved_rate'] > 80 else "Necessita atenção"),
        
        f"⚠️ **Taxa de Falhas:** {analysis_1['failed_rate']:.1f}% - " + 
        ("Crítico" if analysis_1['failed_rate'] > 10 else "Aceitável"),
        
        f"🔄 **Volume Total:** {analysis_1['total_transactions']:,} transações",
        
        "📈 **Tendência:** " + ("Estável" if len(alerts_1) == 0 else "Requer atenção")
    ]
    
    for insight in insights_1:
        st.markdown(insight)

with insights_col2:
    st.subheader("🔍 Insights Transactions 2")
    
    insights_2 = [
        f"✅ **Taxa de Aprovação:** {analysis_2['approved_rate']:.1f}% - " + 
        ("Excelente" if analysis_2['approved_rate'] > 80 else "Necessita atenção"),
        
        f"⚠️ **Taxa de Falhas:** {analysis_2['failed_rate']:.1f}% - " + 
        ("Crítico" if analysis_2['failed_rate'] > 10 else "Aceitável"),
        
        f"🔄 **Volume Total:** {analysis_2['total_transactions']:,} transações",
        
        "📈 **Tendência:** " + ("Estável" if len(alerts_2) == 0 else "Requer atenção")
    ]
    
    for insight in insights_2:
        st.markdown(insight)

# 🚀 PRÓXIMOS PASSOS
st.markdown("---")
st.header("🚀 Próximos Passos Recomendados")

next_steps = [
    "🔄 **Automatização:** Implementar sistema de alertas em tempo real",
    "📊 **Dashboard:** Criar painel executivo com KPIs principais", 
    "🎯 **SLA:** Definir metas e thresholds para cada métrica",
    "📈 **Predição:** Desenvolver modelos de predição de anomalias",
    "🔍 **Root Cause:** Implementar análise de causa raiz automática",
    "📱 **Mobile:** Criar app mobile para alertas críticos"
]

for step in next_steps:
    st.markdown(f"• {step}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🚨 <strong>Sistema de Alertas e Incidentes</strong> | Monitoramento Inteligente de Transações</p>
    <p>Desenvolvido com ❤️ usando Streamlit e Plotly</p>
</div>
""", unsafe_allow_html=True)
