# 📊 Monitoring Analyst Test

Sistema completo de análise de transações e monitoramento desenvolvido em Python com Streamlit. Contém três tarefas independentes com funcionalidades específicas de análise de dados.## 🚀 Execução Rápida

### � Executar Sistema Unificado (Recomendado)
```bash
# Ativar ambiente
source .venv/bin/activate

# Executar aplicação principal unificada
streamlit run main.py
# Acesso: http://localhost:8501
```

**✅ Vantagens do Sistema Unificado:**
- Uma única aplicação com navegação lateral
- Interface consistente entre todas as tarefas
- Mesmo sistema usado no deploy online
- Navegação fluida sem trocar de porta

### 📋 Executar Tarefas Individualmente
```bash
# Ativar ambiente
source .venv/bin/activate

# Tarefa 1: Análise Avançada de Transações
cd Analyze_data && streamlit run app.py
# Acesso: http://localhost:8502

# Tarefa 2: Sistema de Alertas e Incidentes  
cd ../Alert_Incident && streamlit run app.py
# Acesso: http://localhost:8501

# Tarefa 3: Monitoramento de Transações
cd ../Monitoring && streamlit run app.py
# Acesso: http://localhost:8503ine

**🚀 Aplicação em Produção:** [https://monitoring-analyst-test.streamlit.app/](https://monitoring-analyst-test.streamlit.app/)

### 💡 Como usar o deploy:
1. **Acesse a URL** acima para usar o sistema online
2. **Navegue** entre as tarefas usando o menu lateral
3. **Explore** cada funcionalidade sem necessidade de instalação local

### ⚠️ Limitações do Deploy Online:
- Sistema de SMS não funcional (requer configuração de serviços pagos)
- Algumas funcionalidades podem ter limitações de arquivo local
- Para funcionalidade completa, execute localmente conforme instruções abaixo

## 🚀 Configuração Inicial

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Geral

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd monitoring-analyst-test
```

2. **Crie e ative o ambiente virtual**
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual (macOS/Linux)
source .venv/bin/activate

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate
```

3. **Instale as dependências**
```bash
python3 -m pip install -r requirements.txt
```

## 📋 Estrutura do Projeto

```
monitoring-analyst-test/
├── README.md
├── requirements.txt
├── .venv/                    # Ambiente virtual
├── Analyze_data/            # 📊 TAREFA 1
│   ├── app.py
│   ├── data.db
│   └── data/
│       ├── checkout_1.csv
│       ├── checkout_2.csv
│       ├── transactions_1.csv
│       └── transactions_2.csv
├── Alert_Incident/          # 🚨 TAREFA 2  
│   ├── app.py
│   └── data/
│       ├── transactions_1.csv
│       └── transactions_2.csv
└── Monitoring/              # 📱 TAREFA 3
    ├── app.py
    ├── credenciais.py
    ├── database.db
    ├── models.py
    └── data/
        └── transactions_1.csv
```

```

## 📊 TAREFA 1: Análise Avançada de Transações

> **Título da Aplicação:** "📊 Análise Avançada de Transações"  
> **Localização:** `Analyze_data/`

### 🎯 O que faz
Sistema interativo para análise temporal de transações com comparação inteligente entre checkouts e detecção automática de anomalias.

### � Como executar
```bash
# Navegar para o diretório
cd Analyze_data

# Executar aplicação
streamlit run app.py
```

### ✨ Principais funcionalidades
- **📈 Gráficos Interativos**: Visualizações modernas com Plotly
- **🔍 Análise de Anomalias**: Detecção automática de problemas no Checkout 2
- **� Comparação Temporal**: Hoje vs Ontem vs Semana Passada
- **💡 Insights Inteligentes**: Diagnóstico de causas e soluções
- **� Métricas de Impacto**: Quantificação de perdas e prioridades
- **🎮 Controles Interativos**: Checkboxes para personalizar visualizações

### 🔧 Tecnologias
Plotly • Pandas • Matplotlib • SQLite • Streamlit

### 📍 Acesso Local
http://localhost:8502

---

## 🚨 TAREFA 2: Sistema de Alertas e Incidentes

> **Título da Aplicação:** "🚨 Sistema de Alertas e Incidentes - Tarefa 2"  
> **Localização:** `Alert_Incident/`

### 🎯 O que faz
Dashboard profissional para monitoramento de transações com sistema inteligente de detecção de anomalias e alertas automáticos.

### � Como executar
```bash
# Navegar para o diretório
cd Alert_Incident

# Executar aplicação
streamlit run app.py
```

### ✨ Principais funcionalidades
- **🎮 Interface Moderna**: Design profissional com gradientes e métricas
- **� Múltiplas Visualizações**: Barras, Pizza, Sunburst, Treemap
- **� Alertas Automáticos**: Detecção inteligente de anomalias críticas
- **📈 Análise Temporal**: Evolução dos status ao longo do tempo
- **� Recomendações**: Ações imediatas e preventivas
- **🔍 Análise Comparativa**: Side-by-side entre datasets
- **📋 Insights Automáticos**: Conclusões baseadas em dados

### 🔧 Tecnologias
Plotly Express • Pandas • Streamlit • Análise Estatística

### 📍 Acesso Local
http://localhost:8501

---

## 📱 TAREFA 3: Monitoramento de Transações

