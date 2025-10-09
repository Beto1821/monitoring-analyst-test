import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os


# 🎨 Configuração dinâmica da página baseada na rota
# Obter rota atual primeiro (antes de qualquer widget)

# Função para obter query params manualmente se necessário
def get_current_route():
    try:
        query_params = st.query_params
        return query_params.get("page", "home")
    except Exception:
        return "home"


# Definir configurações por rota
route_configs = {
    "home": {
        "title": " Monitoring Analyst Test - Sistema Completo",
        "icon": "🏠"
    },
    "task1": {
        "title": " Análise Avançada de Transações",
        "icon": "📊"
    },
    "task2": {
        "title": " Sistema de Alertas e Incidentes", 
        "icon": "🚨"
    },
    "task3": {
        "title": " Central de Monitoramento Integrado",
        "icon": "📱"
    }
}

# Obter rota atual
current_route = get_current_route()
if current_route not in route_configs:
    current_route = "home"

# Configurar página com base na rota atual
config = route_configs[current_route]
st.set_page_config(
    page_title=config["title"],
    page_icon=config["icon"],
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
        background: #fafafa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        color: #333;
    }
    .task-card h3 {
        color: #667eea;
        margin-top: 0;
    }
    .task-card h4 {
        color: #444;
    }
    .task-card p {
        color: #666;
        line-height: 1.6;
    }
    .task-card ul {
        color: #555;
    }
    .task-card li {
        margin: 0.5rem 0;
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

# 🎮 Sistema de Rotas e Navegação
st.sidebar.title("🎮 Navegação")
st.sidebar.markdown("---")

# Definir rotas disponíveis (sem ícones para evitar duplicação)
routes = {
    "home": "Página Inicial",
    "task1": "Tarefa 1: Análise Avançada de Transações",
    "task2": "Tarefa 2: Sistema de Alertas e Incidentes",
    "task3": "Tarefa 3: Central de Monitoramento Integrado"
}

# Ícones para cada rota
route_icons = {
    "home": "🏠",
    "task1": "📊",
    "task2": "🚨",
    "task3": "📱"
}

# Obter rota atual dos query parameters (usando API atual)
query_params = st.query_params
current_route = query_params.get("page", "home")

# Validar rota
if current_route not in routes:
    current_route = "home"

# Sistema de navegação avançado
st.sidebar.markdown("### 🧭 Navegação por Rotas")

# Criar navegação por radio buttons (mais intuitivo)
route_options = list(routes.keys())
route_labels = list(routes.values())

# Encontrar índice da rota atual
try:
    current_index = route_options.index(current_route)
except ValueError:
    current_index = 0

# Radio button para seleção (combinando ícone + texto)
selected_index = st.sidebar.radio(
    "Selecione a página:",
    range(len(route_options)),
    format_func=lambda x: f"{route_icons[route_options[x]]} {route_labels[x]}",
    index=current_index,
    label_visibility="collapsed"
)

# Atualizar query params se mudou
if selected_index != current_index:
    st.query_params["page"] = route_options[selected_index]
    st.rerun()

st.sidebar.markdown("---")

# URLs diretas para compartilhamento
st.sidebar.markdown("### � Links Diretos")
base_url = "http://localhost:8501"  # Em produção seria a URL do deploy
st.sidebar.markdown(f"""
- [🏠 Início]({base_url}/?page=home)
- [📊 Tarefa 1]({base_url}/?page=task1) 
- [🚨 Tarefa 2]({base_url}/?page=task2)
- [📱 Tarefa 3]({base_url}/?page=task3)
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### ��📋 Informações do Sistema")
st.sidebar.info("✅ Sistema com navegação por rotas URL")

# Definir página atual baseada na rota selecionada
current_route = route_options[selected_index]


# Função para carregar módulos de forma segura
def load_task_safely(task_path, task_name):
    """Carrega uma tarefa de forma segura"""
    try:
        if os.path.exists(task_path):
            # Método mais seguro de importar
            with open(task_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Executar apenas se não houver problemas críticos
            if 'import' in code and 'st.' in code:
                # Criar ambiente local para execução
                local_vars = {
                    'st': st,
                    'pd': pd,
                    'go': go,
                    'px': px,
                    'np': np,
                    'datetime': datetime,
                    'timedelta': timedelta,
                    'make_subplots': make_subplots,
                    'os': os,
                    'sqlite3': sqlite3
                }
                exec(code, local_vars)
                return True
            else:
                st.error(f"❌ Código inválido em {task_name}")
                return False
        else:
            st.error(f"❌ Arquivo não encontrado: {task_path}")
            st.info("💡 Esta funcionalidade requer arquivos locais que podem não estar disponíveis no deploy online.")
            return False
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar {task_name}: {str(e)}")
        st.info("🔧 Esta funcionalidade requer arquivos locais. Para acesso completo, execute localmente: `streamlit run main.py`")
        return False


if current_route == "home":
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
    
    # Métricas gerais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📁 Datasets Totais", 7, delta="3 tarefas")
    with col2:
        st.metric("🔧 Tecnologias", 6, delta="Plotly, Pandas, etc")
    with col3:
        st.metric("📊 Status Sistema", "100%", delta="Todas operacionais")
    
    # Gráfico demonstrativo
    try:
        datasets_info = ["Tarefa 1", "Tarefa 2", "Tarefa 3"]
        files_count = [4, 2, 1]
        
        fig_status = px.bar(
            x=datasets_info,
            y=files_count,
            title="📊 Arquivos por Tarefa",
            color=files_count,
            color_continuous_scale="Viridis"
        )
        fig_status.update_layout(showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
        
    except Exception as e:
        st.info("📋 Gráfico não disponível no momento")
    
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
    
    # ⚠️ Aviso sobre deploy
    st.markdown("---")
    st.warning("""
    ⚠️ **IMPORTANTE**: 
    - O sistema de alertas SMS (Tarefa 3) não está funcional nesta versão de demonstração
    - Algumas funcionalidades podem estar limitadas no deploy online
    - Para funcionalidade completa, execute localmente: `streamlit run main.py`
    """)

elif current_route == "task1":
    # 📊 TAREFA 1
    st.header("📊 Análise Avançada de Transações")
    load_task_safely('Analyze_data/app.py', 'Tarefa 1')

elif current_route == "task2":
    # 🚨 TAREFA 2
    st.header("🚨 Sistema de Alertas e Incidentes")
    load_task_safely('Alert_Incident/app.py', 'Tarefa 2')

elif current_route == "task3":
    # 📱 TAREFA 3
    st.header("📱 Central de Monitoramento Integrado")
    load_task_safely('Monitoring/app.py', 'Tarefa 3')

# 📱 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 <strong>Monitoring Analyst Test</strong> | Sistema Integrado de Análise de Transações</p>
    <p>Desenvolvido com ❤️ usando Streamlit, Plotly e Python</p>
</div>
""", unsafe_allow_html=True)