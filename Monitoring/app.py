import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import time
import os

# Função para detectar o caminho correto dos bancos de dados
def get_db_path(db_filename, task_folder=None):
    """Detecta o caminho correto dos arquivos de banco de dados"""
    import os
    import sys
    
    # Lista de caminhos para tentar
    paths_to_try = []
    
    # Se especificar pasta da tarefa
    if task_folder:
        # Caminho relativo direto
        paths_to_try.append(os.path.join(task_folder, db_filename))
        
        # Se executado do diretório raiz do projeto
        paths_to_try.append(os.path.join(".", task_folder, db_filename))
        
        # Caminho absoluto baseado no diretório atual
        current_dir = os.getcwd()
        paths_to_try.append(os.path.join(current_dir, task_folder, db_filename))
        
        # Caminho subindo um nível (caso esteja dentro de Monitoring)
        paths_to_try.append(os.path.join("..", task_folder, db_filename))
    
    # Caminho relativo atual
    paths_to_try.append(db_filename)
    
    # Se executado a partir do main.py
    paths_to_try.append(os.path.join("Monitoring", db_filename))
    
    # Caminho absoluto como fallback usando abspath diretamente
    try:
        current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        paths_to_try.append(os.path.join(current_dir, "Monitoring", db_filename))
        
        # Tentar diretório atual
        current_working_dir = os.getcwd()
        paths_to_try.append(os.path.join(current_working_dir, "Monitoring", db_filename))
        
        # Se task_folder especificado, tentar do diretório atual
        if task_folder:
            paths_to_try.append(os.path.join(current_working_dir, task_folder, db_filename))
            
    except Exception:
        pass
    
    # Testar todos os caminhos
    for path in paths_to_try:
        if os.path.exists(path):
            return path
    
    return None  # Retornar None se não encontrar

# Função para detectar o caminho correto dos arquivos de dados CSV
def get_data_path(relative_path):
    """Detecta o caminho correto dos arquivos CSV"""
    import os
    
    # Tentar caminho relativo direto primeiro
    if os.path.exists(relative_path):
        return relative_path
    
    # Tentar usando diretório de trabalho atual
    try:
        current_working_dir = os.getcwd()
        absolute_path = os.path.join(current_working_dir, relative_path)
        if os.path.exists(absolute_path):
            return absolute_path
    except Exception:
        pass
    
    # Fallback - tentar caminhos relativos
    fallback_paths = [
        os.path.join('..', relative_path),
        os.path.join('../..', relative_path),
        os.path.join('Monitoring', relative_path)
    ]
    
    for path in fallback_paths:
        if os.path.exists(path):
            return path
    
    return relative_path  # Retornar original se nada funcionar


def create_alert_database_from_csv():
    """Cria banco SQLite a partir dos CSVs da Tarefa 2"""
    try:
        task2_db_path = 'Alert_Incident/alert_data.db'
        csv_path1 = 'Alert_Incident/data/transactions_1.csv'
        csv_path2 = 'Alert_Incident/data/transactions_2.csv'
        
        conn = sqlite3.connect(task2_db_path)
        
        # Carregar CSV 1 se existir
        if os.path.exists(csv_path1):
            df1 = pd.read_csv(csv_path1)
            df1.to_sql('transactions_1', conn, if_exists='replace', index=False)
        
        # Carregar CSV 2 se existir
        if os.path.exists(csv_path2):
            df2 = pd.read_csv(csv_path2)
            df2.to_sql('transactions_2', conn, if_exists='replace', index=False)
        
        conn.close()
        
    except Exception as e:
        # Se houver erro, não quebrar a aplicação
        pass


