# 🎮 Sistema de Simulações SimPy

## 📋 Visão Geral

Este módulo implementa simulações discretas de eventos usando **SimPy** para modelar e analisar diferentes aspectos de sistemas de checkout e suas anomalias.

## 🚀 Como Executar

### Método 1: Script Automático (Recomendado)
```bash
# No diretório raiz do projeto
./start_system.sh
```

### Método 2: Manual
```bash
# Terminal 1 - Aplicação Principal
streamlit run main.py --server.port 8512

# Terminal 2 - Simulações
cd simulacoes
streamlit run app.py --server.port 8511
```

## 🎯 Tipos de Simulação

### 1. 🛒 Simulação de Checkouts
**Objetivo:** Modelar filas e tempos de espera em checkouts

**Parâmetros:**
- `checkout1_capacity`: Capacidade do checkout 1 (1-5)
- `checkout2_capacity`: Capacidade do checkout 2 (1-5)  
- `service_time_multiplier`: Multiplicador de tempo do checkout 2 (1.0-5.0)
- `duration_hours`: Duração da simulação (1-48 horas)

**Métricas Geradas:**
- Tempo de espera médio/máximo
- Utilização dos checkouts
- Distribuição de transações por hora
- Número total de clientes atendidos

### 2. 🚨 Simulação de Anomalias
**Objetivo:** Modelar falhas de sistema e processos de recuperação

**Parâmetros:**
- `mtbf_checkout1`: MTBF do checkout 1 (4-24 horas)
- `mtbf_checkout2`: MTBF do checkout 2 (2-16 horas)
- `network_failure_rate`: Taxa de falha da rede (0-20%)
- `duration_hours`: Duração da simulação

**Métricas Geradas:**
- Timeline de eventos (falhas/reparos)
- Frequência de falhas por componente
- Tempo de downtime total
- Eventos de rede vs hardware

### 3. 🔍 Análise de Cenários
**Objetivo:** Comparar diferentes configurações operacionais

**Cenários Predefinidos:**
- **Normal**: Configuração padrão (C1: cap=1, C2: cap=1, mult=2.0)
- **Otimizado**: Melhor performance (C1: cap=2, C2: cap=1, mult=1.5)
- **Sobrecarga**: Teste de stress (C1: cap=1, C2: cap=1, mult=3.0)

**Métricas Comparativas:**
- Tempos de espera entre cenários
- Utilização relativa dos checkouts
- Throughput de clientes
- Análise de trade-offs

### 4. 📊 Comparação Real vs Simulado
**Objetivo:** Validar modelos de simulação com dados reais

**Funcionalidades:**
- Carregamento de dados históricos
- Execução de simulação equivalente
- Comparação visual de métricas
- Análise de aderência do modelo

## 📊 Interpretação de Resultados

### ✅ Indicadores Positivos
- **Tempo de espera < 5 min**: Sistema eficiente
- **Utilização 70-85%**: Balanceamento ideal
- **Distribuição equilibrada**: Checkouts bem utilizados

### ⚠️ Indicadores de Atenção
- **Tempo de espera 5-10 min**: Necessita otimização
- **Utilização > 90%**: Próximo da saturação
- **Picos de demanda**: Considerar capacidade adicional

### 🚨 Indicadores Críticos
- **Tempo de espera > 15 min**: Sistema sobrecarregado
- **Utilização > 95%**: Saturação crítica
- **Falhas frequentes**: Revisar manutenção

## 🔧 Configurações Recomendadas

### Para Testes Rápidos
```python
duration_hours = 2
checkout1_capacity = 1
checkout2_capacity = 1
service_time_multiplier = 2.0
```

### Para Análise Detalhada
```python
duration_hours = 24
checkout1_capacity = 2
checkout2_capacity = 1
service_time_multiplier = 1.5
```

### Para Teste de Stress
```python
duration_hours = 8
checkout1_capacity = 1
checkout2_capacity = 1
service_time_multiplier = 4.0
```

## 💡 Boas Práticas

### ⏱️ Gerenciamento de Tempo
1. **Testes iniciais**: Use 1-2 horas
2. **Análises padrão**: Use 8-12 horas
3. **Estudos detalhados**: Use 24+ horas

### 🎛️ Configuração de Parâmetros
1. **Comece com valores padrão**
2. **Ajuste um parâmetro por vez**
3. **Compare resultados sistematicamente**
4. **Documente configurações bem-sucedidas**

### 📈 Análise de Resultados
1. **Foque em tendências, não valores únicos**
2. **Compare múltiplas execuções**
3. **Valide com dados reais quando possível**
4. **Considere variabilidade estatística**

## 🛠️ Troubleshooting

### Problema: Simulação não carrega
**Solução:**
```bash
cd simulacoes
source ../.venv/bin/activate
streamlit run app.py --server.port 8511
```

### Problema: Erro de importação SimPy
**Solução:**
```bash
pip install simpy==4.1.1
```

### Problema: Performance lenta
**Soluções:**
- Reduza `duration_hours`
- Feche outras abas do navegador
- Use parâmetros menores para capacidade

### Problema: Porta ocupada
**Solução:**
```bash
pkill -f streamlit
# Aguarde 2-3 segundos
streamlit run app.py --server.port 8511
```

## 📚 Referências Técnicas

- **SimPy Documentation**: https://simpy.readthedocs.io/
- **Discrete Event Simulation**: Conceitos fundamentais
- **Queueing Theory**: Base matemática para filas
- **Performance Analysis**: Metodologias de análise

## 🔄 Desenvolvimento e Contribuição

### Estrutura do Código
```
simulacoes/
├── app.py                 # Interface principal
├── README.md             # Esta documentação
└── backup/               # Versões anteriores
```

### Adicionando Novas Simulações
1. Crie nova classe herdando padrões SimPy
2. Implemente método `run_simulation()`
3. Adicione na interface principal
4. Teste com parâmetros variados
5. Documente parâmetros e resultados

---

**📧 Para dúvidas técnicas ou sugestões, consulte a documentação principal do projeto.**