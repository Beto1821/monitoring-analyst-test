# 📊 Monitoring Analyst Test

Sistema completo de análise de transações e monitoramento desenvolvido em Python com Streamlit. Quatro módulos integrados em uma aplicação moderna com navegação por rotas e ícones dinâmicos.

## ✨ Principais Funcionalidades

- **🗃️ Integração SQLite**: Carregamento direto de bancos `data.db`, `data1.db`, `data2.db`
- **📈 Gráficos Interativos**: Visualizações modernas com Plotly
- **🔍 Análise de Anomalias**: Detecção automática de problemas de performance
- **📅 Comparação Temporal**: Hoje vs Ontem vs Semana Passada
- **⚡ Cache Inteligente**: Otimizações para queries SQLite
- **🎮 Simulações SimPy**: Modelagem avançada de sistemas
- **🧭 Navegação por Rotas**: URLs compartilháveis para cada módulo
- **📱 Interface Responsiva**: Design moderno e profissional

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

# Simulações SimPy: Modelagem e Simulação
cd ../simulacoes && streamlit run app.py
# Acesso: http://localhost:8504
```

**🚀 Aplicação em Produção:** [https://monitoring-analyst-test.streamlit.app/](https://monitoring-analyst-test.streamlit.app/)

### 💡 Como usar o deploy:
1. **Acesse a URL** acima para usar o sistema online
2. **Navegue** entre as tarefas usando o menu lateral OU URLs diretas:
   - 🏠 Home: `https://monitoring-analyst-test.streamlit.app/`
   - 📊 Tarefa 1: `https://monitoring-analyst-test.streamlit.app/?page=task1`
   - 🚨 Tarefa 2: `https://monitoring-analyst-test.streamlit.app/?page=task2`
   - 📱 Tarefa 3: `https://monitoring-analyst-test.streamlit.app/?page=task3`
   - 🎮 Simulações: `https://monitoring-analyst-test.streamlit.app/?page=simulacoes`
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
├── Monitoring/             # 📱 TAREFA 3 - Monitoramento SQLite
    ├── app.py             # Sistema integrado multi-database
    ├── credenciais.py     # Configurações Twilio
    ├── database.db       # 🗃️ Banco local de monitoramento
    ├── models.py         # Models SQLite
    └── data/             # 📁 CSVs (fallback)
        └── transactions_1.csv
└── simulacoes/             # 🎮 SIMULAÇÕES SIMPY
    ├── app.py             # Interface principal Streamlit
    ├── checkout_simulation.py    # Modelagem de checkouts
    ├── anomaly_simulation.py     # Simulação de falhas
    └── scenario_simulation.py    # Análise de cenários
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

## 📱 TAREFA 3: Central de Monitoramento Integrado

> **Título da Aplicação:** "� Central de Monitoramento Integrado"  
> **Localização:** `Monitoring/` (integrada no sistema unificado)

### 🎯 O que faz
Sistema avançado de monitoramento unificado que integra **todos os bancos SQLite** das tarefas com análise consolidada de transações e alertas automáticos. Completamente reformulada para máxima estabilidade e compatibilidade.

### 🚀 Como executar

#### **Método Recomendado - Sistema Unificado:**
```bash
# Executar via sistema principal (mais estável)
streamlit run main.py
# Acesse: http://localhost:8501/?page=task3
```

#### **Método Individual:**
```bash
# Navegar para o diretório
cd Monitoring

# Executar aplicação individual
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

### ✨ Principais Funcionalidades
- **🗃️ Multi-Database**: Integração de todos os bancos SQLite (data.db, data1.db, data2.db)
- **📱 Alertas SMS**: Notificações instantâneas via Twilio (opcional)
- **💾 Persistência**: Banco SQLite com models personalizados
- **📊 Dashboard Consolidado**: Métricas de todas as tarefas unificadas
- **🔄 Carregamento Inteligente**: Sistema ultra-robusto com fallbacks automáticos
- **🚨 Análise Integrada**: Detecção de anomalias cross-datasets
- **📈 Visualizações Avançadas**: Gráficos interativos com distribuição de status
- **⚡ Arquitetura Otimizada**: Versão redesenhada para máxima compatibilidade
- **🛡️ Ultra-Robusta**: Operações básicas Python para evitar conflitos de versão

### 🔧 Tecnologias
SQLite Multi-Database • Twilio • Pandas • Plotly • Python Puro • Streamlit

### 📍 Acesso Local
- **Sistema Unificado:** http://localhost:8501/?page=task3 (recomendado)
- **Individual:** http://localhost:8503

### ⭐ Melhorias Recentes
- **🔧 Correção Total:** Resolvido erro `'PandasThen' object has no attribute '_evaluate_output_names'`
- **🚀 Arquitetura Híbrida:** Versão estável integrada no sistema principal
- **🛡️ Operações Seguras:** Substituição de operações Pandas complexas por Python básico
- **📊 Análise Robusta:** Sistema de contagem manual ultra-compatível

---

## 🎮 SIMULAÇÕES SIMPY: Modelagem e Simulação

> **Título da Aplicação:** "🎮 Simulações SimPy"  
> **Localização:** `simulacoes/`

### 🎯 O que faz
Sistema avançado de simulação usando **SimPy** para modelar comportamento de checkouts, prever falhas e testar cenários de melhoria com análise de ROI.

### 🚀 Como executar
```bash
# Navegar para o diretório
cd simulacoes

