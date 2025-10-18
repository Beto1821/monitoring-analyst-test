#!/bin/bash

# Script para iniciar ambas as aplicações do sistema de monitoramento

echo "🚀 Iniciando Sistema de Monitoramento Completo..."

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source .venv/bin/activate

# Parar aplicações que possam estar rodando
echo "🛑 Parando aplicações anteriores..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# Iniciar aplicação principal (main.py) na porta 8512
echo "🏠 Iniciando aplicação principal na porta 8512..."
streamlit run main.py --server.port 8512 &
MAIN_PID=$!
sleep 3

# Iniciar aplicação de simulações na porta 8511
echo "🎮 Iniciando aplicação de simulações na porta 8511..."
cd simulacoes
streamlit run app.py --server.port 8511 &
SIM_PID=$!
cd ..
sleep 3

# Verificar se ambas as aplicações estão rodando
echo "🔍 Verificando status das aplicações..."

if lsof -i :8512 > /dev/null 2>&1; then
    echo "✅ Aplicação principal rodando na porta 8512"
    echo "   🌐 Acesse: http://localhost:8512"
else
    echo "❌ Falha ao iniciar aplicação principal"
fi

if lsof -i :8511 > /dev/null 2>&1; then
    echo "✅ Aplicação de simulações rodando na porta 8511"
    echo "   🌐 Acesse: http://localhost:8511"
else
    echo "❌ Falha ao iniciar aplicação de simulações"
fi

echo ""
echo "🎯 SISTEMA INICIADO COM SUCESSO!"
echo "📱 Aplicação Principal: http://localhost:8512"
echo "🎮 Simulações: http://localhost:8511"
echo ""
echo "💡 Para parar as aplicações: pkill -f streamlit"
echo "📖 Para logs: verificar os terminais ou usar 'ps aux | grep streamlit'"

# Manter o script rodando para monitorar os processos
echo "⌛ Pressione Ctrl+C para parar todas as aplicações..."
trap 'echo "🛑 Parando aplicações..."; pkill -f streamlit; exit 0' INT

# Loop infinito para manter o script ativo
while true; do
    sleep 10
    # Verificar se as aplicações ainda estão rodando
    if ! lsof -i :8512 > /dev/null 2>&1; then
        echo "⚠️  Aplicação principal parou de funcionar"
    fi
    if ! lsof -i :8511 > /dev/null 2>&1; then
        echo "⚠️  Aplicação de simulações parou de funcionar" 
    fi
done