> **Título da Aplicação:** "Monitoramento de Transações"  
> **Localização:** `Monitoring/`

### 🎯 O que faz
Sistema avançado de monitoramento em tempo real com capacidade de envio de alertas SMS via Twilio e persistência em banco de dados.

### � Como executar
```bash
# Navegar para o diretório
cd Monitoring

# Executar aplicação
streamlit run app.py
```

### ⚙️ Configuração Twilio (Opcional)
1. Crie conta no [Twilio](https://www.twilio.com/)
2. Configure `credenciais.py`:
```python
account_sid = "seu_account_sid"
token = "seu_auth_token"  
remetente = "seu_numero_twilio"
```

### ✨ Principais funcionalidades
- **📱 Alertas SMS**: Notificações instantâneas via Twilio
- **💾 Persistência**: Banco SQLite com models personalizados
- **📊 Monitoramento Real-time**: Acompanhamento contínuo
- **🔄 Processamento Automático**: SQL para DataFrame
- **🚨 Sistema de Alertas**: Detecção de anomalias
- **📈 Visualizações**: Dashboard de métricas

### 🔧 Tecnologias
Twilio • SQLite • Pandas • Plotly • Custom Models

### 📍 Acesso Local
http://localhost:8503

---

## � Execução Rápida

### Executar Todas as Tarefas
```bash
# Ativar ambiente
source .venv/bin/activate

# Tarefa 1: Análise Avançada de Transações
cd Analyze_data && streamlit run app.py
# Acesso: http://localhost:8502

# Tarefa 2: Sistema de Alertas e Incidentes  
cd ../Alert_Incident && streamlit run app.py
# Acesso: http://localhost:8501

# Tarefa 3: Monitoramento de Transações
cd ../Monitoring && streamlit run app.py
# Acesso: http://localhost:8503
```

### Comandos de Manutenção
```bash
# Atualizar dependências
pip install -r requirements.txt --upgrade

# Debug detalhado
streamlit run app.py --logger.level=debug

# Parar todas as aplicações
pkill -f streamlit
```

---

## � Resumo das Funcionalidades

| Tarefa | Aplicação | Foco Principal | Tecnologia Destaque |
|--------|-----------|----------------|---------------------|
| **1** | � Análise Avançada | Detecção de anomalias em checkouts | Plotly + Análise Inteligente |
| **2** | 🚨 Alertas e Incidentes | Dashboard de monitoramento | Interface Moderna + Alertas |
| **3** | 📱 Monitoramento | Alertas SMS em tempo real | Twilio + Persistência |

---

## 📝 Informações Importantes

- **📊 Dados**: Arquivos CSV incluídos para demonstração
- **💾 Bancos**: SQLite criados automaticamente  
- **� Credenciais**: Configure `credenciais.py` apenas para SMS (Tarefa 3)
- **🌐 Portas**: Cada aplicação usa uma porta diferente
- **� Responsivo**: Todas as interfaces adaptam ao mobile

---

## 🎯 Para Desenvolvedores

### Deploy

#### 🌐 Deploy Atual - Streamlit Cloud
**URL de Produção:** [https://monitoring-analyst-test.streamlit.app/](https://monitoring-analyst-test.streamlit.app/)

**Configuração do Deploy:**
- **Repository:** `Beto1821/monitoring-analyst-test`
- **Branch:** `main`
- **Main file:** `main.py`
- **Python version:** 3.9+

#### 🔧 Arquitetura de Deploy
- **Sistema Unificado**: `main.py` como ponto de entrada único
- **Navegação Lateral**: Menu para alternar entre as 3 tarefas
- **Carregamento Seguro**: Tratamento gracioso de arquivos não encontrados
- **Interface Responsiva**: Funciona em desktop e mobile

#### 🚀 Outras Opções de Deploy
- **Streamlit Cloud**: ✅ Atualmente em uso (gratuito)
- **Heroku**: Para projetos com mais recursos
- **Railway**: Alternativa moderna
- **Render**: Deploy rápido e simples

### Estrutura
- Cada tarefa é **independente**
- **Dados compartilhados** entre algumas tarefas
- **Configuração única** do ambiente virtual

---

## 📞 Suporte Técnico

- **Streamlit**: [docs.streamlit.io](https://docs.streamlit.io/)
- **Plotly**: [plotly.com/python/](https://plotly.com/python/)
- **Twilio**: [twilio.com/docs/python](https://www.twilio.com/docs/python)

---

## 🎯 DESTAQUE: TAREFA 3 INTEGRADA

### 📊 Central de Monitoramento Renovada
A **Tarefa 3** foi completamente reformulada como **solução integrada**:

- **🔗 Integra Tarefas 1 + 2**: Monitora todos os dados em uma interface
- **🎮 Interface Moderna**: Design profissional com visualizações avançadas  
- **🚨 Alertas Inteligentes**: Detecção automática cross-datasets
- **📊 Dashboard Unificado**: Métricas consolidadas de todas as fontes
- **💡 Análise Correlacionada**: Insights baseados em dados integrados

### 🚀 Acesso Direto:
```bash
cd Monitoring && streamlit run app.py
# http://localhost:8502
```

**Agora você tem uma central de comando que resolve os problemas das tarefas anteriores!** 🎯

---

*Desenvolvido com ❤️ para análise inteligente de transações*
