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
    # Se especificar pasta da tarefa
    if task_folder:
        task_path = os.path.join(task_folder, db_filename)
        if os.path.exists(task_path):
            return task_path

# Função para detectar o caminho correto dos arquivos de dados CSV
def get_data_path(relative_path):
    """Detecta o caminho correto dos arquivos CSV"""
    # Caminho absoluto do diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir caminho absoluto
    absolute_path = os.path.join(current_dir, relative_path)
    
    if os.path.exists(absolute_path):
        return absolute_path
    
    # Fallback - tentar caminhos relativos
    fallback_paths = [
        relative_path,
        os.path.join('..', relative_path),
        os.path.join('../..', relative_path)
    ]
    
    for path in fallback_paths:
        if os.path.exists(path):
            return path
    
    return relative_path  # Retornar original se nada funcionar


@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_integrated_data():
    """Carrega dados integrados de todas as tarefas via SQLite"""
    try:
        data = {}
        
        # Carregar dados da Tarefa 1 (Analyze_data)
        task1_db_path = get_db_path('data.db', '../Analyze_data')
        if os.path.exists(task1_db_path):
            conn1 = sqlite3.connect(task1_db_path)
            data['checkout1'] = pd.read_sql_query("SELECT * FROM data_table_1", conn1)
            data['checkout2'] = pd.read_sql_query("SELECT * FROM data_table_2", conn1)
            data['general'] = pd.read_sql_query("SELECT * FROM data_table", conn1)
            conn1.close()
        else:
            st.warning("⚠️ Banco da Tarefa 1 não encontrado")
            data['checkout1'] = pd.DataFrame()
            data['checkout2'] = pd.DataFrame()
            data['general'] = pd.DataFrame()
        
        # Carregar dados do banco local de monitoramento
        monitoring_db_path = get_db_path('database.db')
        data['monitoring_logs'] = load_or_create_monitoring_data(monitoring_db_path)
        
        return data
        
    except Exception as e:
        st.error(f"Erro ao carregar dados integrados: {str(e)}")
        return {
            'checkout1': pd.DataFrame(),
            'checkout2': pd.DataFrame(), 
            'general': pd.DataFrame(),
            'monitoring_logs': pd.DataFrame()
        }

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

