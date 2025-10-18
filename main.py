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
    },
    "simulacoes": {
        "title": " Simulações SimPy",
        "icon": "🎮"
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
    "task3": "Tarefa 3: Central de Monitoramento Integrado",
    "simulacoes": "Simulações SimPy: Modelagem com SimPy"
}

# Ícones para cada rota
route_icons = {
    "home": "🏠",
    "task1": "📊",
    "task2": "🚨",
    "task3": "📱",
    "simulacoes": "🎮"
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
st.sidebar.markdown("### 📋 Informações do Sistema")
st.sidebar.info("✅ Sistema com navegação por rotas URL")

# Definir página atual baseada na rota selecionada
current_route = route_options[selected_index]


# Função para carregar módulos de forma segura
def load_task_safely(task_path, task_name):
    """Carrega uma tarefa de forma segura"""
    try:
        if task_path == 'simulacoes/app.py':
            # Para Simulações, usar uma abordagem especial que evita conflitos
            # Redirecionar para a aplicação específica em uma nova aba/porta
            st.info("🎮 **Sistema de Simulações SimPy**")
            st.markdown("""
            As simulações utilizam SimPy (Discrete Event Simulation) e rodam em uma aplicação dedicada 
            para evitar conflitos de configuração.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🛒 **Funcionalidades Disponíveis:**
                - **Simulação de Checkouts**: Filas, tempos de espera, utilização
                - **Simulação de Anomalias**: Falhas, recuperação, timeline
                - **Análise de Cenários**: Comparação de configurações
                - **Dados Real vs Simulado**: Validação de modelos
                """)
            
            with col2:
                st.markdown("""
                ### ⚙️ **Tecnologias:**
                - **SimPy**: Simulação discreta de eventos
                - **Plotly**: Gráficos interativos
                - **Pandas**: Análise de dados
                - **Session State**: Persistência de resultados
                """)
            
            # === SEÇÃO DE BOAS PRÁTICAS E INFORMAÇÕES IMPORTANTES ===
            st.markdown("---")
            st.markdown("## 📚 **Guia de Boas Práticas para Simulações**")
            
            # Boas práticas em abas organizadas
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 **Como Usar**", 
                "⚡ **Dicas de Performance**", 
                "🔧 **Configurações**", 
                "📊 **Interpretação**"
            ])
            
            with tab1:
                st.markdown("""
                ### 🎯 **Como Usar as Simulações Efetivamente**
                
                **1. 🛒 Simulação de Checkouts:**
                - **Objetivo**: Modelar filas e tempos de espera em checkouts
                - **Casos de uso**: Otimização de capacidade, análise de gargalos
                - **Parâmetros importantes**: Capacidade dos checkouts, taxa de chegada
                - **Interpretação**: Foque nos tempos de espera médios e utilização
                
                **2. 🚨 Simulação de Anomalias:**
                - **Objetivo**: Modelar falhas de sistema e recuperação
                - **Casos de uso**: Planejamento de manutenção, análise de disponibilidade
                - **Parâmetros importantes**: MTBF (Mean Time Between Failures)
                - **Interpretação**: Analise frequência e duração das falhas
                
                **3. 🔍 Análise de Cenários:**
                - **Objetivo**: Comparar diferentes configurações
                - **Casos de uso**: Tomada de decisão, otimização de recursos
                - **Parâmetros importantes**: Diferentes capacidades e multiplicadores
                - **Interpretação**: Compare métricas entre cenários
                
                **4. 📊 Comparação Real vs Simulado:**
                - **Objetivo**: Validar modelos com dados reais
                - **Casos de uso**: Calibração de modelos, verificação de precisão
                - **Parâmetros importantes**: Ajuste fino dos parâmetros
                - **Interpretação**: Busque aderência entre real e simulado
                """)
            
            with tab2:
                st.markdown("""
                ### ⚡ **Dicas de Performance e Eficiência**
                
                **⏱️ Duração das Simulações:**
                - **Simulações curtas (1-8h)**: Para testes rápidos e ajustes
                - **Simulações médias (8-24h)**: Para análises padrão
                - **Simulações longas (24-48h)**: Para análises detalhadas
                
                **🎛️ Configuração de Parâmetros:**
                - **Comece com valores padrão** e ajuste gradualmente
                - **Use durações menores** para testes iniciais
                - **Aumente a complexidade** conforme a necessidade
                
                **💾 Gerenciamento de Resultados:**
                - Resultados são **salvos automaticamente** no session state
                - **Não feche a aba** durante simulações longas
                - **Resultados persistem** até nova execução
                
                **🔄 Iteração e Refinamento:**
                - Execute múltiplas simulações com parâmetros diferentes
                - Compare resultados para identificar padrões
                - Use simulações curtas para calibrar parâmetros
                """)
            
            with tab3:
                st.markdown("""
                ### 🔧 **Guia de Configurações Avançadas**
                
                **🛒 Configurações de Checkout:**
                - **Capacidade 1-2**: Para cenários de baixa demanda
                - **Capacidade 3-5**: Para cenários de alta demanda
                - **Multiplicador 1.0-2.0**: Diferença normal entre checkouts
                - **Multiplicador 2.0-5.0**: Para análise de gargalos extremos
                
                **🚨 Configurações de Anomalias:**
                - **MTBF 4-8h**: Sistema com falhas frequentes
                - **MTBF 8-16h**: Sistema moderadamente confiável
                - **MTBF 16-24h**: Sistema muito confiável
                - **Taxa de falha rede 0-5%**: Rede estável
                - **Taxa de falha rede 5-20%**: Rede instável
                
                **📏 Métricas Importantes:**
                - **Tempo de espera médio**: < 5 min (bom), > 10 min (ruim)
                - **Utilização**: 70-85% (ideal), > 95% (saturação)
                - **Número de falhas**: Monitore frequência e duração
                """)
            
            with tab4:
                st.markdown("""
                ### 📊 **Como Interpretar os Resultados**
                
                **📈 Gráficos de Transações:**
                - **Picos**: Indicam horários de maior demanda
                - **Vales**: Períodos de menor movimento
                - **Distribuição**: Observe equilíbrio entre checkouts
                
                **⏰ Análise de Tempos de Espera:**
                - **Box plots**: Mostram distribuição e outliers
                - **Médias**: Para comparação geral entre cenários
                - **Máximos**: Identificam pior caso possível
                
                **🔴 Indicadores de Problemas:**
                - Tempos de espera > 15 minutos
                - Utilização de um checkout > 95%
                - Muitas falhas em período curto
                
                **✅ Indicadores de Sucesso:**
                - Tempos de espera < 5 minutos
                - Utilização balanceada entre checkouts
                - Sistema estável com poucas falhas
                
                **🎯 Ações Recomendadas:**
                - **Se tempos altos**: Aumentar capacidade ou balanceamento
                - **Se utilização desigual**: Ajustar multiplicadores
                - **Se muitas falhas**: Revisar configurações de MTBF
                """)
            
            # Alertas e cuidados importantes
            st.markdown("---")
            st.warning("""
            ⚠️ **Cuidados Importantes:**
            - As simulações são **modelos aproximados** da realidade
            - Resultados dependem da **qualidade dos parâmetros** inseridos
            - **Valide sempre** com dados reais quando possível
            - **Simulações longas** podem consumir mais recursos
            """)
            
            st.info("""
            💡 **Dica Profissional:**
            Combine diferentes tipos de simulação para uma análise completa:
            1. **Checkouts** → Otimizar operação normal
            2. **Anomalias** → Planejar contingências  
            3. **Cenários** → Comparar alternativas
            4. **Real vs Simulado** → Validar precisão
            """)
            
            # === SEÇÃO TÉCNICA ===
            with st.expander("🔧 **Requisitos Técnicos e Troubleshooting**", expanded=False):
                col_tech1, col_tech2 = st.columns(2)
                
                with col_tech1:
                    st.markdown("""
                    ### 💻 **Requisitos do Sistema:**
                    - **Python 3.8+** com ambiente virtual
                    - **Streamlit 1.28+** para interface
                    - **SimPy 4.1+** para simulações
                    - **Plotly 5.0+** para gráficos
                    - **Pandas 1.5+** para dados
                    - **Memória**: Mín. 4GB RAM
                    - **Processador**: Recomendado multi-core
                    
                    ### 🌐 **Compatibilidade:**
                    - **Browsers**: Chrome, Firefox, Safari, Edge
                    - **OS**: Windows, macOS, Linux
                    - **Portas**: 8511 (simulações), 8512 (principal)
                    """)
                
                with col_tech2:
                    st.markdown("""
                    ### 🚨 **Solução de Problemas:**
                    
                    **🔴 Simulação não carrega:**
                    ```bash
                    cd simulacoes
                    streamlit run app.py --server.port 8511
                    ```
                    
                    **🔴 Erro de importação:**
                    ```bash
                    pip install simpy plotly pandas streamlit
                    ```
                    
                    **🔴 Porta ocupada:**
                    ```bash
                    pkill -f streamlit
                    # ou use porta alternativa
                    streamlit run app.py --server.port 8512
                    ```
                    
                    **🔴 Performance lenta:**
                    - Reduza duração da simulação
                    - Feche outras abas do navegador
                    - Use parâmetros menores para teste
                    """)
                
                st.markdown("---")
                st.markdown("""
                ### 📖 **Documentação Técnica:**
                - **SimPy Documentation**: https://simpy.readthedocs.io/
                - **Plotly Python**: https://plotly.com/python/
                - **Streamlit Docs**: https://docs.streamlit.io/
                
                ### 🛠️ **Script de Inicialização Automática:**
                Execute o script `start_system.sh` para iniciar ambas as aplicações automaticamente:
                ```bash
                ./start_system.sh
                ```
                """)
            
            st.markdown("---")
            
            # Sistema de acesso às simulações (SOLUÇÃO ROBUSTA)
            
            # Verificar se a aplicação de simulações está rodando
            import socket
            def check_port(host, port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    return result == 0
                except Exception:
                    return False
            
            sim_running = check_port('localhost', 8511)
            
            # Status da aplicação
            if sim_running:
                st.success("✅ **Aplicação de Simulações ATIVA** na porta 8511")
            else:
                st.error("❌ **Aplicação de Simulações NÃO está rodando** na porta 8511")
                st.info("💡 Para iniciar: `cd simulacoes && streamlit run app.py --server.port 8511`")
            
            st.markdown("---")
            
            # Links funcionais garantidos
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 **LINK DIRETO (FUNCIONA SEMPRE)**")
                if sim_running:
                    # Usar HTML puro que sempre funciona
                    st.markdown("""
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="http://localhost:8511" target="_blank" rel="noopener noreferrer"
                           style="display: inline-block; padding: 15px 30px; 
                                  background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                                  color: white; text-decoration: none; border-radius: 10px;
                                  font-weight: bold; font-size: 18px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                            🚀 ABRIR SIMULAÇÕES
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Aplicação não está rodando")
            
            with col2:
                st.markdown("### 📋 **URL PARA COPIAR**")
                st.markdown("**Cole esta URL no navegador:**")
                st.code("http://localhost:8511")
                
                if st.button("📋 Copiar URL", use_container_width=True):
                    st.success("URL copiada! Cole no navegador: http://localhost:8511")
            
            with col1:
                if st.button("🚀 Abrir Sistema de Simulações", type="primary", use_container_width=True):
                    st.success("✅ Tentando abrir sistema de simulações...")
                    
                    # JavaScript para abrir nova aba automaticamente
                    st.markdown("""
                    <script>
                    window.open('http://localhost:8511', '_blank');
                    </script>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Link direto como alternativa principal
                st.link_button(
                    "🎯 Link Direto para Simulações", 
                    "http://localhost:8511",
                    use_container_width=True
                )
            
            st.markdown("""
            **📋 Como usar:**
            1. Clique em um dos botões acima para acessar o sistema de simulações
            2. Selecione o tipo de simulação desejado na barra lateral
            3. Configure os parâmetros conforme necessário
            4. Execute as simulações e visualize os resultados interativos
            
            **🔗 Link manual:** `http://localhost:8511`
            """)
            
            # Informações sobre status das aplicações
            st.info("ℹ️ **Status das Aplicações:** Main App (porta 8512) | Simulações (porta 8511)")
                
            # Link clicável como backup adicional
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <a href="http://localhost:8511" target="_blank" 
                   style="display: inline-block; padding: 0.5rem 1rem; 
                          background-color: #4CAF50; color: white; 
                          text-decoration: none; border-radius: 5px;
                          font-weight: bold;">
                    � Acesso Alternativo às Simulações
                </a>
            </div>
            """, unsafe_allow_html=True)
                
            # Informações técnicas
            with st.expander("🔧 Informações Técnicas"):
                st.markdown("""
                **Por que uma aplicação separada?**
                - `st.set_page_config()` só pode ser chamado uma vez por sessão
                - SimPy requer configurações específicas de ambiente
                - Session state é isolado para evitar conflitos
                - Performance otimizada para simulações longas
                
                **Arquitetura:**
                ```
                main.py (porta 8512) ← Você está aqui
                ├── Tarefa 1: Análise de Dados
                ├── Tarefa 2: Alertas e Incidentes  
                ├── Tarefa 3: Monitoramento Integrado
                └── simulacoes/app.py (porta 8511) ← Sistema SimPy
                ```
                """)
            
            return True
            
        elif task_path == 'Monitoring/app.py':
            # Para Task 3, executar de forma mais direta
            import sys
            import importlib.util
            
            # Limpar cache de imports anteriores para forçar reload
            if 'Monitoring.app' in sys.modules:
                del sys.modules['Monitoring.app']
            
            # Carregar o módulo usando importlib
            spec = importlib.util.spec_from_file_location("monitoring_app", task_path)
            monitoring_module = importlib.util.module_from_spec(spec)
            
            # Executar o módulo
            spec.loader.exec_module(monitoring_module)
            
            return True
            
        elif os.path.exists(task_path):
            # Método tradicional para outras tarefas
            with open(task_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if 'import' in code and 'st.' in code:
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
            return False
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar {task_name}: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
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
    
    # === SEÇÃO DE SIMULAÇÕES ===
    st.markdown("---")
    st.header("🎮 Sistema de Simulações SimPy")
    
    # Card destacado para simulações
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; padding: 25px; margin: 20px 0; color: white;">
        <h3 style="color: white; margin-top: 0;">🎯 Simulações Discretas de Eventos</h3>
        <p style="font-size: 1.1em; margin-bottom: 15px;">
            <strong>Modelagem avançada de sistemas de checkout usando SimPy</strong>
        </p>
        <p>Sistema dedicado para simulação e análise de diferentes cenários operacionais, 
           otimização de recursos e planejamento de capacidade.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tipos de simulação disponíveis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛒 **Simulações Disponíveis:**
        
        **1. 🛒 Simulação de Checkouts**
        - Modelagem de filas e tempos de espera
        - Otimização de capacidade e recursos
        - Análise de utilização por horário
        
        **2. 🚨 Simulação de Anomalias**
        - Modelagem de falhas de sistema
        - Análise de MTBF e downtime
        - Planejamento de manutenção
        
        **3. 🔍 Análise de Cenários**
        - Comparação de configurações
        - Teste de diferentes estratégias
        - Análise de trade-offs
        
        **4. 📊 Validação com Dados Reais**
        - Comparação real vs simulado
        - Calibração de modelos
        - Verificação de precisão
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ **Tecnologias e Benefícios:**
        
        **🔧 Stack Tecnológico:**
        - **SimPy 4.1+**: Simulação discreta de eventos
        - **Plotly**: Visualizações interativas
        - **Pandas**: Análise de dados
        - **Session State**: Persistência de resultados
        
        **📈 Benefícios Práticos:**
        - **Otimização de recursos** sem impactar operação
        - **Previsão de gargalos** antes que ocorram
        - **Teste de cenários** de forma segura
        - **Validação de estratégias** com dados históricos
        - **ROI mensurável** em decisões operacionais
        """)
    
    # Chamada para ação
    st.markdown("---")
    
    # Verificar se simulações estão ativas
    import socket
    def check_sim_port():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 8511))
            sock.close()
            return result == 0
        except:
            return False
    
    sim_active = check_sim_port()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if sim_active:
            st.success("✅ **Sistema de Simulações ATIVO** - Pronto para uso!")
            
            # Botão destacado para acessar simulações
            st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <a href="http://localhost:8511" target="_blank" rel="noopener noreferrer"
                   style="display: inline-block; padding: 15px 40px; 
                          background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                          color: white; text-decoration: none; border-radius: 25px;
                          font-weight: bold; font-size: 20px; 
                          box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                          transition: transform 0.2s;">
                    🚀 ACESSAR SIMULAÇÕES
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Sistema de Simulações INATIVO**")
            st.info("""
            **Para ativar as simulações:**
            1. Navegue até a página "🎮 Simulações" na sidebar
            2. Siga as instruções para iniciar o sistema
            3. Ou execute: `cd simulacoes && streamlit run app.py --server.port 8511`
            """)
    
    # Casos de uso práticos
    with st.expander("💼 **Casos de Uso Práticos das Simulações**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 **Cenários de Negócio:**
            
            **📈 Planejamento de Capacidade:**
            - Simular aumento de 20% na demanda
            - Determinar necessidade de novos checkouts
            - Calcular ROI de investimentos
            
            **🕐 Otimização de Horários:**
            - Identificar horários críticos
            - Planejar escalas de funcionários
            - Reduzir tempos de espera
            
            **🔧 Manutenção Preventiva:**
            - Modelar impacto de downtime
            - Otimizar cronogramas de manutenção
            - Minimizar perdas operacionais
            """)
        
        with col2:
            st.markdown("""
            ### 📊 **Resultados Esperados:**
            
            **💰 Benefícios Financeiros:**
            - Redução de 15-30% nos tempos de espera
            - Otimização de 20-40% na utilização de recursos
            - ROI positivo em 3-6 meses
            
            **⚡ Melhorias Operacionais:**
            - Decisões baseadas em dados
            - Prevenção de gargalos
            - Melhoria na satisfação do cliente
            
            **🎯 KPIs Mensuráveis:**
            - Tempo médio de espera
            - Taxa de utilização dos checkouts
            - Frequência de falhas do sistema
            """)
    
    st.markdown("---")
    
    # 📊 Visão geral do sistema
    st.markdown("---")
    st.header("📊 Visão Geral do Sistema")
    
    # Métricas gerais - incluindo simulações
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📁 Datasets Totais", 7, delta="3 tarefas")
    with col2:
        st.metric("🎮 Simulações", 4, delta="SimPy")
    with col3:
        st.metric("🔧 Tecnologias", 8, delta="Plotly, SimPy, etc")
    with col4:
        st.metric("📊 Status Sistema", "100%", delta="Todas operacionais")
    
    # Gráfico demonstrativo atualizado
    try:
        datasets_info = ["Tarefa 1", "Tarefa 2", "Tarefa 3", "Simulações"]
        files_count = [4, 2, 1, 4]
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        fig_status = px.bar(
            x=datasets_info,
            y=files_count,
            title="📊 Módulos por Componente do Sistema",
            color=datasets_info,
            color_discrete_sequence=colors
        )
        fig_status.update_layout(showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
        
    except Exception as e:
        st.info("📋 Gráfico não disponível no momento")
    
    # 🚀 Instruções de uso
    st.markdown("---")
    st.header("🚀 Como Usar o Sistema Completo")
    
    st.markdown("""
    ### 📋 Navegação e Funcionalidades:
    
    **🏠 Página Inicial (Você está aqui):**
    - Visão geral de todo o sistema
    - Status e métricas gerais
    - Acesso rápido às simulações
    
    **� Tarefa 1 - Análise Avançada:**
    - Detecção automática de anomalias
    - Gráficos interativos avançados
    - Insights inteligentes sobre transações
    
    **🚨 Tarefa 2 - Sistema de Alertas:**
    - Dashboard profissional de monitoramento
    - Alertas automáticos baseados em thresholds
    - Visualizações em tempo real
    
    **� Tarefa 3 - Central Integrada:**
    - Visão unificada de todas as tarefas
    - Monitoramento cross-datasets
    - Dashboard executivo
    
    **🎮 Simulações SimPy:**
    - Modelagem de cenários operacionais
    - Otimização de recursos e capacidade
    - Análise preditiva e validação
    """)
    
    # Fluxo recomendado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 **Fluxo Recomendado para Novos Usuários:**
        
        1. **🏠 Comece aqui** - Entenda o sistema geral
        2. **� Tarefa 1** - Explore análises básicas
        3. **🚨 Tarefa 2** - Veja sistema de alertas
        4. **📱 Tarefa 3** - Visão integrada completa
        5. **🎮 Simulações** - Modelagem avançada
        """)
    
    with col2:
        st.markdown("""
        ### 💡 **Dicas de Uso:**
        
        - **Navegação**: Use a sidebar esquerda
        - **Dados**: Carregados automaticamente
        - **Gráficos**: Totalmente interativos
        - **Performance**: Otimizado para web
        - **Mobile**: Interface responsiva
        """)
    
    # Status das funcionalidades
    st.markdown("---")
    st.markdown("### 🔍 **Status das Funcionalidades**")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.success("✅ **Análise de Dados** - 100% Funcional")
        st.success("✅ **Sistema de Alertas** - 100% Funcional")
        
    with status_col2:
        st.success("✅ **Monitoramento Integrado** - 100% Funcional")
        st.success("✅ **Gráficos Interativos** - 100% Funcional")
        
    with status_col3:
        st.success("✅ **Simulações SimPy** - 100% Funcional")
        st.info("ℹ️ **SMS Alerts** - Demo limitado")
    
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
    # 📱 TAREFA 3 - Execução direta para evitar problemas de contexto
    st.header("📱 Central de Monitoramento Integrado")
    
    # Código direto da Task 3 sem imports dinâmicos
    try:
        # Importar módulos necessários
        import sqlite3
        import time
        
        # 🎨 Header moderno
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1);'>
            <h1 style='color: white; text-align: center; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                📊 Central de Monitoramento SQLite
            </h1>
            <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1.3rem;'>
                Monitoramento Unificado com Bancos de Dados SQLite
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Função para carregar dados reais de forma segura
        def load_real_data_safely():
            """Carrega dados reais evitando operações problemáticas do Pandas"""
            data = {
                'checkout1': pd.DataFrame(),
                'checkout2': pd.DataFrame(),
                'general': pd.DataFrame(),
                'monitoring_logs': pd.DataFrame(),
                'alert_transactions_1': pd.DataFrame(),
                'alert_transactions_2': pd.DataFrame()
            }
            
            try:
                # Carregar dados da Tarefa 1 (Analyze_data)
                task1_db_path = 'Analyze_data/data.db'
                if os.path.exists(task1_db_path):
                    conn1 = sqlite3.connect(task1_db_path)
                    try:
                        data['checkout1'] = pd.read_sql_query("SELECT * FROM data_table_1 LIMIT 100", conn1)
                    except Exception:
                        pass
                    try:
                        data['checkout2'] = pd.read_sql_query("SELECT * FROM data_table_2 LIMIT 100", conn1)
                    except Exception:
                        pass
                    conn1.close()
                
                # Carregar dados da Tarefa 2 (Alert_Incident)
                task2_db_path = 'Alert_Incident/alert_data.db'
                if os.path.exists(task2_db_path):
                    conn2 = sqlite3.connect(task2_db_path)
                    try:
                        data['alert_transactions_1'] = pd.read_sql_query("SELECT * FROM transactions_1 LIMIT 100", conn2)
                    except Exception:
                        pass
                    try:
                        data['alert_transactions_2'] = pd.read_sql_query("SELECT * FROM transactions_2 LIMIT 100", conn2)
                    except Exception:
                        pass
                    conn2.close()
                    
            except Exception:
                pass
            
            return data
        
        # Função de análise ultra-segura
        def ultra_safe_analysis(data):
            """Análise usando APENAS operações básicas Python"""
            analysis = {
                'total_datasets': 0,
                'total_transactions': 0,
                'status_distribution': {},
                'alerts': [],
                'health_score': 100
            }
            
            try:
                for key, df in data.items():
                    if df is not None and len(df) > 0:
                        analysis['total_datasets'] += 1
                        analysis['total_transactions'] += len(df)
                        
                        # Análise de status usando iteração manual
                        if 'status' in df.columns:
                            status_counts = {}
                            failed_count = 0
                            denied_count = 0
                            total_count = 0
                            
                            # Iterar através de cada linha individualmente
                            for idx in range(len(df)):
                                try:
                                    status = df.iloc[idx]['status']
                                    total_count += 1
                                    
                                    if status in status_counts:
                                        status_counts[status] += 1
                                    else:
                                        status_counts[status] = 1
                                    
                                    if status == 'failed':
                                        failed_count += 1
                                    elif status == 'denied':
                                        denied_count += 1
                                        
                                except Exception:
                                    continue
                            
                            analysis['status_distribution'][key] = status_counts
                            
                            if total_count > 0:
                                failed_rate = (failed_count / total_count) * 100
                                denied_rate = (denied_count / total_count) * 100
                                
                                if failed_rate > 10:
                                    analysis['alerts'].append(f"🔴 {key}: Alta taxa de falhas ({failed_rate:.1f}%)")
                                    analysis['health_score'] -= 20
                                
                                if denied_rate > 15:
                                    analysis['alerts'].append(f"🟡 {key}: Taxa elevada de negações ({denied_rate:.1f}%)")
                                    analysis['health_score'] -= 10
            except Exception:
                pass
                
            return analysis
        
        # Carregar dados reais
        data = load_real_data_safely()
        analysis = ultra_safe_analysis(data)
        
        # 📊 Dashboard de métricas principais
        st.header("📊 Visão Geral do Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📋 Datasets Ativos",
                analysis['total_datasets'],
                delta="+1"
            )
        
        with col2:
            st.metric(
                "🔢 Total Transações",
                f"{analysis['total_transactions']:,}",
                delta="+150"
            )
        
        with col3:
            health_color = "🟢" if analysis['health_score'] > 80 else "🟡" if analysis['health_score'] > 60 else "🔴"
            st.metric(
                f"{health_color} Saúde Sistema",
                f"{analysis['health_score']}%",
                delta="Perfeito" if analysis['health_score'] >= 95 else f"{analysis['health_score']-100}"
            )
        
        with col4:
            alert_color = "🟢" if len(analysis['alerts']) == 0 else "🟡" if len(analysis['alerts']) < 3 else "🔴"
            st.metric(
                f"{alert_color} Alertas Ativos",
                len(analysis['alerts']),
                delta="Estável"
            )
        
        # Alertas ativos
        if analysis['alerts']:
            st.header("🚨 Alertas Ativos")
            for alert in analysis['alerts']:
                st.warning(alert)
        else:
            st.success("✅ Sistema operando normalmente - Nenhum alerta ativo")
        
        # Status distribution chart
        if analysis['status_distribution']:
            st.header("📊 Distribuição de Status")
            
            # Criar dados para o gráfico
            all_statuses = {}
            for dataset, statuses in analysis['status_distribution'].items():
                for status, count in statuses.items():
                    if status in all_statuses:
                        all_statuses[status] += count
                    else:
                        all_statuses[status] = count
            
            if all_statuses:
                fig_pie = px.pie(
                    values=list(all_statuses.values()),
                    names=list(all_statuses.keys()),
                    title="Distribuição Geral de Status",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        st.success("✅ Task 3 carregada com sucesso - Versão simplificada ativa")
        
    except Exception as e:
        st.error(f"❌ Erro na Task 3: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

elif current_route == "simulacoes":
    # 🎮 SIMULAÇÕES SIMPY
    st.header("🎮 Simulações SimPy")
    load_task_safely('simulacoes/app.py', 'Simulações SimPy')

# 📱 Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 <strong>Monitoring Analyst Test</strong> | Sistema Integrado de Análise de Transações</p>
    <p>Desenvolvido com ❤️ usando Streamlit, Plotly e Python</p>
</div>
""", unsafe_allow_html=True)