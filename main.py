import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
import sys

# 🎨 Configuração da página
st.set_page_config(
    page_title="📊 Monitoring Analyst Test - Sistema Completo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📱 CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .task-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.25rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 📊 Header principal
st.markdown("""
<div class="main-header">
    <h1 style='color: white; text-align: center; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        📊 Monitoring Analyst Test
    </h1>
    <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1.3rem;'>
        Sistema Completo de Análise de Transações e Monitoramento
    </p>
</div>
""", unsafe_allow_html=True)

# 🎮 Navegação na sidebar
st.sidebar.title("🎮 Navegação")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "📱 Selecione a Tarefa:",
    [
        "🏠 Página Inicial",
        "📊 Tarefa 1: Análise Avançada de Transações", 
        "🚨 Tarefa 2: Sistema de Alertas e Incidentes",
        "📱 Tarefa 3: Central de Monitoramento Integrado"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Informações do Sistema")
st.sidebar.info("✅ Todas as aplicações integradas em uma interface única")

if page == "🏠 Página Inicial":
    # 🏠 PÁGINA INICIAL
    st.header("🏠 Bem-vindo ao Sistema de Monitoramento")
    
    st.markdown("""
    Este sistema integra **três tarefas** de análise de transações e monitoramento:
    """)
    
    # Cards das tarefas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="task-card">
            <h3>📊 Tarefa 1</h3>
            <h4>Análise Avançada de Transações</h4>
            <p><strong>Foco:</strong> Análise temporal e detecção de anomalias em checkouts</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>🔍 Detecção automática de anomalias</li>
                <li>📈 Gráficos interativos com Plotly</li>
                <li>💡 Insights inteligentes</li>
                <li>📋 Análise de causas e soluções</li>
            </ul>
            <p><strong>Tecnologias:</strong> Plotly, Pandas, SQLite</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="task-card">
            <h3>🚨 Tarefa 2</h3>
            <h4>Sistema de Alertas e Incidentes</h4>
            <p><strong>Foco:</strong> Dashboard profissional com alertas automáticos</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>🎮 Interface moderna</li>
                <li>📊 Múltiplas visualizações</li>
                <li>🚨 Alertas inteligentes</li>
                <li>📈 Análise temporal</li>
            </ul>
            <p><strong>Tecnologias:</strong> Plotly Express, Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="task-card">
            <h3>📱 Tarefa 3</h3>
            <h4>Central de Monitoramento Integrado</h4>
            <p><strong>Foco:</strong> Visão unificada de todas as tarefas</p>
            <p><strong>Características:</strong></p>
            <ul>
                <li>🔗 Integração total</li>
                <li>📊 Dashboard unificado</li>
                <li>🚨 Alertas cross-datasets</li>
                <li>📱 Sistema SMS (opcional)</li>
            </ul>
            <p><strong>Tecnologias:</strong> Integração Multi-Dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 📊 Visão geral do sistema
    st.markdown("---")
    st.header("📊 Visão Geral do Sistema")
    
    # Tentar carregar dados para métricas gerais
    try:
        # Dados básicos para demonstração
        datasets_info = {
            "Tarefa 1": {"files": 4, "status": "✅ Operacional"},
            "Tarefa 2": {"files": 2, "status": "✅ Operacional"}, 
            "Tarefa 3": {"files": 1, "status": "✅ Operacional"}
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📁 Datasets Totais", 7, delta="3 tarefas")
        with col2:
            st.metric("🔧 Tecnologias", 6, delta="Plotly, Pandas, etc")
        with col3:
            st.metric("📊 Status Sistema", "100%", delta="Todas operacionais")
        
        # Gráfico de status das tarefas
        fig_status = px.bar(
            x=list(datasets_info.keys()),
            y=[info["files"] for info in datasets_info.values()],
            title="📊 Arquivos por Tarefa",
            color=[info["files"] for info in datasets_info.values()],
            color_continuous_scale="Viridis"
        )
        fig_status.update_layout(showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
        
    except Exception as e:
        st.info("📋 Selecione uma tarefa na sidebar para começar a análise")
    
    # 🚀 Instruções de uso
    st.markdown("---")
    st.header("🚀 Como Usar")
    
    st.markdown("""
    ### 📋 Passo a Passo:
    
    1. **📱 Navegação**: Use a sidebar para selecionar a tarefa desejada
    2. **📊 Tarefa 1**: Comece com análise de transações e detecção de anomalias  
    3. **🚨 Tarefa 2**: Explore o sistema de alertas e incidentes
    4. **📱 Tarefa 3**: Veja a visão integrada de todo o sistema
    
    ### 💡 Dicas:
    - Cada tarefa é **independente** e pode ser usada separadamente
    - A **Tarefa 3** oferece visão consolidada das outras duas
    - Todos os dados são **carregados automaticamente**
    - Interface **responsiva** - funciona em desktop e mobile
    """)
    
    # ⚠️ Aviso sobre SMS
    st.markdown("---")
    st.warning("""
    ⚠️ **IMPORTANTE**: O sistema de alertas SMS (Tarefa 3) não está funcional nesta versão de demonstração, 
    pois requer configuração de serviços pagos (Twilio). A funcionalidade está implementada mas desabilitada por padrão.
    """)

elif page == "📊 Tarefa 1: Análise Avançada de Transações":
    # 📊 TAREFA 1 - Importar e executar código da Tarefa 1
    st.header("📊 Análise Avançada de Transações")
    
    try:
        # Executar código da Tarefa 1
        exec(open('Analyze_data/app.py').read())
    except FileNotFoundError:
        st.error("❌ Arquivo Analyze_data/app.py não encontrado!")
        st.info("📋 Certifique-se de que todos os arquivos estão na estrutura correta.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar Tarefa 1: {str(e)}")
        st.info("🔧 Verifique se todas as dependências estão instaladas.")

elif page == "🚨 Tarefa 2: Sistema de Alertas e Incidentes":
    # 🚨 TAREFA 2 - Importar e executar código da Tarefa 2
    st.header("🚨 Sistema de Alertas e Incidentes")
    
    try:
        # Executar código da Tarefa 2
        exec(open('Alert_Incident/app.py').read())
    except FileNotFoundError:
        st.error("❌ Arquivo Alert_Incident/app.py não encontrado!")
        st.info("📋 Certifique-se de que todos os arquivos estão na estrutura correta.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar Tarefa 2: {str(e)}")
        st.info("🔧 Verifique se todas as dependências estão instaladas.")

elif page == "📱 Tarefa 3: Central de Monitoramento Integrado":
    # 📱 TAREFA 3 - Importar e executar código da Tarefa 3
    st.header("📱 Central de Monitoramento Integrado")
    
    try:
        # Executar código da Tarefa 3
        exec(open('Monitoring/app.py').read())
    except FileNotFoundError:
        st.error("❌ Arquivo Monitoring/app.py não encontrado!")
        st.info("📋 Certifique-se de que todos os arquivos estão na estrutura correta.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar Tarefa 3: {str(e)}")
        st.info("🔧 Verifique se todas as dependências estão instaladas.")

# 📱 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 <strong>Monitoring Analyst Test</strong> | Sistema Integrado de Análise de Transações</p>
    <p>Desenvolvido com ❤️ usando Streamlit, Plotly e Python</p>
</div>
""", unsafe_allow_html=True)