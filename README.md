# 📊 Monitoring Analyst Test

Sistema completo de análise de transações e monitoramento desenvolvido em Python com Streamlit. Três tarefas indepen### ✨ Principais funcionalidades
- **🗃️ Integração SQLite**: Carregamento direto de bancos `data.db`, `data1.db`, `data2.db`
- **📈 Gráficos Interativos**: Visualizações modernas com Plotly
- **🔍 Análise de Anomalias**: Detecção automática de problemas no Checkout 2
- **📅 Comparação Temporal**: Hoje vs Ontem vs Semana Passada
- **⚡ Cache Inteligente**: @st.cache_data para queries otimizadases integradas em uma aplicação moderna com navegação por rotas e ícones dinâmicos.

## 🚀 Execução Rápida

### 🎯 Executar Sistema Unificado (Recomendado)
```bash
# Ativar ambiente
source .venv/bin/activate

# Executar aplicação principal unificada
streamlit run main.py
# Acesso: http://localhost:8501 (ou porta disponível)
```

**✅ Vantagens do Sistema Unificado:**
- 🧭 Navegação por rotas URL com ícones dinâmicos
- 📱 Interface responsiva e moderna
- 🔗 URLs compartilháveis para cada tarefa
- 🎨 Ícones da página mudam automaticamente
- 🚀 Sistema usado no deploy em produção

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

# Tarefa 3: Central de Monitoramento Integrado
cd ../Monitoring && streamlit run app.py
# Acesso: http://localhost:8503
```

**🚀 Aplicação em Produção:** [https://monitoring-analyst-test.streamlit.app/](https://monitoring-analyst-test.streamlit.app/)

### 💡 Como usar o deploy:
1. **Acesse a URL** acima para usar o sistema online
2. **Navegue** entre as tarefas usando o menu lateral OU URLs diretas:
   - 🏠 Home: `https://monitoring-analyst-test.streamlit.app/`
   - 📊 Tarefa 1: `https://monitoring-analyst-test.streamlit.app/?page=task1`
   - 🚨 Tarefa 2: `https://monitoring-analyst-test.streamlit.app/?page=task2`
   - 📱 Tarefa 3: `https://monitoring-analyst-test.streamlit.app/?page=task3`
3. **Compartilhe** URLs específicas com outros usuários
4. **Observe** como o ícone da página muda automaticamente

### 🎯 Novas Funcionalidades (Atualização Recente):
- **🧭 Navegação por Rotas:** URLs compartilháveis para cada tarefa (`/?page=task1`, `/?page=task2`, etc.)
- **🎨 Ícones Dinâmicos:** O ícone da página muda automaticamente conforme a rota
- **🔧 Sistema Corrigido:** Todos os problemas de renderização foram resolvidos
- **📱 Interface Moderna:** Design responsivo e profissional

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
├── main.py                  # 🚀 Sistema unificado com navegação por rotas
├── README.md
├── requirements.txt
├── .gitignore              # Arquivos ignorados pelo Git
├── .venv/                  # Ambiente virtual
├── Analyze_data/           # 📊 TAREFA 1 - SQLite
│   ├── app.py             # Sistema integrado com SQLite
│   ├── data.db           # 🗃️ Banco principal (data_table, data_table_1, data_table_2)
│   ├── data1.db          # 🗃️ Banco secundário (data_table)
│   ├── data2.db          # 🗃️ Banco terciário (data_table)
│   └── data/             # 📁 CSVs (fallback)
│       ├── checkout_1.csv
│       ├── checkout_2.csv
│       ├── transactions_1.csv
│       └── transactions_2.csv
├── Alert_Incident/         # 🚨 TAREFA 2  
│   ├── app.py
│   └── data/
│       ├── transactions_1.csv
│       └── transactions_2.csv
└── Monitoring/             # 📱 TAREFA 3 - Monitoramento SQLite
    ├── app.py             # Sistema integrado multi-database
    ├── credenciais.py     # Configurações Twilio
    ├── database.db       # 🗃️ Banco local de monitoramento
    ├── models.py         # Models SQLite
    └── data/             # 📁 CSVs (fallback)
        └── transactions_1.csv
```
```