# 📊 Carregar dados das tarefas anteriores usando SQLite
@st.cache_data
def load_integrated_data():
    """Carrega dados de todas as tarefas SQLite para monitoramento integrado"""
    data = {}
    
    # Dados da Tarefa 1 (Analyze_data) - Bancos SQLite
    try:
        # Carregando dados do data.db da Tarefa 1
        db_path = get_db_path('data.db', '../Analyze_data')
        if db_path:
            conn = sqlite3.connect(db_path)
            
            # Tabelas do data.db
            query = "SELECT * FROM data_table"
            data['analyze_data_table'] = pd.read_sql_query(query, conn)
            
            try:
                query = "SELECT * FROM data_table_1"
                data['analyze_data_table_1'] = pd.read_sql_query(query, conn)
            except Exception:
                st.info("Tabela data_table_1 não encontrada no data.db")
            
            try:
                query = "SELECT * FROM data_table_2"
                data['analyze_data_table_2'] = pd.read_sql_query(query, conn)
            except Exception:
                st.info("Tabela data_table_2 não encontrada no data.db")
            
            conn.close()
        
        # Carregando dados do data1.db
        db1_path = get_db_path('data1.db', '../Analyze_data')
        if db1_path:
            conn = sqlite3.connect(db1_path)
            try:
                query = "SELECT * FROM data_table"
                data['analyze_data1'] = pd.read_sql_query(query, conn)
            except Exception:
                pass
            conn.close()
        
        # Carregando dados do data2.db
        db2_path = get_db_path('data2.db', '../Analyze_data')
        if db2_path:
            conn = sqlite3.connect(db2_path)
            try:
                query = "SELECT * FROM data_table"
                data['analyze_data2'] = pd.read_sql_query(query, conn)
            except Exception:
                pass
            conn.close()
            
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados SQLite da Tarefa 1: {str(e)}")
    
    # Dados da Tarefa 2 (Alert_Incident) - usando CSV como fallback
    try:
        # Verificar se existe banco SQLite na Tarefa 2
        alert_db_path = get_db_path('database.db', '../Alert_Incident')
        if alert_db_path:
            conn = sqlite3.connect(alert_db_path)
            try:
                query = "SELECT * FROM transactions"
                data['alert_transactions'] = pd.read_sql_query(query, conn)
            except Exception:
                # Fallback para CSV se não houver tabela
                path1 = '../Alert_Incident/data/transactions_1.csv'
                path2 = '../Alert_Incident/data/transactions_2.csv'
                data['alert_transactions_1'] = pd.read_csv(
                    get_data_path(path1))
                data['alert_transactions_2'] = pd.read_csv(
                    get_data_path(path2))
            conn.close()
        else:
            # Usar CSV se não houver banco SQLite
            path1 = '../Alert_Incident/data/transactions_1.csv'
            path2 = '../Alert_Incident/data/transactions_2.csv'
            data['alert_transactions_1'] = pd.read_csv(get_data_path(path1))
            data['alert_transactions_2'] = pd.read_csv(get_data_path(path2))
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados da Tarefa 2: {str(e)}")
    
    # Dados locais (Monitoring) - database.db local
    try:
        db_path = get_db_path('database.db')
        if db_path:
            conn = sqlite3.connect(db_path)
            try:
                query = "SELECT * FROM transactions"
                data['monitoring_transactions'] = pd.read_sql_query(
                    query, conn)
            except Exception:
                # Criar tabela se não existir
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        amount REAL,
                        status TEXT,
                        source TEXT
                    )
                ''')
                conn.commit()
                data['monitoring_transactions'] = pd.DataFrame()
            conn.close()
        else:
            # Fallback para CSV se não houver banco local
            path = 'data/transactions_1.csv'
            data['monitoring_transactions'] = pd.read_csv(get_data_path(path))
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados de monitoramento: {str(e)}")
        data['monitoring_transactions'] = pd.DataFrame()
    
    return data

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
    """Análise integrada de todos os dados"""
    analysis = {
        'total_datasets': 0,
        'total_transactions': 0,
        'status_distribution': {},
        'alerts': [],
        'health_score': 100
    }
    
    for key, df in data.items():
        if not df.empty:
            analysis['total_datasets'] += 1
            analysis['total_transactions'] += len(df)
            
            # Análise de status se existir
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                analysis['status_distribution'][key] = status_counts.to_dict()
                
                # Alertas baseados nos dados
                failed_rate = (df['status'] == 'failed').mean() * 100
                denied_rate = (df['status'] == 'denied').mean() * 100
                
                if failed_rate > 10:
                    analysis['alerts'].append(f"🔴 {key}: Alta taxa de falhas ({failed_rate:.1f}%)")
                    analysis['health_score'] -= 20
                
                if denied_rate > 15:
                    analysis['alerts'].append(f"🟡 {key}: Taxa elevada de negações ({denied_rate:.1f}%)")
                    analysis['health_score'] -= 10
    
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
data = load_integrated_data()
analysis = analyze_integrated_data(data)

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
    
    if 'checkout_1' in data and not data['checkout_1'].empty:
        checkout_col1, checkout_col2 = st.columns(2)
        
        with checkout_col1:
            st.markdown("#### 🏪 Checkout 1 - Status")
            checkout1_metrics = len(data['checkout_1'])
            st.metric("Registros", checkout1_metrics)
            
            # Gráfico simples se houver dados numéricos
            numeric_cols = data['checkout_1'].select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig_checkout1 = px.line(
                    data['checkout_1'], 
                    x=data['checkout_1'].index,
                    y=numeric_cols[0] if len(numeric_cols) > 0 else None,
                    title="Tendência Checkout 1"
                )
                st.plotly_chart(fig_checkout1, use_container_width=True)
        
        with checkout_col2:
            st.markdown("#### 🏪 Checkout 2 - Status")
            if 'checkout_2' in data and not data['checkout_2'].empty:
                checkout2_metrics = len(data['checkout_2'])
                st.metric("Registros", checkout2_metrics)
                
                numeric_cols2 = data['checkout_2'].select_dtypes(include=[np.number]).columns
                if len(numeric_cols2) > 0:
                    fig_checkout2 = px.line(
                        data['checkout_2'], 
                        x=data['checkout_2'].index,
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
        
        # Status distribution
        if 'status' in alert_data.columns:
            status_counts = alert_data['status'].value_counts()
            
            fig_alert = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Distribuição de Status - Dados de Alerta",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_alert, use_container_width=True)
            
            # Métricas de alerta
            col1, col2, col3 = st.columns(3)
            with col1:
                approved = (alert_data['status'] == 'approved').sum()
                st.metric("✅ Aprovadas", approved)
            with col2:
                failed = (alert_data['status'] == 'failed').sum()
                st.metric("❌ Falhas", failed)
            with col3:
                denied = (alert_data['status'] == 'denied').sum()
                st.metric("⛔ Negadas", denied)
        else:
            st.info("📋 Estrutura de dados não compatível com análise de status.")
    else:
        st.info("📋 Dados da Tarefa 2 não disponíveis para monitoramento.")

with tab3:
    st.subheader("📱 Monitoramento Local - Tarefa 3")
    
    if 'monitoring_transactions' in data and not data['monitoring_transactions'].empty:
        monitoring_data = data['monitoring_transactions']
        
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
            current_approved = (monitoring_data['status'] == 'approved').sum()
            current_failed = (monitoring_data['status'] == 'failed').sum()
            current_denied = (monitoring_data['status'] == 'denied').sum()
            
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