def load_integrated_data():
    """Carrega dados integrados de todas as tarefas via SQLite - versão ultra-robusta sem cache"""
    data = {
        'checkout1': pd.DataFrame(),
        'checkout2': pd.DataFrame(),
        'general': pd.DataFrame(),
        'monitoring_logs': pd.DataFrame(),
        'alert_transactions_1': pd.DataFrame(),
        'alert_transactions_2': pd.DataFrame()
    }
    
    # Carregar dados da Tarefa 1 (Analyze_data) 
    try:
        task1_db_path = 'Analyze_data/data.db'
        if os.path.exists(task1_db_path):
            conn1 = sqlite3.connect(task1_db_path)
            try:
                data['checkout1'] = pd.read_sql_query("SELECT * FROM data_table_1", conn1)
            except Exception:
                pass
            try:
                data['checkout2'] = pd.read_sql_query("SELECT * FROM data_table_2", conn1)
            except Exception:
                pass
            try:
                data['general'] = pd.read_sql_query("SELECT * FROM data_table", conn1)
            except Exception:
                pass
            conn1.close()
    except Exception:
        pass
    
    # Carregar dados do banco local de monitoramento
    try:
        monitoring_db_path = get_db_path('database.db')
        if monitoring_db_path:
            data['monitoring_logs'] = load_or_create_monitoring_data(monitoring_db_path)
    except Exception:
        pass
    
    # Carregar dados da Tarefa 2 (Alert_Incident) - convertendo CSV para SQLite
    try:
        task2_db_path = 'Alert_Incident/alert_data.db'
        
        # Se o banco não existir, criar a partir dos CSVs
        if not os.path.exists(task2_db_path):
            create_alert_database_from_csv()
        
        # Carregar usando SQL
        if os.path.exists(task2_db_path):
            conn2 = sqlite3.connect(task2_db_path)
            try:
                data['alert_transactions_1'] = pd.read_sql_query("SELECT * FROM transactions_1", conn2)
            except Exception:
                pass
            try:
                data['alert_transactions_2'] = pd.read_sql_query("SELECT * FROM transactions_2", conn2)
            except Exception:
                pass
            conn2.close()
    except Exception:
        pass
    
    return data

