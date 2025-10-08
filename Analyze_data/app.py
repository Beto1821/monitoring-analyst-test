import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import os

# Disable warning for st.pyplot() - option deprecated in newer Streamlit versions
# st.set_option('deprecation.showPyplotGlobalUse', False)

# Função para detectar o caminho correto dos dados
def get_data_path(filename):
    """Detecta o caminho correto dos arquivos de dados"""
    # Primeiro, tenta o caminho relativo atual
    if os.path.exists(filename):
        return filename
    
    # Se executado a partir do main.py, ajusta o caminho
    analyze_path = os.path.join("Analyze_data", filename)
    if os.path.exists(analyze_path):
        return analyze_path
    
    # Caminho absoluto como fallback
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(current_dir, filename)
    if os.path.exists(abs_path):
        return abs_path
    
    # Se nada funcionar, retorna o caminho original para mostrar o erro
    return filename

# Load CSV files
df1 = pd.read_csv(get_data_path("data/checkout_1.csv"))
df2 = pd.read_csv(get_data_path("data/checkout_2.csv"))
df3 = pd.read_csv(get_data_path("data/transactions_1.csv"))
df4 = pd.read_csv(get_data_path("data/transactions_2.csv"))

# Create SQLite database connections
conn1 = sqlite3.connect(get_data_path('data1.db'))
df1.to_sql('data_table', conn1, if_exists='replace', index=False)

conn2 = sqlite3.connect(get_data_path('data2.db'))
df2.to_sql('data_table', conn2, if_exists='replace', index=False)

# Define SQL queries
query1 = "SELECT time, today, yesterday, same_day_last_week, " \
         "avg_last_week, avg_last_month FROM data_table"

query2 = "SELECT time, today, yesterday, same_day_last_week, " \
         "avg_last_week, avg_last_month FROM data_table"

# Execute SQL queries
results_df1 = pd.read_sql_query(query1, conn1)
results_df2 = pd.read_sql_query(query2, conn2)

# Close database connections
conn1.close()
conn2.close()

# Converter time para formato numérico para cálculos
results_df1['time_numeric'] = results_df1['time'].str.replace('h', '').astype(int)
results_df2['time_numeric'] = results_df2['time'].str.replace('h', '').astype(int)

