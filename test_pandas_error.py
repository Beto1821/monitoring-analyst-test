#!/usr/bin/env python3
"""
Teste isolado para identificar o erro do Pandas '_evaluate_output_names'
"""

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def test_pandas_operations():
    """Testa operações que podem causar o erro"""
    
    print("🔍 Testando operações do Pandas...")
    
    # Criar dados de teste
    data = {
        'status': ['approved', 'failed', 'denied', 'approved', 'failed'] * 100,
        'amount': np.random.rand(500) * 1000,
        'timestamp': pd.date_range('2024-01-01', periods=500, freq='H')
    }
    
    df = pd.DataFrame(data)
    print(f"✅ DataFrame criado: {df.shape}")
    
    # Testar operações básicas
    try:
        # 1. tolist() - deve funcionar
        status_list = df['status'].tolist()
        print(f"✅ tolist(): {len(status_list)} items")
        
        # 2. count manual - deve funcionar
        approved_count = status_list.count('approved')
        print(f"✅ count manual: {approved_count}")
        
        # 3. value_counts() - pode causar problema
        status_counts = df['status'].value_counts()
        print(f"✅ value_counts(): {status_counts}")
        
        # 4. Operações booleanas - podem causar problema
        mask = df['status'] == 'approved'
        approved_sum = mask.sum()
        print(f"✅ Boolean operation: {approved_sum}")
        
        # 5. Gráfico plotly - pode causar problema
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Test Chart"
        )
        print("✅ Plotly chart created")
        
    except Exception as e:
        print(f"❌ Erro detectado: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_pandas_operations()