# Executar aplicação
streamlit run app.py
```

### ✨ Principais funcionalidades
- **🛒 Simulação de Checkouts**: Modelagem de filas, tempos de atendimento e capacidade
- **🚨 Simulação de Anomalias**: Falhas de hardware, software, rede e problemas ambientais
- **🔍 Análise de Cenários**: Comparação entre situação atual vs melhorias propostas
- **📊 Comparação Real vs Simulado**: Validação de modelos com dados reais
- **💰 Análise de ROI**: Cálculo de retorno sobre investimento para melhorias
- **📈 Métricas Avançadas**: MTBF, disponibilidade, satisfação do cliente
- **🎯 Recomendações Inteligentes**: Sugestões baseadas em simulações
- **⏰ Simulação Temporal**: Padrões de uso por hora, detecção de picos

### 🔧 Módulos SimPy
- **CheckoutSimulation**: Modelagem de filas e processos de atendimento
- **AnomalySimulation**: Simulação de falhas com distribuições estatísticas
- **ScenarioSimulation**: Análise de cenários what-if com ROI

### 🎮 Tipos de Simulação
1. **🛒 Checkouts**: Filas, tempos de espera, utilização, eficiência
2. **🚨 Anomalias**: Hardware, software, rede, energia, ambiente
3. **🔍 Cenários**: Atual, melhorado, redundância, manutenção, upgrade
4. **📊 Validação**: Comparação com dados reais SQLite

### 📍 Acesso Local
http://localhost:8504

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

## 🛠️ Stack Tecnológico

### 🐍 Backend & Análise
- **Python 3.9+**: Linguagem principal
- **Pandas**: Manipulação de dados com operações seguras
- **SQLite**: Banco de dados leve e eficiente
- **NumPy**: Computação numérica

### 🎨 Frontend & Visualização
- **Streamlit**: Framework web interativo
- **Plotly**: Gráficos interativos avançados
- **Matplotlib**: Visualizações estatísticas
- **HTML/CSS**: Customização de interface

### 🔗 Integração & Comunicação
- **Twilio**: Envio de SMS (opcional)
- **SimPy**: Simulação de sistemas
- **Git**: Controle de versão

### 🏗️ Arquitetura
- **MVC Pattern**: Separação de responsabilidades
- **Microserviços**: Cada tarefa como módulo independente
- **Sistema Unificado**: Ponto de entrada centralizado
- **Fallback Systems**: Múltiplas camadas de recuperação

---

## 📊 Resumo das Funcionalidades

| Tarefa | Aplicação | Foco Principal | Status | Tecnologia Destaque |
|--------|-----------|----------------|---------|---------------------|
| **1** | 📊 Análise Avançada | Detecção de anomalias em checkouts | ✅ Estável | SQLite + Plotly + Análise Inteligente |
| **2** | 🚨 Alertas e Incidentes | Dashboard de monitoramento | ✅ Estável | Interface Moderna + Alertas |
| **3** | 📱 Monitoramento Integrado | Central unificada multi-database | 🔧 **Corrigido** | Python Ultra-Robusto + SQLite |
| **4** | 🎮 Simulações SimPy | Modelagem e análise de cenários | ✅ Estável | SimPy + ROI Calculator |

---

## 📝 Informações Importantes

- **📊 Dados**: Arquivos CSV incluídos para demonstração
- **💾 Bancos**: SQLite criados automaticamente  
- **� Credenciais**: Configure `credenciais.py` apenas para SMS (Tarefa 3)
- **🌐 Portas**: Cada aplicação usa uma porta diferente
- **� Responsivo**: Todas as interfaces adaptam ao mobile

---

## 🔧 Troubleshooting

### ❌ Problemas Comuns e Soluções

#### **Error: 'PandasThen' object has no attribute '_evaluate_output_names'**
- **Causa:** Incompatibilidade entre versões do Pandas e operações complexas
- **Solução:** ✅ **RESOLVIDO** - Use o sistema unificado (`streamlit run main.py`)
- **Alternativa:** Operações básicas Python foram implementadas como fallback

#### **Erro de porta já em uso**
```bash
# Parar todos os processos Streamlit
pkill -9 -f streamlit