# 🎨 CONFIGURAÇÃO DO LAYOUT
st.set_page_config(
    page_title="📊 Análise de Transações",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎯 TÍTULO PRINCIPAL
st.title("📊 Análise Avançada de Transações")
st.markdown("---")

# 🎛️ SIDEBAR PARA CONTROLES
st.sidebar.header("🎛️ Controles de Visualização")
st.sidebar.markdown("---")

# Controles do Checkout 1
st.sidebar.subheader("✅ Checkout 1 (Normal)")
show_today_1 = st.sidebar.checkbox("📈 Hoje", value=True, key="today1")
show_yesterday_1 = st.sidebar.checkbox("📊 Ontem", value=True, key="yesterday1")
show_same_day_last_week_1 = st.sidebar.checkbox("📅 Mesmo Dia Semana Passada", value=True, key="week1")

st.sidebar.markdown("---")

# Controles do Checkout 2
st.sidebar.subheader("🚨 Checkout 2 (Anomalia)")
show_today_2 = st.sidebar.checkbox("📈 Hoje", value=True, key="today2")
show_yesterday_2 = st.sidebar.checkbox("📊 Ontem", value=True, key="yesterday2")
show_same_day_last_week_2 = st.sidebar.checkbox("📅 Mesmo Dia Semana Passada", value=True, key="week2")

st.sidebar.markdown("---")

# Controles de Médias
st.sidebar.subheader("📊 Médias Históricas")
show_avg_last_week = st.sidebar.checkbox("📊 Média Semana Passada", value=True, key="avg_week")
show_avg_last_month = st.sidebar.checkbox("📆 Média Mês Passado", value=True, key="avg_month")

# Opções de visualização
st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Opções de Visualização")
chart_theme = st.sidebar.selectbox("🎨 Tema do Gráfico", ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"])
show_grid = st.sidebar.checkbox("📐 Mostrar Grade", value=True)
show_markers = st.sidebar.checkbox("🔵 Mostrar Marcadores", value=True)

# 📊 GRÁFICO PRINCIPAL INTERATIVO
st.subheader("📈 Comparação Temporal de Transações")

# Criar gráfico principal com Plotly
fig_main = go.Figure()

# Cores personalizadas e estilos
colors_checkout1 = {
    'today': '#FF6B6B',      # Vermelho vibrante
    'yesterday': '#4ECDC4',   # Turquesa
    'week': '#45B7D1'        # Azul claro
}

colors_checkout2 = {
    'today': '#FFA726',      # Laranja
    'yesterday': '#AB47BC',   # Roxo
    'week': '#66BB6A'        # Verde
}

# Checkout 1 - Linhas
if show_today_1:
    fig_main.add_trace(go.Scatter(
        x=results_df1['time_numeric'],
        y=results_df1['today'],
        mode='lines+markers' if show_markers else 'lines',
        name='🔴 Hoje (Checkout 1)',
        line=dict(color=colors_checkout1['today'], width=3, dash='solid'),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='<b>Checkout 1 - Hoje</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

if show_yesterday_1:
    fig_main.add_trace(go.Scatter(
        x=results_df1['time_numeric'],
        y=results_df1['yesterday'],
        mode='lines+markers' if show_markers else 'lines',
        name='🔵 Ontem (Checkout 1)',
        line=dict(color=colors_checkout1['yesterday'], width=3, dash='dot'),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>Checkout 1 - Ontem</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

if show_same_day_last_week_1:
    fig_main.add_trace(go.Scatter(
        x=results_df1['time_numeric'],
        y=results_df1['same_day_last_week'],
        mode='lines+markers' if show_markers else 'lines',
        name='📅 Semana Passada (Checkout 1)',
        line=dict(color=colors_checkout1['week'], width=3, dash='dashdot'),
        marker=dict(size=8, symbol='square'),
        hovertemplate='<b>Checkout 1 - Semana Passada</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

# Checkout 2 - Linhas
if show_today_2:
    fig_main.add_trace(go.Scatter(
        x=results_df2['time_numeric'],
        y=results_df2['today'],
        mode='lines+markers' if show_markers else 'lines',
        name='🟠 Hoje (Checkout 2)',
        line=dict(color=colors_checkout2['today'], width=3, dash='solid'),
        marker=dict(size=8, symbol='triangle-up'),
        hovertemplate='<b>Checkout 2 - Hoje ⚠️</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

if show_yesterday_2:
    fig_main.add_trace(go.Scatter(
        x=results_df2['time_numeric'],
        y=results_df2['yesterday'],
        mode='lines+markers' if show_markers else 'lines',
        name='🟣 Ontem (Checkout 2)',
        line=dict(color=colors_checkout2['yesterday'], width=3, dash='dot'),
        marker=dict(size=8, symbol='triangle-down'),
        hovertemplate='<b>Checkout 2 - Ontem</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

if show_same_day_last_week_2:
    fig_main.add_trace(go.Scatter(
        x=results_df2['time_numeric'],
        y=results_df2['same_day_last_week'],
        mode='lines+markers' if show_markers else 'lines',
        name='🟢 Semana Passada (Checkout 2)',
        line=dict(color=colors_checkout2['week'], width=3, dash='dashdot'),
        marker=dict(size=8, symbol='star'),
        hovertemplate='<b>Checkout 2 - Semana Passada</b><br>' +
                      'Hora: %{x}h<br>' +
                      'Transações: %{y}<br>' +
                      '<extra></extra>'
    ))

# Destacar zona de anomalia no Checkout 2
if show_today_2:
    fig_main.add_vrect(
        x0=13, x1=19,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0,
    )
    fig_main.add_annotation(
        x=16, y=max(results_df2['today']) * 0.8,
        text="🚨 ZONA DE ANOMALIA<br>Checkout 2",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="red",
        borderwidth=2
    )

# Configuração do layout
fig_main.update_layout(
    title={
        'text': "📊 Análise Comparativa de Transações por Hora",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    xaxis_title="⏰ Horário do Dia",
    yaxis_title="📈 Número de Transações",
    template=chart_theme,
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    height=600,
    xaxis=dict(
        showgrid=show_grid,
        gridwidth=1,
        gridcolor='lightgray',
        tickmode='linear',
        tick0=0,
        dtick=2,
        ticksuffix='h'
    ),
    yaxis=dict(
        showgrid=show_grid,
        gridwidth=1,
        gridcolor='lightgray'
    )
)

st.plotly_chart(fig_main, use_container_width=True)

# 📊 GRÁFICO DE MÉDIAS HISTÓRICAS
if show_avg_last_week or show_avg_last_month:
    st.markdown("---")
    st.subheader("📊 Análise de Médias Históricas")
    
    # Criar gráfico de médias com subplots
    fig_avg = make_subplots(
        rows=2, cols=1,
        subplot_titles=('✅ Checkout 1 - Médias Históricas', '🚨 Checkout 2 - Médias Históricas'),
        vertical_spacing=0.1,
        shared_xaxes=True
    )
    
    colors_avg = {
        'week1': '#2E86AB',
        'month1': '#A23B72',
        'week2': '#F18F01',
        'month2': '#C73E1D'
    }
    
    # Checkout 1 - Médias
    if show_avg_last_week:
        fig_avg.add_trace(
            go.Scatter(
                x=results_df1['time_numeric'],
                y=results_df1['avg_last_week'],
                mode='lines+markers' if show_markers else 'lines',
                name='📊 Média Semana (C1)',
                line=dict(color=colors_avg['week1'], width=3),
                marker=dict(size=6, symbol='circle'),
                hovertemplate='<b>Checkout 1 - Média Semanal</b><br>' +
                              'Hora: %{x}h<br>' +
                              'Transações: %{y}<br>' +
                              '<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig_avg.add_trace(
            go.Scatter(
                x=results_df2['time_numeric'],
                y=results_df2['avg_last_week'],
                mode='lines+markers' if show_markers else 'lines',
                name='📊 Média Semana (C2)',
                line=dict(color=colors_avg['week2'], width=3),
                marker=dict(size=6, symbol='triangle-up'),
                hovertemplate='<b>Checkout 2 - Média Semanal</b><br>' +
                              'Hora: %{x}h<br>' +
                              'Transações: %{y}<br>' +
                              '<extra></extra>'
            ),
            row=2, col=1
        )
    
    if show_avg_last_month:
        fig_avg.add_trace(
            go.Scatter(
                x=results_df1['time_numeric'],
                y=results_df1['avg_last_month'],
                mode='lines+markers' if show_markers else 'lines',
                name='📆 Média Mensal (C1)',
                line=dict(color=colors_avg['month1'], width=3, dash='dot'),
                marker=dict(size=6, symbol='diamond'),
                hovertemplate='<b>Checkout 1 - Média Mensal</b><br>' +
                              'Hora: %{x}h<br>' +
                              'Transações: %{y}<br>' +
                              '<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig_avg.add_trace(
            go.Scatter(
                x=results_df2['time_numeric'],
                y=results_df2['avg_last_month'],
                mode='lines+markers' if show_markers else 'lines',
                name='📆 Média Mensal (C2)',
                line=dict(color=colors_avg['month2'], width=3, dash='dot'),
                marker=dict(size=6, symbol='star'),
                hovertemplate='<b>Checkout 2 - Média Mensal</b><br>' +
                              'Hora: %{x}h<br>' +
                              'Transações: %{y}<br>' +
                              '<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Configurações do layout
    fig_avg.update_layout(
        title={
            'text': "📈 Comparativo de Médias Históricas por Checkout",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        template=chart_theme,
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Configurar eixos
    fig_avg.update_xaxes(
        title_text="⏰ Horário do Dia",
        showgrid=show_grid,
        gridwidth=1,
        gridcolor='lightgray',
        tickmode='linear',
        tick0=0,
        dtick=2,
        ticksuffix='h',
        row=2, col=1
    )
    
    fig_avg.update_yaxes(
        title_text="📈 Transações",
        showgrid=show_grid,
        gridwidth=1,
        gridcolor='lightgray'
    )
    
    st.plotly_chart(fig_avg, use_container_width=True)

# 📊 DASHBOARD DE MÉTRICAS RÁPIDAS
st.markdown("---")
st.subheader("⚡ Dashboard de Métricas Rápidas")

col1, col2, col3, col4 = st.columns(4)

# Calcular estatísticas
checkout1_today_total = results_df1['today'].sum()
checkout2_today_total = results_df2['today'].sum()
checkout1_max_hour = results_df1.loc[results_df1['today'].idxmax(), 'time']
checkout2_max_hour = results_df2.loc[results_df2['today'].idxmax(), 'time']

with col1:
    st.metric(
        label="🛒 Total Checkout 1",
        value=f"{checkout1_today_total:,.0f}",
        delta="Normal"
    )

with col2:
    st.metric(
        label="🛒 Total Checkout 2",
        value=f"{checkout2_today_total:,.0f}",
        delta=f"{checkout2_today_total - checkout1_today_total:+.0f}"
    )

with col3:
    st.metric(
        label="⏰ Pico Checkout 1",
        value=f"{checkout1_max_hour}h",
        delta="Horário normal"
    )

with col4:
    st.metric(
        label="⏰ Pico Checkout 2",
        value=f"{checkout2_max_hour}h",
        delta="Verificar anomalia"
    )

# 🔥 HEATMAP DE COMPARAÇÃO
st.markdown("---")
st.subheader("🔥 Heatmap de Performance por Horário")

# Preparar dados para heatmap
heatmap_data = pd.DataFrame({
    'Horário': results_df1['time_numeric'],
    'Checkout 1 - Hoje': results_df1['today'],
    'Checkout 1 - Ontem': results_df1['yesterday'],
    'Checkout 1 - Semana': results_df1['same_day_last_week'],
    'Checkout 2 - Hoje': results_df2['today'],
    'Checkout 2 - Ontem': results_df2['yesterday'],
    'Checkout 2 - Semana': results_df2['same_day_last_week']
})

# Transpor para ter horários nas colunas
heatmap_matrix = heatmap_data.set_index('Horário').T

# Criar heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_matrix.values,
    x=[f"{int(h)}h" for h in heatmap_matrix.columns],
    y=heatmap_matrix.index,
    colorscale='RdYlGn',
    showscale=True,
    hovertemplate='<b>%{y}</b><br>' +
                  'Horário: %{x}<br>' +
                  'Transações: %{z}<br>' +
                  '<extra></extra>',
    colorbar=dict(
        title="Transações",
        titleside="right"
    )
))

fig_heatmap.update_layout(
    title={
        'text': "🔥 Mapa de Calor - Performance por Período e Horário",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16}
    },
    template=chart_theme,
    height=400,
    xaxis_title="⏰ Horário do Dia",
    yaxis_title="📊 Período/Checkout"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 📈 GRÁFICO DE ÁREA COMPARATIVO
st.markdown("---")
st.subheader("📈 Análise de Área - Distribuição de Transações")

fig_area = go.Figure()

# Adicionar áreas empilhadas
fig_area.add_trace(go.Scatter(
    x=results_df1['time_numeric'],
    y=results_df1['today'],
    fill='tonexty',
    mode='lines',
    name='✅ Checkout 1',
    line=dict(color='rgba(0, 100, 80, 0.7)', width=2),
    fillcolor='rgba(0, 100, 80, 0.3)'
))

fig_area.add_trace(go.Scatter(
    x=results_df2['time_numeric'],
    y=results_df2['today'],
    fill='tonexty',
    mode='lines',
    name='🚨 Checkout 2',
    line=dict(color='rgba(255, 0, 0, 0.7)', width=2),
    fillcolor='rgba(255, 0, 0, 0.3)'
))

fig_area.update_layout(
    title={
        'text': "📊 Distribuição Comparativa de Transações (Hoje)",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16}
    },
    template=chart_theme,
    height=400,
    xaxis_title="⏰ Horário do Dia",
    yaxis_title="📈 Número de Transações",
    hovermode='x unified',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=2,
        ticksuffix='h'
    )
)

st.plotly_chart(fig_area, use_container_width=True)

# 📊 ANÁLISE DETALHADA DOS GRÁFICOS
st.markdown("---")
st.header("📊 Análise Detalhada das Transações")

# Análise do Checkout 1
st.subheader("✅ Checkout 1 - Status: Normal")
st.markdown("""
<div style='background-color: #d4edda; padding: 15px; border-radius: 5px; border-left: 5px solid #28a745;'>
<h4 style='color: #155724; margin-top: 0;'>📈 Comportamento Identificado:</h4>
<ul style='color: #155724;'>
<li><strong>Padrão Consistente:</strong> Transações seguem tendência similar entre hoje, ontem e mesmo dia da semana passada</li>
<li><strong>Picos Esperados:</strong> Horários de maior movimento (9h-12h e 14h-18h) condizem com padrão comercial</li>
<li><strong>Variação Normal:</strong> Flutuações dentro da margem esperada para operação saudável</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Análise do Checkout 2
st.subheader("🚨 Checkout 2 - Status: Anomalia Detectada")
st.markdown("""
<div style='background-color: #f8d7da; padding: 15px; border-radius: 5px; border-left: 5px solid #dc3545;'>
<h4 style='color: #721c24; margin-top: 0;'>⚠️ Problema Identificado:</h4>
<ul style='color: #721c24;'>
<li><strong>Queda Crítica:</strong> Redução drástica entre 13h-19h</li>
<li><strong>Interrupção Total:</strong> Zero transações no período 15h-17h</li>
<li><strong>Recuperação Parcial:</strong> Retomada gradual após 17h, mas abaixo do esperado</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Possíveis Causas
st.subheader("🔍 Possíveis Causas da Anomalia (Checkout 2)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background-color: #fff3cd; padding: 10px; border-radius: 5px;'>
    <h5 style='color: #856404;'>🔧 Causas Técnicas:</h5>
    <ul style='color: #856404; font-size: 14px;'>
    <li>Falha no sistema de pagamento</li>
    <li>Problemas de conectividade</li>
    <li>Manutenção não programada</li>
    <li>Sobrecarga do servidor</li>
    <li>Erro no software do checkout</li>
    <li>Problemas na rede interna</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background-color: #e7e7ff; padding: 10px; border-radius: 5px;'>
    <h5 style='color: #383874;'>👥 Causas Operacionais:</h5>
    <ul style='color: #383874; font-size: 14px;'>
    <li>Fechamento temporário do terminal</li>
    <li>Treinamento de funcionários</li>
    <li>Problema físico no checkout</li>
    <li>Falta de operador no período</li>
    <li>Manutenção preventiva</li>
    <li>Reorganização do layout</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Soluções Recomendadas
st.subheader("💡 Soluções Recomendadas")

st.markdown("""
<div style='background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 5px solid #17a2b8;'>
<h4 style='color: #0c5460; margin-top: 0;'>🎯 Ações Imediatas:</h4>
<ol style='color: #0c5460;'>
<li><strong>Verificação Técnica:</strong> Diagnóstico completo do hardware e software do Checkout 2</li>
<li><strong>Teste de Conectividade:</strong> Validar conexão com servidor central e gateway de pagamento</li>
<li><strong>Log de Eventos:</strong> Analisar logs do sistema para identificar erros específicos</li>
<li><strong>Backup Operacional:</strong> Ativar checkout reserva durante investigação</li>
</ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #e2e3e5; padding: 15px; border-radius: 5px; border-left: 5px solid #6c757d;'>
<h4 style='color: #495057; margin-top: 0;'>📋 Ações Preventivas:</h4>
<ul style='color: #495057;'>
<li><strong>Monitoramento Contínuo:</strong> Alertas automáticos para quedas de performance</li>
<li><strong>Redundância:</strong> Sistema de backup automático entre checkouts</li>
<li><strong>Manutenção Programada:</strong> Cronograma regular fora do horário comercial</li>
<li><strong>Treinamento:</strong> Capacitação da equipe para resolução rápida de problemas</li>
<li><strong>SLA:</strong> Definir tempo máximo de inatividade aceitável</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Métricas de Impacto
st.subheader("📉 Impacto da Anomalia")

# Calcular algumas métricas básicas de impacto
total_expected = results_df1['today'].sum()  # Usando checkout 1 como baseline
total_actual_checkout2 = results_df2['today'].sum()
loss_percentage = ((total_expected - total_actual_checkout2) / total_expected) * 100

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        label="📊 Transações Perdidas",
        value=f"{int(total_expected - total_actual_checkout2)}", 
        delta=f"-{loss_percentage:.1f}%"
    )

with col4:
    st.metric(
        label="⏰ Período Crítico", 
        value="15h-17h",
        delta="Zero transações"
    )

with col5:
    st.metric(
        label="🎯 Prioridade",
        value="ALTA",
        delta="Ação imediata"
    )

# Display the DataFrames using Streamlit
st.subheader("Checkout 1 Data")
st.dataframe(df1, width=2200)

st.subheader("Checkout 2 Data")
st.dataframe(df2, width=2200)
