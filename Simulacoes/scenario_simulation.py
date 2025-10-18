import simpy
import random
import pandas as pd
import numpy as np
from checkout_simulation import CheckoutSimulation
from anomaly_simulation import AnomalySimulation


class ScenarioSimulation:
    """
    Simulação de diferentes cenários para análise de melhorias
    """
    
    def __init__(self):
        """
        Inicializa a simulação de cenários
        """
        self.scenarios = {
            'current': {
                'name': 'Cenário Atual',
                'description': 'Situação atual dos checkouts',
                'checkout1_capacity': 1,
                'checkout2_capacity': 1,
                'mtbf_checkout1': 12,
                'mtbf_checkout2': 6,
                'service_time_multiplier': 2.0,
                'maintenance_schedule': False,
                'backup_system': False,
                'cost': 0
            },
            'improved': {
                'name': 'Cenário Melhorado',
                'description': 'Checkout 2 reparado e otimizado',
                'checkout1_capacity': 1,
                'checkout2_capacity': 1,
                'mtbf_checkout1': 12,
                'mtbf_checkout2': 12,  # Melhorado
                'service_time_multiplier': 1.2,  # Muito melhor
                'maintenance_schedule': True,
                'backup_system': False,
                'cost': 5000  # Custo do reparo
            },
            'redundancy': {
                'name': 'Cenário com Redundância',
                'description': 'Sistema com checkout backup',
                'checkout1_capacity': 2,  # Checkout backup
                'checkout2_capacity': 1,
                'mtbf_checkout1': 12,
                'mtbf_checkout2': 6,
                'service_time_multiplier': 2.0,
                'maintenance_schedule': False,
                'backup_system': True,
                'cost': 15000  # Custo do checkout adicional
            },
            'maintenance': {
                'name': 'Manutenção Preventiva',
                'description': 'Programa de manutenção preventiva',
                'checkout1_capacity': 1,
                'checkout2_capacity': 1,
                'mtbf_checkout1': 16,  # Melhor devido à manutenção
                'mtbf_checkout2': 10,  # Melhor devido à manutenção
                'service_time_multiplier': 1.8,  # Ligeiramente melhor
                'maintenance_schedule': True,
                'backup_system': False,
                'cost': 2000  # Custo anual de manutenção
            },
            'full_upgrade': {
                'name': 'Upgrade Completo',
                'description': 'Todos os checkouts novos + redundância',
                'checkout1_capacity': 2,
                'checkout2_capacity': 2,
                'mtbf_checkout1': 20,
                'mtbf_checkout2': 20,
                'service_time_multiplier': 1.0,  # Performance igual
                'maintenance_schedule': True,
                'backup_system': True,
                'cost': 30000  # Investimento alto
            }
        }
    
    def run_scenario(self, scenario_name, duration_hours=24):
        """
        Executa um cenário específico
        
        Args:
            scenario_name: Nome do cenário
            duration_hours: Duração da simulação
            
        Returns:
            Dict com resultados do cenário
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Cenário '{scenario_name}' não encontrado")
        
        scenario = self.scenarios[scenario_name]
        
        # Executar simulação de checkouts
        checkout_sim = CheckoutSimulation(
            checkout1_capacity=scenario['checkout1_capacity'],
            checkout2_capacity=scenario['checkout2_capacity'],
            service_time_multiplier=scenario['service_time_multiplier']
        )
        
        transactions_df = checkout_sim.run_simulation(duration_hours)
        
        # Executar simulação de anomalias
        anomaly_sim = AnomalySimulation(
            mtbf_checkout1=scenario['mtbf_checkout1'],
            mtbf_checkout2=scenario['mtbf_checkout2']
        )
        
        anomalies_df = anomaly_sim.run_simulation(duration_hours)
        
        # Calcular métricas do cenário
        metrics = self.calculate_scenario_metrics(
            transactions_df, anomalies_df, scenario
        )
        
        return {
            'scenario': scenario,
            'transactions': transactions_df,
            'anomalies': anomalies_df,
            'metrics': metrics
        }
    
    def run_all_scenarios(self, duration_hours=24):
        """
        Executa todos os cenários
        
        Args:
            duration_hours: Duração da simulação
            
        Returns:
            Dict com resultados de todos os cenários
        """
        results = {}
        
        for scenario_name in self.scenarios.keys():
            print(f"🎯 Executando cenário: {scenario_name}")
            results[scenario_name] = self.run_scenario(scenario_name, duration_hours)
        
        return results
    
    def calculate_scenario_metrics(self, transactions_df, anomalies_df, scenario):
        """
        Calcula métricas para um cenário
        
        Args:
            transactions_df: DataFrame com transações
            anomalies_df: DataFrame com anomalias
            scenario: Configuração do cenário
            
        Returns:
            Dict com métricas calculadas
        """
        metrics = {}
        
        # Métricas de transações
        if not transactions_df.empty:
            metrics['total_customers'] = len(transactions_df)
            metrics['avg_wait_time'] = transactions_df['wait_time'].mean()
            metrics['max_wait_time'] = transactions_df['wait_time'].max()
            metrics['avg_service_time'] = transactions_df['service_time'].mean()
            metrics['checkout1_usage'] = (
                len(transactions_df[transactions_df['checkout'] == 1]) / 
                len(transactions_df)
            )
            metrics['system_efficiency'] = transactions_df['efficiency'].mean()
        else:
            metrics.update({
                'total_customers': 0,
                'avg_wait_time': 0,
                'max_wait_time': 0,
                'avg_service_time': 0,
                'checkout1_usage': 0,
                'system_efficiency': 0
            })
        
        # Métricas de anomalias
        if not anomalies_df.empty:
            metrics['total_anomalies'] = len(anomalies_df)
            metrics['total_downtime'] = anomalies_df['duration'].sum()
            metrics['critical_incidents'] = len(
                anomalies_df[anomalies_df['severity'] == 'critical']
            )
            metrics['avg_impact_score'] = anomalies_df['impact_score'].mean()
        else:
            metrics.update({
                'total_anomalies': 0,
                'total_downtime': 0,
                'critical_incidents': 0,
                'avg_impact_score': 0
            })
        
        # Calcular disponibilidade do sistema
        total_time = 24 * 60  # 24 horas em minutos
        downtime = metrics['total_downtime']
        metrics['availability'] = ((total_time - downtime) / total_time) * 100
        
        # Métricas de negócio
        metrics['revenue_loss'] = self.calculate_revenue_loss(
            downtime, metrics['avg_wait_time']
        )
        metrics['customer_satisfaction'] = self.calculate_satisfaction(
            metrics['avg_wait_time'], metrics['availability']
        )
        
        # Custo do cenário
        metrics['implementation_cost'] = scenario['cost']
        
        return metrics
    
    def calculate_revenue_loss(self, downtime_minutes, avg_wait_time):
        """
        Calcula perda de receita estimada
        
        Args:
            downtime_minutes: Tempo total de indisponibilidade
            avg_wait_time: Tempo médio de espera
            
        Returns:
            Perda de receita em R$
        """
        # Premissas de negócio
        avg_transaction_value = 50.0  # R$ 50 por transação
        transactions_per_hour = 30    # 30 transações por hora
        
        # Perda por downtime completo
        downtime_hours = downtime_minutes / 60
        direct_loss = downtime_hours * transactions_per_hour * avg_transaction_value
        
        # Perda por clientes que desistem devido à espera
        # Assume que clientes desistem se espera > 15 min
        if avg_wait_time > 15:
            abandonment_rate = min(0.5, (avg_wait_time - 15) / 30)
            abandonment_loss = (24 * transactions_per_hour * 
                              avg_transaction_value * abandonment_rate)
        else:
            abandonment_loss = 0
        
        return direct_loss + abandonment_loss
    
    def calculate_satisfaction(self, avg_wait_time, availability):
        """
        Calcula índice de satisfação do cliente (0-100)
        
        Args:
            avg_wait_time: Tempo médio de espera
            availability: Disponibilidade do sistema
            
        Returns:
            Índice de satisfação (0-100)
        """
        # Score baseado no tempo de espera
        if avg_wait_time <= 5:
            wait_score = 100
        elif avg_wait_time <= 10:
            wait_score = 80
        elif avg_wait_time <= 20:
            wait_score = 60
        else:
            wait_score = max(20, 100 - avg_wait_time * 2)
        
        # Score baseado na disponibilidade
        availability_score = availability
        
        # Média ponderada (60% espera, 40% disponibilidade)
        satisfaction = (wait_score * 0.6) + (availability_score * 0.4)
        
        return min(100, max(0, satisfaction))
    
    def calculate_roi(self, scenario_results):
        """
        Calcula ROI para cada cenário
        
        Args:
            scenario_results: Resultados de todos os cenários
            
        Returns:
            Dict com ROI de cada cenário
        """
        roi_data = {}
        baseline = scenario_results['current']['metrics']
        baseline_loss = baseline['revenue_loss']
        
        for scenario_name, results in scenario_results.items():
            metrics = results['metrics']
            
            # Redução na perda de receita
            loss_reduction = baseline_loss - metrics['revenue_loss']
            
            # Custo de implementação
            implementation_cost = metrics['implementation_cost']
            
            # ROI anual (assumindo que benefícios se mantêm)
            annual_savings = loss_reduction * 365  # Por dia * 365 dias
            
            if implementation_cost > 0:
                roi = ((annual_savings - implementation_cost) / 
                       implementation_cost) * 100
            else:
                roi = 0  # Cenário atual (baseline)
            
            roi_data[scenario_name] = roi
        
        return roi_data
    
    def get_recommendations(self, scenario_results):
        """
        Gera recomendações baseadas nos resultados
        
        Args:
            scenario_results: Resultados de todos os cenários
            
        Returns:
            Lista de recomendações
        """
        recommendations = []
        
        # Analisar métricas
        current_metrics = scenario_results['current']['metrics']
        
        # Recomendações baseadas em problemas identificados
        if current_metrics['avg_wait_time'] > 10:
            recommendations.append(
                "⏰ Tempo de espera alto detectado. "
                "Considere melhorar a eficiência do Checkout 2."
            )
        
        if current_metrics['availability'] < 95:
            recommendations.append(
                "📉 Disponibilidade baixa. "
                "Implemente manutenção preventiva para reduzir falhas."
            )
        
        if current_metrics['checkout1_usage'] > 0.7:
            recommendations.append(
                "⚖️ Desbalanceamento entre checkouts. "
                "Melhore o Checkout 2 para distribuir melhor a carga."
            )
        
        # Recomendação de melhor cenário
        roi_data = self.calculate_roi(scenario_results)
        best_scenario = max(roi_data, key=roi_data.get)
        
        if best_scenario != 'current' and roi_data[best_scenario] > 50:
            scenario_name = scenario_results[best_scenario]['scenario']['name']
            recommendations.append(
                f"💰 Melhor investimento: {scenario_name} "
                f"(ROI: {roi_data[best_scenario]:.1f}%)"
            )
        
        # Recomendações específicas por cenário
        if roi_data.get('maintenance', 0) > 100:
            recommendations.append(
                "🔧 Manutenção preventiva tem ROI excelente. "
                "Implemente imediatamente."
            )
        
        if roi_data.get('improved', 0) > 200:
            recommendations.append(
                "🚀 Reparo do Checkout 2 é crítico. "
                "Prioridade máxima de implementação."
            )
        
        return recommendations
    
    def export_comparison(self, scenario_results, filename="scenario_comparison.csv"):
        """
        Exporta comparação de cenários para CSV
        
        Args:
            scenario_results: Resultados dos cenários
            filename: Nome do arquivo
        """
        comparison_data = []
        
        for scenario_name, results in scenario_results.items():
            scenario = results['scenario']
            metrics = results['metrics']
            
            row = {
                'scenario': scenario_name,
                'name': scenario['name'],
                'description': scenario['description'],
                'cost': scenario['cost'],
                **metrics
            }
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        df.to_csv(filename, index=False)
        print(f"✅ Comparação exportada para {filename}")
        
        return df