def load_or_create_monitoring_data(db_path):
    """Carrega ou cria dados de monitoramento"""
    try:
        conn = sqlite3.connect(db_path)
        
        # Criar tabela se não existir
        conn.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                value REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verificar se há dados
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM monitoring_events")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Inserir dados de exemplo
            sample_data = [
                ('00h', 'checkout1', 'transaction_count', 'info', 'Transações processadas', 6),
                ('01h', 'checkout1', 'transaction_count', 'info', 'Transações processadas', 3),
                ('02h', 'checkout1', 'transaction_count', 'warning', 'Volume baixo detectado', 3),
                ('00h', 'checkout2', 'transaction_count', 'critical', 'Checkout com problemas', 2),
                ('01h', 'checkout2', 'transaction_count', 'critical', 'Sistema instável', 1),
                ('02h', 'checkout2', 'transaction_count', 'warning', 'Recuperação parcial', 4),
            ]
            
            for item in sample_data:
                conn.execute('''
                    INSERT INTO monitoring_events (timestamp, source, event_type, severity, message, value)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', item)
            
            conn.commit()
        
        # Carregar dados
        df = pd.read_sql_query("SELECT * FROM monitoring_events ORDER BY timestamp", conn)
        conn.close()
        return df
        
    except Exception as e:
        st.error(f"Erro ao acessar banco de monitoramento: {str(e)}")
        return pd.DataFrame()

# 🎨 Configuração da página (apenas quando executado individualmente)
try:
    st.set_page_config(
        page_title="📊 Central de Monitoramento Integrado",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except st.errors.StreamlitAPIException:
    # Já foi configurado pelo main.py
    pass

# 🚨 Sistema de alertas SMS (opcional)
def enviar_sms(mensagem):
    """Sistema de SMS usando Twilio (opcional)"""
    try:
        from twilio.rest import Client
        import credenciais
        
        account_sid = credenciais.account_sid
        token = credenciais.token
        client = Client(account_sid, token)
        
        remetente = credenciais.remetente
        destino = '+5535998022002'
        
        message = client.messages.create(
            to=destino,
            from_=remetente,
            body=mensagem
        )
        return f"SMS enviado! ID: {message.sid}"
    except ImportError:
        return "⚠️ Twilio não configurado. Alerta registrado no log."
    except Exception as e:
        return f"❌ Erro ao enviar SMS: {str(e)}"

# 📊 Análise integrada dos dados
def analyze_integrated_data(data):
    """Análise integrada usando APENAS operações básicas Python - versão final"""
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
                
                # Análise de status APENAS com Python básico
                if 'status' in df.columns:
                    try:
                        # Converter para lista Python básica
                        status_values = []
                        for index, row in df.iterrows():
                            status_values.append(row['status'])
                        
                        # Contar manualmente
                        status_counts = {}
                        for status in status_values:
                            if status in status_counts:
                                status_counts[status] += 1
                            else:
                                status_counts[status] = 1
                        
                        analysis['status_distribution'][key] = status_counts
                        
                        # Análise de saúde usando contagem manual
                        total_records = len(status_values)
                        if total_records > 0:
                            failed_count = 0
                            denied_count = 0
                            
                            for status in status_values:
                                if status == 'failed':
                                    failed_count += 1
                                elif status == 'denied':
                                    denied_count += 1
                            
                            failed_rate = (failed_count / total_records) * 100
                            denied_rate = (denied_count / total_records) * 100
                            
                            if failed_rate > 10:
                                analysis['alerts'].append(f"🔴 {key}: Alta taxa de falhas ({failed_rate:.1f}%)")
                                analysis['health_score'] -= 20
                            
                            if denied_rate > 15:
                                analysis['alerts'].append(f"🟡 {key}: Taxa elevada de negações ({denied_rate:.1f}%)")
                                analysis['health_score'] -= 10
                    except Exception:
                        # Se houver qualquer erro, pular este dataset
                        continue
    except Exception:
        # Se houver qualquer erro geral, retornar análise básica
        pass
    
    # Garantir que health_score não seja negativo
    if analysis['health_score'] < 0:
        analysis['health_score'] = 0
    
    return analysis

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

# Carregar dados
try:
    data = load_integrated_data()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados integrados: {str(e)}")
    # Fallback com dados vazios
    data = {
        'checkout1': pd.DataFrame(),
        'checkout2': pd.DataFrame(),
        'general': pd.DataFrame(),
        'monitoring_logs': pd.DataFrame(),
        'alert_transactions_1': pd.DataFrame(),
        'alert_transactions_2': pd.DataFrame()
    }

try:
    analysis = analyze_integrated_data(data)
except Exception as e:
    st.error(f"❌ Erro na análise consolidada: {str(e)}")
    # Fallback com análise vazia
    analysis = {
        'total_datasets': 0,
        'total_transactions': 0,
        'status_distribution': {},
        'alerts': [],
        'health_score': 100
    }

# 📊 Dashboard de métricas principais
st.header("📊 Visão Geral do Sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Datasets Ativos", 
        analysis['total_datasets'],
        delta=f"{analysis['total_datasets']}/6 disponíveis"
    )

with col2:
    st.metric(
        "🔢 Total Transações", 
        f"{analysis['total_transactions']:,}",
        delta="+100%" if analysis['total_transactions'] > 0 else "Sem dados"
    )

with col3:
    health_color = "🟢" if analysis['health_score'] > 80 else "🟡" if analysis['health_score'] > 60 else "🔴"
    st.metric(
        f"{health_color} Saúde Sistema", 
        f"{analysis['health_score']}/100",
        delta=f"{analysis['health_score']-100}" if analysis['health_score'] < 100 else "Perfeito"
    )

with col4:
    alert_count = len(analysis['alerts'])
    alert_color = "🟢" if alert_count == 0 else "🟡" if alert_count < 3 else "🔴"
    st.metric(
        f"{alert_color} Alertas Ativos", 
        alert_count,
        delta="Tudo OK" if alert_count == 0 else f"{alert_count} problemas"
    )

# 🚨 Sistema de alertas
if analysis['alerts']:
    st.markdown("---")
    st.header("🚨 Alertas do Sistema")
    
    for alert in analysis['alerts']:
        if "🔴" in alert:
            st.error(alert)
        elif "🟡" in alert:
            st.warning(alert)
        else:
            st.info(alert)

# 📊 Análise por tarefa
st.markdown("---")
st.header("📈 Monitoramento por Tarefa")

tab1, tab2, tab3, tab_sms = st.tabs([
    "📊 Tarefa 1: Checkout Analysis", 
    "🚨 Tarefa 2: Alert System", 
    "📱 Tarefa 3: Monitoring",
    "📱 Sistema SMS"
])

with tab1:
    st.subheader("📊 Análise de Checkouts - Integração Tarefa 1")
    
    if 'checkout1' in data and not data['checkout1'].empty:
        checkout_col1, checkout_col2 = st.columns(2)
        
        with checkout_col1:
            st.markdown("#### 🏪 Checkout 1 - Status")
            checkout1_metrics = len(data['checkout1'])
            st.metric("Registros", checkout1_metrics)
            
            # Gráfico simples se houver dados numéricos
            numeric_cols = data['checkout1'].select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig_checkout1 = px.line(
                    data['checkout1'], 
                    x=data['checkout1'].index,
                    y=numeric_cols[0] if len(numeric_cols) > 0 else None,
                    title="Tendência Checkout 1"
                )
                st.plotly_chart(fig_checkout1, use_container_width=True)
        
        with checkout_col2:
            st.markdown("#### 🏪 Checkout 2 - Status")
            if 'checkout2' in data and not data['checkout2'].empty:
                checkout2_metrics = len(data['checkout2'])
                st.metric("Registros", checkout2_metrics)
                
                numeric_cols2 = data['checkout2'].select_dtypes(include=[np.number]).columns
                if len(numeric_cols2) > 0:
                    fig_checkout2 = px.line(
                        data['checkout2'], 
                        x=data['checkout2'].index,
                        y=numeric_cols2[0] if len(numeric_cols2) > 0 else None,
                        title="Tendência Checkout 2"
                    )
                    st.plotly_chart(fig_checkout2, use_container_width=True)
    else:
        st.info("📋 Dados da Tarefa 1 não disponíveis para monitoramento.")

with tab2:
    st.subheader("🚨 Sistema de Alertas - Integração Tarefa 2")
    
    if 'alert_transactions_1' in data and not data['alert_transactions_1'].empty:
        alert_data = data['alert_transactions_1']
        
        # Status distribution - versão robusta
        if 'status' in alert_data.columns:
            try:
                # Contar status usando Python básico
                status_list = alert_data['status'].tolist()
                status_counts = {}
                
                for status in status_list:
                    if status in status_counts:
                        status_counts[status] += 1
                    else:
                        status_counts[status] = 1
                
                if status_counts:
                    fig_alert = px.pie(
                        values=list(status_counts.values()),
                        names=list(status_counts.keys()),
                        title="Distribuição de Status - Dados de Alerta",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig_alert, use_container_width=True)
                
                # Métricas de alerta - contagem manual
                col1, col2, col3 = st.columns(3)
                with col1:
                    approved = status_list.count('approved')
                    st.metric("✅ Aprovadas", approved)
                with col2:
                    failed = status_list.count('failed')
                    st.metric("❌ Falhas", failed)
                with col3:
                    denied = status_list.count('denied')
                    st.metric("⛔ Negadas", denied)
            except Exception as e:
                st.error(f"❌ Erro na análise de status: {str(e)}")
        else:
            st.info("📋 Estrutura de dados não compatível com análise de status.")
    else:
        st.info("📋 Dados da Tarefa 2 não disponíveis para monitoramento.")

with tab3:
    st.subheader("📱 Monitoramento Local - Tarefa 3")
    
    if 'monitoring_logs' in data and not data['monitoring_logs'].empty:
        monitoring_data = data['monitoring_logs']
        
        # Configuração de thresholds
        st.markdown("#### ⚙️ Configuração de Alertas")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            threshold_approved = st.number_input("🟢 Limite Aprovadas", value=1000, step=100)
        with col2:
            threshold_failed = st.number_input("🔴 Limite Falhas", value=100, step=10)
        with col3:
            threshold_denied = st.number_input("🟡 Limite Negadas", value=150, step=25)
        
        # Análise em tempo real
        if 'status' in monitoring_data.columns:
            try:
                # Contagem manual para evitar problemas do Pandas
                status_list = monitoring_data['status'].tolist()
                current_approved = status_list.count('approved')
                current_failed = status_list.count('failed')
                current_denied = status_list.count('denied')
                
                # Status atual
                st.markdown("#### 📊 Status Atual")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    status_approved = "🚨" if current_approved > threshold_approved else "✅"
                    delta_approved = int(current_approved - threshold_approved)
                    st.metric(f"{status_approved} Aprovadas", int(current_approved), 
                             delta=delta_approved)
                
                with col2:
                    status_failed = "🚨" if current_failed > threshold_failed else "✅"
                    delta_failed = int(current_failed - threshold_failed)
                    st.metric(f"{status_failed} Falhas", int(current_failed),
                             delta=delta_failed)
                
                with col3:
                    status_denied = "🚨" if current_denied > threshold_denied else "✅"
                    delta_denied = int(current_denied - threshold_denied)
                    st.metric(f"{status_denied} Negadas", int(current_denied),
                             delta=delta_denied)
            except Exception as e:
                st.error(f"❌ Erro na análise de monitoramento: {str(e)}")
            
            # Gráfico de monitoramento
            fig_monitoring = px.bar(
                x=['Aprovadas', 'Falhas', 'Negadas'],
                y=[current_approved, current_failed, current_denied],
                title="Monitoramento em Tempo Real",
                color=['Aprovadas', 'Falhas', 'Negadas'],
                color_discrete_map={
                    'Aprovadas': '#2ecc71',
                    'Falhas': '#e74c3c', 
                    'Negadas': '#f39c12'
                }
            )
            st.plotly_chart(fig_monitoring, use_container_width=True)
            
        else:
            st.info("📋 Dados locais não possuem coluna 'status' para monitoramento.")
            st.dataframe(monitoring_data.head())
    else:
        st.error("❌ Dados de monitoramento local não encontrados!")

with tab_sms:
    st.subheader("📱 Sistema de Alertas SMS")
    
    # Interface para SMS
    st.markdown("#### ⚙️ Configuração SMS")
    
    sms_enabled = st.checkbox("📱 Ativar alertas SMS", value=False)
    
    if sms_enabled:
        phone_number = st.text_input("📞 Número de destino", value="+5535998022002")
        
        # Teste de SMS
        if st.button("🧪 Testar SMS"):
            test_message = f"🧪 Teste do sistema de monitoramento - {datetime.now().strftime('%H:%M:%S')}"
            result = enviar_sms(test_message)
            st.success(result)
        
        # Alertas automáticos
        st.markdown("#### 🚨 Alertas Automáticos")
        
        auto_alerts = st.checkbox("🤖 Ativar alertas automáticos", value=False)
        
        if auto_alerts and analysis['alerts']:
            if st.button("📤 Enviar Alertas Pendentes"):
                for alert in analysis['alerts'][:3]:  # Limitar a 3 alertas
                    result = enviar_sms(f"ALERTA SISTEMA: {alert}")
                    st.info(result)
    else:
        st.info("📱 SMS desativado. Configure Twilio para ativar.")

# 📊 Análise consolidada
st.markdown("---")
st.header("📊 Análise Consolidada")

if analysis['status_distribution']:
    # Criar gráfico consolidado
    consolidated_data = []
    for dataset, statuses in analysis['status_distribution'].items():
        for status, count in statuses.items():
            consolidated_data.append({
                'Dataset': dataset,
                'Status': status,
                'Count': count
            })
    
    if consolidated_data:
        df_consolidated = pd.DataFrame(consolidated_data)
        
        fig_consolidated = px.sunburst(
            df_consolidated,
            path=['Dataset', 'Status'],
            values='Count',
            title="Distribuição Consolidada por Dataset e Status"
        )
        st.plotly_chart(fig_consolidated, use_container_width=True)

# 🎯 Recomendações
st.markdown("---")
st.header("💡 Recomendações do Sistema")

recommendations = [
    "🔄 **Integração Completa**: Todos os datasets estão sendo monitorados",
    "📊 **Dashboard Unificado**: Visão centralizada de todas as tarefas",
    "🚨 **Alertas Inteligentes**: Sistema automático de detecção de anomalias",
    "📱 **Notificações SMS**: Alertas críticos via Twilio (opcional)",
    "📈 **Análise Consolidada**: Correlação entre diferentes fontes de dados",
    "🎯 **Monitoramento Real-time**: Acompanhamento contínuo de métricas"
]

for rec in recommendations:
    st.markdown(f"• {rec}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📊 <strong>Central de Monitoramento Integrado</strong> | Unificando Tarefas 1, 2 e 3</p>
    <p>Sistema inteligente de monitoramento com alertas automáticos e análise consolidada</p>
</div>
""", unsafe_allow_html=True)
