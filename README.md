# Projeto monitoring-analyst-test

# rode na raiz
# Crie o ambiente virtual para o projeto
python3 -m venv .venv && source .venv/bin/activate

# Instale as dependências
python3 -m pip install -r requirements.txt


# TAREFA 1

# Rodando o app para geração dos gráficos Tarefa 1
cd Analyze_data
streamlit run app.py

# TAREFA 2

# Rodando o app para geração dos gráficos Tarefa 1
cd Alert_Incident/
streamlit run app.py

# Monitoring

# Rodando o app para geração dos gráficos Tarefa 1
cd Monitoring/
streamlit run app.py