import simpy
import random
import pandas as pd
import numpy as np
from datetime import datetime


class CheckoutSimulation:
    """
    Simulação de checkouts usando SimPy para modelar filas e atendimento
    """
    
    def __init__(self, checkout1_capacity=1, checkout2_capacity=1, 
                 service_time_multiplier=2.0):
        """
        Inicializa a simulação
        
        Args:
            checkout1_capacity: Capacidade do checkout 1
            checkout2_capacity: Capacidade do checkout 2  
            service_time_multiplier: Multiplicador de tempo para checkout 2
        """
        self.env = simpy.Environment()
        self.checkout1 = simpy.Resource(self.env, capacity=checkout1_capacity)
        self.checkout2 = simpy.Resource(self.env, capacity=checkout2_capacity)
        self.service_time_multiplier = service_time_multiplier
        self.transaction_log = []
        self.customer_id_counter = 0
        
    def customer_process(self, customer_id, checkout_choice, arrival_hour):
        """
        Processo de atendimento ao cliente
        
        Args:
            customer_id: ID único do cliente
            checkout_choice: 1 ou 2 (escolha do checkout)
            arrival_hour: Hora de chegada (0-23)
        """
        arrival_time = self.env.now
        
        # Escolher checkout baseado na choice
        if checkout_choice == 1:
            checkout = self.checkout1
            checkout_name = "Checkout 1"
        else:
            checkout = self.checkout2
            checkout_name = "Checkout 2"
        
        # Solicitar o recurso (checkout)
        request_start = self.env.now
        with checkout.request() as request:
            yield request
            
            service_start = self.env.now
            wait_time = service_start - request_start
            
            # Calcular tempo de serviço
            service_time = self.get_service_time(checkout_choice, arrival_hour)
            
            # Simular o atendimento
            yield self.env.timeout(service_time)
            
            completion_time = self.env.now
            
            # Log da transação
            self.transaction_log.append({
                'customer_id': customer_id,
                'checkout': checkout_choice,
                'checkout_name': checkout_name,
                'arrival_time': arrival_time,
                'service_start': service_start,
                'completion_time': completion_time,
                'service_time': service_time,
                'wait_time': wait_time,
                'hour': arrival_hour,
                'total_time': completion_time - arrival_time
            })
    
    def get_service_time(self, checkout_id, hour):
        """
        Calcula tempo de atendimento baseado no checkout e hora
        
        Args:
            checkout_id: 1 ou 2
            hour: Hora do dia (0-23)
            
        Returns:
            Tempo de serviço em minutos
        """
        # Tempo base (em minutos)
        if checkout_id == 1:
            # Checkout 1: Mais eficiente e estável
            base_time = random.uniform(2, 5)
        else:
            # Checkout 2: Pode ter problemas
            base_time = random.uniform(1.5, 4)
            
            # Simular problemas específicos no Checkout 2
            # Problema crítico entre 13h-19h (conforme dados reais)
            if 13 <= hour <= 19:
                # 30% chance de lentidão severa
                if random.random() < 0.3:
                    base_time *= self.service_time_multiplier
                # 10% chance de falha total (tempo muito alto)
                elif random.random() < 0.1:
                    base_time *= 5
            
            # Problemas menores em outros horários
            elif random.random() < 0.1:
                base_time *= 1.5
        
        return base_time
    
    def get_arrival_rate(self, hour):
        """
        Taxa de chegada de clientes baseada na hora
        
        Args:
            hour: Hora do dia (0-23)
            
        Returns:
            Intervalo entre chegadas (minutos)
        """
        # Padrão baseado em dados reais de transações
        if 9 <= hour <= 12:
            # Manhã: movimento moderado
            return random.uniform(1, 3)
        elif 13 <= hour <= 18:
            # Tarde: pico de movimento
            return random.uniform(0.5, 2)
        elif 19 <= hour <= 21:
            # Noite: movimento médio
            return random.uniform(2, 4)
        else:
            # Madrugada/início manhã: movimento baixo
            return random.uniform(5, 10)
    
    def customer_generator(self):
        """
        Gerador de clientes ao longo do dia
        """
        while True:
            # Calcular hora atual
            current_hour = int(self.env.now) % 24
            
            # Tempo até próximo cliente
            arrival_interval = self.get_arrival_rate(current_hour)
            yield self.env.timeout(arrival_interval)
            
            # Escolha do checkout (preferência por Checkout 1)
            # Baseado em dados reais: C1 é mais usado
            checkout_choice = random.choices([1, 2], weights=[0.65, 0.35])[0]
            
            # Se Checkout 2 está com problemas, mais pessoas vão para C1
            if checkout_choice == 2 and 13 <= current_hour <= 19:
                if random.random() < 0.4:  # 40% migram para C1
                    checkout_choice = 1
            
            # Criar processo do cliente
            self.env.process(
                self.customer_process(
                    self.customer_id_counter, 
                    checkout_choice, 
                    current_hour
                )
            )
            self.customer_id_counter += 1
    
    def system_monitoring(self):
        """
        Processo de monitoramento do sistema
        """
        while True:
            yield self.env.timeout(60)  # Monitorar a cada hora
            
            current_hour = int(self.env.now) % 24
            
            # Simular detecção de problemas
            if len(self.transaction_log) > 0:
                recent_transactions = [
                    t for t in self.transaction_log 
                    if t['completion_time'] > self.env.now - 60
                ]
                
                if recent_transactions:
                    # Calcular métricas
                    avg_wait = np.mean([t['wait_time'] for t in recent_transactions])
                    c2_transactions = [t for t in recent_transactions if t['checkout'] == 2]
                    
                    # Detectar anomalias
                    if avg_wait > 10:  # Espera muito alta
                        print(f"⚠️ ALERTA {current_hour:02d}h: Tempo de espera alto ({avg_wait:.1f}min)")
                    
                    if c2_transactions and len(c2_transactions) < len(recent_transactions) * 0.2:
                        print(f"🚨 ALERTA {current_hour:02d}h: Checkout 2 com baixa utilização")
    
    def run_simulation(self, duration_hours=24):
        """
        Executa a simulação
        
        Args:
            duration_hours: Duração da simulação em horas
            
        Returns:
            DataFrame com resultados
        """
        # Reiniciar ambiente
        self.env = simpy.Environment()
        self.checkout1 = simpy.Resource(self.env, capacity=self.checkout1.capacity)
        self.checkout2 = simpy.Resource(self.env, capacity=self.checkout2.capacity)
        self.transaction_log = []
        self.customer_id_counter = 0
        
        # Iniciar processos
        self.env.process(self.customer_generator())
        self.env.process(self.system_monitoring())
        
        # Executar simulação
        self.env.run(until=duration_hours * 60)  # Converter para minutos
        
        # Converter para DataFrame
        if self.transaction_log:
            df = pd.DataFrame(self.transaction_log)
            
            # Adicionar métricas calculadas
            df['efficiency'] = df['service_time'] / df['total_time']
            df['utilization'] = df.groupby(['checkout', 'hour'])['service_time'].transform('sum') / 60
            
            return df
        else:
            # Retornar DataFrame vazio se não houver transações
            return pd.DataFrame(columns=[
                'customer_id', 'checkout', 'checkout_name', 'arrival_time',
                'service_start', 'completion_time', 'service_time', 'wait_time',
                'hour', 'total_time', 'efficiency', 'utilization'
            ])
    
    def get_performance_metrics(self, results_df):
        """
        Calcula métricas de performance
        
        Args:
            results_df: DataFrame com resultados da simulação
            
        Returns:
            Dict com métricas
        """
        if results_df.empty:
            return {}
        
        metrics = {
            'total_customers': len(results_df),
            'avg_wait_time': results_df['wait_time'].mean(),
            'max_wait_time': results_df['wait_time'].max(),
            'avg_service_time': results_df['service_time'].mean(),
            'checkout1_usage': len(results_df[results_df['checkout'] == 1]) / len(results_df),
            'checkout2_usage': len(results_df[results_df['checkout'] == 2]) / len(results_df),
            'system_efficiency': results_df['efficiency'].mean(),
            'peak_hour': results_df.groupby('hour').size().idxmax()
        }
        
        return metrics
    
    def export_results(self, results_df, filename="simulation_results.csv"):
        """
        Exporta resultados para CSV
        
        Args:
            results_df: DataFrame com resultados
            filename: Nome do arquivo
        """
        results_df.to_csv(filename, index=False)
        print(f"✅ Resultados exportados para {filename}")