```

## 📊 TAREFA 1: Análise Avançada de Transações SQLite

> **Título da Aplicação:** "📊 Análise de Dados - SQLite"  
> **Localização:** `Analyze_data/`

### 🎯 O que faz
Sistema interativo para análise temporal de transações usando **bancos de dados SQLite** com comparação inteligente entre checkouts e detecção automática de anomalias.

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

## 📱 TAREFA 3: Central de Monitoramento SQLite

> **Título da Aplicação:** "📊 Central de Monitoramento SQLite"  
> **Localização:** `Monitoring/`

### 🎯 O que faz
Sistema avançado de monitoramento unificado que integra **todos os bancos SQLite** das tarefas com capacidade de envio de alertas SMS via Twilio e persistência em banco de dados.

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
- **�️ Multi-Database**: Integração de todos os bancos SQLite (data.db, data1.db, data2.db, database.db)
- **�📱 Alertas SMS**: Notificações instantâneas via Twilio
- **💾 Persistência**: Banco SQLite com models personalizados
- **📊 Monitoramento Unificado**: Dados de todas as tarefas em uma interface
- **🔄 Processamento Automático**: SQL para DataFrame com fallback para CSV
- **🚨 Sistema de Alertas**: Detecção de anomalias cross-datasets
- **📈 Visualizações**: Dashboard de métricas integradas
- **⚡ Cache Otimizado**: Carregamento inteligente com detecção automática

### 🔧 Tecnologias
SQLite Multi-Database • Twilio • Pandas • Plotly • Custom Models • Cache Avançado

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
- **🧭 Navegação por Rotas**: URLs compartilháveis (`/?page=task1`, `/?page=task2`, `/?page=task3`)
- **🎨 Ícones Dinâmicos**: Favicon muda automaticamente por página
- **📱 Interface Responsiva**: Design moderno que funciona em desktop e mobile
- **🔧 Carregamento Seguro**: Tratamento gracioso de arquivos não encontrados
- **⚡ Performance**: APIs atualizadas para versões mais recentes do Streamlit

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

## 🗃️ INTEGRAÇÃO SQLITE COMPLETA

### 📊 Arquitetura de Dados
O sistema foi **completamente migrado** para usar bancos de dados SQLite:

#### 🎯 Tarefa 1 - Analyze_data
- **data.db**: Tabelas `data_table`, `data_table_1`, `data_table_2`
- **data1.db**: Tabela `data_table` (dados específicos)
- **data2.db**: Tabela `data_table` (dados específicos)

#### 📱 Tarefa 3 - Monitoring
- **Integração Multi-Database**: Acesso unificado a todos os bancos
- **database.db**: Banco local de monitoramento
- **Detecção Automática**: Identifica bancos disponíveis em runtime

### ⚡ Vantagens da Integração SQLite
- **🚀 Performance**: Queries SQL nativas são muito mais rápidas que CSV
- **🔍 Flexibilidade**: Consultas complexas com JOIN, WHERE, GROUP BY
- **💾 Economia de Memória**: Carregamento sob demanda dos dados
- **🔄 Fallback**: Mantém compatibilidade com CSVs quando necessário
- **⚡ Cache**: Sistema de cache otimizado para queries repetidas

### 🔧 Estrutura das Tabelas
```sql
-- Estrutura típica dos dados horários
CREATE TABLE data_table (
    time TEXT,
    today INTEGER,
    yesterday INTEGER,
    same_day_last_week INTEGER,
    avg_last_week REAL,
    avg_last_month REAL
);
```

---

## 📋 Changelog

### 🆕 Versão 2.1 (Outubro 2025) - Integração SQLite Completa
- **🗃️ SQLite Nativo:** Migração completa de CSV para bancos SQLite
- **📊 Tarefa 1 SQLite:** Carregamento de `data.db`, `data1.db`, `data2.db`
- **📱 Monitoramento Unificado:** Integração multi-database na Tarefa 3
- **⚡ Cache Otimizado:** @st.cache_data para queries SQLite
- **🔄 Fallback Inteligente:** Sistema mantém compatibilidade com CSV
- **🔍 Detecção Automática:** Identifica bancos disponíveis dinamicamente

### 🆕 Versão 2.0 (Outubro 2025)
- **🧭 Navegação por Rotas:** Sistema de URLs compartilháveis implementado
- **🎨 Ícones Dinâmicos:** Favicon muda automaticamente por página
- **🔧 Correções:** Problemas de renderização da Tarefa 2 resolvidos
- **⚡ APIs Atualizadas:** Migração de APIs experimentais para versões estáveis
- **📱 Interface Melhorada:** Design mais moderno e responsivo
- **🚀 Deploy Otimizado:** Sistema unificado em produção

### 📊 Versão 1.0 (Versão Inicial)
- **📊 Tarefa 1:** Análise avançada de transações com detecção de anomalias
- **🚨 Tarefa 2:** Sistema de alertas e incidentes profissional
- **📱 Tarefa 3:** Central de monitoramento integrado com SMS
- **🌐 Deploy:** Primeira versão em produção no Streamlit Cloud

---

*Desenvolvido com ❤️ para análise inteligente de transações*
