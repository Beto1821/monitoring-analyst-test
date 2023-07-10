# Projeto monitoring-analyst-test

# Crie o ambiente virtual para o projeto
python3 -m venv .venv && source .venv/bin/activate

# Instale as dependências
python3 -m pip install -r requirements.txt

# Rodando o app para geração dos gráficos
streamlit run app.py