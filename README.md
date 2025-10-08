# 📊 Monitoring Analyst Test# Projeto monitoring-analyst-test



Este projeto é um sistema completo de análise de transações e monitoramento desenvolvido em Python com Streamlit. Contém três tarefas principais que demonstram diferentes aspectos de análise de dados e monitoramento.# rode na raiz

# Crie o ambiente virtual para o projeto

## 🚀 Configuração Inicialpython3 -m venv .venv && source .venv/bin/activate



### Pré-requisitos# Instale as dependências

- Python 3.8 ou superiorpython3 -m pip install -r requirements.txt

- pip (gerenciador de pacotes Python)



### Instalação# TAREFA 1 - Sistema de Análise de Transações



1. **Clone o repositório**##  Como Executar:

```bash

git clone <url-do-repositorio>```bash

cd monitoring-analyst-test# Navegar para o diretório da tarefa 1

```cd Analyze_data



2. **Crie e ative o ambiente virtual**# Executar aplicação

```bashstreamlit run app.py

# Criar ambiente virtual```

python3 -m venv .venv

### 📊 Funcionalidades:

# Ativar ambiente virtual (macOS/Linux)- ✅ Análise temporal de transações

source .venv/bin/activate- 📈 Comparação entre checkout 1 e checkout 2  

- � Visualização de dados com checkboxes interativos

# Ativar ambiente virtual (Windows)- 📋 Gráficos de today, yesterday, same day last week

.venv\Scripts\activate- 💾 Armazenamento em banco SQLite

```

# TAREFA 2

3. **Instale as dependências**

```bash# Rodando o app para geração dos gráficos Tarefa 1

python3 -m pip install -r requirements.txtcd Alert_Incident/

```streamlit run app.py



## 📋 Estrutura do Projeto# Monitoring



```# Rodando o app para geração dos gráficos Tarefa 1

monitoring-analyst-test/cd Monitoring/

├── README.mdstreamlit run app.py
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

---

## 📊 TAREFA 1 - Sistema de Análise de Transações

### 🎯 Objetivo
Sistema interativo para análise temporal de transações com comparação entre diferentes checkouts e visualização de dados históricos.

### 🛠️ Como Executar
```bash
# Navegar para o diretório da tarefa 1
cd Analyze_data

# Executar aplicação Streamlit
streamlit run app.py
```

### ✨ Funcionalidades
- **📈 Análise Temporal**: Visualização de transações por períodos (hoje, ontem, mesmo dia da semana passada)
- **🔄 Comparação de Checkouts**: Análise comparativa entre checkout_1 e checkout_2
- **✅ Interface Interativa**: Checkboxes para seleção dinâmica de visualizações
- **📊 Gráficos Dinâmicos**: Matplotlib integrado para visualizações em tempo real
- **💾 Persistência**: Armazenamento automatizado em banco SQLite
- **📋 Processamento CSV**: Carregamento e análise automática de arquivos CSV

### 🔧 Tecnologias Utilizadas
- **Streamlit**: Framework web para dashboards
- **Pandas**: Manipulação e análise de dados
- **Matplotlib**: Visualização de gráficos
- **SQLite**: Banco de dados local
- **NumPy**: Computação numérica

---

## 🚨 TAREFA 2 - Sistema de Alertas e Incidentes

### 🎯 Objetivo
Dashboard para monitoramento de transações com análise de status e identificação de incidentes através de visualizações de barras e pivot tables.

### 🛠️ Como Executar
```bash
# Navegar para o diretório da tarefa 2
cd Alert_Incident

# Executar aplicação Streamlit
streamlit run app.py
```

### ✨ Funcionalidades
- **📊 Análise de Status**: Contagem automática de transações por status
- **📈 Gráficos de Barras**: Visualização comparativa entre transactions_1 e transactions_2
- **🔄 Pivot Tables**: Reorganização inteligente de dados por tempo e status
- **🚨 Detecção de Incidentes**: Identificação visual de anomalias nos dados
- **📋 Dashboard Interativo**: Interface intuitiva para análise rápida

### 🔧 Tecnologias Utilizadas
- **Streamlit**: Interface web interativa
- **Pandas**: Análise e manipulação de dados
- **Plotly**: Gráficos interativos avançados
- **CSV Processing**: Leitura automática de dados

---

## 📱 TAREFA 3 - Sistema de Monitoramento com Alertas SMS

### 🎯 Objetivo
Sistema avançado de monitoramento em tempo real com capacidade de envio de alertas SMS via Twilio e persistência em banco de dados.

### 🛠️ Como Executar
```bash
# Navegar para o diretório da tarefa 3
cd Monitoring

# Executar aplicação Streamlit
streamlit run app.py
```

### ⚙️ Configuração SMS (Twilio)
1. Crie uma conta no [Twilio](https://www.twilio.com/)
2. Configure o arquivo `credenciais.py`:
```python
account_sid = "seu_account_sid"
token = "seu_auth_token"  
remetente = "seu_numero_twilio"
```

### ✨ Funcionalidades
- **📱 Alertas SMS**: Integração com Twilio para notificações instantâneas
- **💾 Persistência**: Armazenamento em SQLite com models personalizados
- **📊 Monitoramento Real-time**: Acompanhamento contínuo de métricas
- **🔄 Processamento Automático**: Conversão SQL para DataFrame
- **🚨 Sistema de Alertas**: Detecção automática de anomalias
- **📈 Visualização**: Dashboard para acompanhamento de métricas

### 🔧 Tecnologias Utilizadas
- **Streamlit**: Interface de monitoramento
- **Twilio**: Serviço de SMS
- **SQLite**: Banco de dados local
- **Pandas**: Processamento de dados
- **Plotly**: Visualizações interativas
- **Custom Models**: Estruturas de dados personalizadas

---

## 🛠️ Comandos Úteis

### Ativação do Ambiente Virtual
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Execução das Aplicações
```bash
# Tarefa 1 - Análise de Transações
cd Analyze_data && streamlit run app.py

# Tarefa 2 - Alertas e Incidentes  
cd Alert_Incident && streamlit run app.py

# Tarefa 3 - Monitoramento com SMS
cd Monitoring && streamlit run app.py
```

### Atualização de Dependências
```bash
pip install -r requirements.txt --upgrade
```

---

## 📝 Notas Importantes

- **🔒 Credenciais**: Configure adequadamente o arquivo `credenciais.py` para funcionalidades SMS
- **📊 Dados**: Os arquivos CSV estão incluídos para demonstração
- **🌐 Acesso**: Aplicações executam por padrão em `http://localhost:8501`
- **💾 Persistência**: Bancos SQLite são criados automaticamente
- **🐛 Debug**: Use `streamlit run app.py --logger.level=debug` para logs detalhados

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é para fins educacionais e de demonstração.

---