# Verificar portas em uso
lsof -i :8501

# Usar porta específica
streamlit run main.py --server.port 8502
```

#### **Erro de importação de módulos**
```bash
# Verificar ambiente virtual ativo
which python

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Limpar cache
pip cache purge
```

#### **Problemas com SQLite**
- **Erro:** Database locked ou arquivo não encontrado
- **Solução:** Verificar permissões de arquivo e fechar conexões
```bash
# Verificar se arquivos SQLite existem
ls -la *.db */data*.db

# Testar conexão
python -c "import sqlite3; conn = sqlite3.connect('data.db'); print('OK')"
```

#### **Interface não carrega ou apresenta erro 500**
1. **Verifique o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   which python
   ```

2. **Atualize o Streamlit:**
   ```bash
   pip install streamlit --upgrade
   ```

3. **Use modo debug:**
   ```bash
   streamlit run main.py --logger.level=debug
   ```

### 🚀 Dicas de Performance
- **Use o sistema unificado** (`main.py`) para melhor estabilidade
- **Task 3 integrada** evita problemas de contexto de execução
- **Dados limitados** com LIMIT nas queries SQLite para melhor performance
- **Fallbacks automáticos** garantem funcionamento mesmo com problemas

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

## 🎯 DESTAQUE: TAREFA 3 TOTALMENTE CORRIGIDA

### 📊 Central de Monitoramento Ultra-Estável
A **Tarefa 3** foi **completamente corrigida e reformulada** como **solução definitiva**:

- **🔧 Problema Resolvido**: Eliminado erro `'PandasThen' object has no attribute '_evaluate_output_names'`
- **🚀 Arquitetura Híbrida**: Versão estável integrada no sistema principal
- **🔗 Integra Tarefas 1 + 2**: Monitora todos os dados SQLite em uma interface unificada
- **🛡️ Ultra-Robusta**: Operações básicas Python para máxima compatibilidade
- **🎮 Interface Moderna**: Design profissional com visualizações avançadas  
- **🚨 Alertas Inteligentes**: Detecção automática cross-datasets
- **📊 Dashboard Consolidado**: Métricas consolidadas de todas as fontes
- **💡 Análise Segura**: Sistema de contagem manual livre de conflitos de versão

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

### 🆕 Versão 2.3 (Outubro 2025) - Correção Total da Task 3
- **🔧 Resolução Definitiva:** Corrigido erro `'PandasThen' object has no attribute '_evaluate_output_names'`
- **🚀 Arquitetura Híbrida:** Task 3 integrada diretamente no sistema principal para máxima estabilidade
- **🛡️ Operações Ultra-Robustas:** Substituição de operações Pandas complexas por Python básico
- **📊 Análise Manual:** Sistema de contagem e análise usando iteração Python pura
- **⚡ Performance Otimizada:** Carregamento de dados com LIMIT para melhor performance
- **🔄 Fallbacks Automáticos:** Sistema defensivo com múltiplos níveis de recuperação
- **💾 Dados Reais:** Integração funcional com bancos SQLite reais
- **🎯 Compatibilidade Total:** Solução universal compatível com todas as versões do Pandas

### 🆕 Versão 2.2 (Outubro 2025) - Simulações SimPy
- **🎮 SimPy Integration:** Sistema completo de simulação e modelagem
- **🛒 Checkout Simulation:** Modelagem de filas e tempos de atendimento
- **🚨 Anomaly Simulation:** Simulação de falhas (hardware, software, rede)
- **🔍 Scenario Analysis:** Análise de cenários what-if com ROI
- **📊 Real vs Simulated:** Comparação e validação de modelos
- **💰 ROI Calculator:** Análise financeira de melhorias propostas
- **🎯 Smart Recommendations:** Recomendações baseadas em simulações

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
