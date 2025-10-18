import simpy
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class AnomalySimulation:
    """
    Simulação de anomalias nos checkouts usando SimPy
    """
    
    def __init__(self, mtbf_checkout1=12, mtbf_checkout2=6, 
                 network_failure_rate=0.05):
        """
        Inicializa a simulação de anomalias
        
        Args:
            mtbf_checkout1: Mean Time Between Failures para Checkout 1 (horas)
            mtbf_checkout2: Mean Time Between Failures para Checkout 2 (horas)
            network_failure_rate: Taxa de falha de rede (0-1)
        """
        self.env = simpy.Environment()
        self.mtbf_checkout1 = mtbf_checkout1
        self.mtbf_checkout2 = mtbf_checkout2
        self.network_failure_rate = network_failure_rate
        self.anomaly_log = []
        self.anomaly_id_counter = 0
        
    def hardware_failure(self, checkout_id, mtbf):
        """
        Simula falhas de hardware usando distribuição exponencial
        
        Args:
            checkout_id: ID do checkout (1 ou 2)
            mtbf: Mean Time Between Failures em horas
        """
        while True:
            # Tempo até próxima falha (distribuição exponencial)
            time_to_failure = random.expovariate(1 / (mtbf * 60))  # Converter para minutos
            yield self.env.timeout(time_to_failure)
            
            # Duração da falha (30 min a 4 horas)
            failure_duration = random.uniform(30, 240)
            
            # Severidade baseada na duração
            if failure_duration > 180:
                severity = 'critical'
            elif failure_duration > 90:
                severity = 'major'
            else:
                severity = 'minor'
            
            # Registrar anomalia
            self.log_anomaly(
                anomaly_type='hardware_failure',
                checkout=checkout_id,
                start_time=self.env.now,
                duration=failure_duration,
                severity=severity,
                description=f"Falha de hardware no Checkout {checkout_id}"
            )
            
            # Simular tempo de reparo
            yield self.env.timeout(failure_duration)
    
    def software_glitch(self, checkout_id):
        """
        Simula problemas de software/sistema
        
        Args:
            checkout_id: ID do checkout (1 ou 2)
        """
        while True:
            # Intervalo entre verificações (30min a 2h)
            yield self.env.timeout(random.uniform(30, 120))
            
            # Probabilidade de glitch (5-15% dependendo do checkout)
            glitch_probability = 0.05 if checkout_id == 1 else 0.15
            
            if random.random() < glitch_probability:
                # Duração do glitch (5 min a 45 min)
                glitch_duration = random.uniform(5, 45)
                
                # Tipo de problema
                problem_types = [
                    'sistema_lento',
                    'erro_comunicacao',
                    'timeout_rede',
                    'bug_software',
                    'memoria_insuficiente'
                ]
                
                problem_type = random.choice(problem_types)
                
                # Severidade baseada no tipo e duração
                if glitch_duration > 30 or problem_type in ['erro_comunicacao', 'bug_software']:
                    severity = 'major'
                elif glitch_duration > 15:
                    severity = 'warning'
                else:
                    severity = 'minor'
                
                self.log_anomaly(
                    anomaly_type='software_glitch',
                    checkout=checkout_id,
                    start_time=self.env.now,
                    duration=glitch_duration,
                    severity=severity,
                    description=f"{problem_type.replace('_', ' ').title()} no Checkout {checkout_id}",
                    details={'problem_type': problem_type}
                )
                
                yield self.env.timeout(glitch_duration)
    
    def network_issue(self):
        """
        Simula problemas de rede que afetam todo o sistema
        """
        while True:
            # Verificar rede a cada 1-4 horas
            yield self.env.timeout(random.uniform(60, 240))
            
            if random.random() < self.network_failure_rate:
                # Duração do problema de rede (10 min a 2 horas)
                outage_duration = random.uniform(10, 120)
                
                # Tipo de problema de rede
                network_issues = [
                    'perda_conectividade',
                    'latencia_alta',
                    'timeout_servidor',
                    'sobrecarga_rede',
                    'falha_dns'
                ]
                
                issue_type = random.choice(network_issues)
                
                # Severidade baseada na duração e tipo
                if outage_duration > 60 or issue_type == 'perda_conectividade':
                    severity = 'critical'
                elif outage_duration > 30:
                    severity = 'major'
                else:
                    severity = 'warning'
                
                self.log_anomaly(
                    anomaly_type='network_issue',
                    checkout='both',
                    start_time=self.env.now,
                    duration=outage_duration,
                    severity=severity,
                    description=f"Problema de rede: {issue_type.replace('_', ' ')}",
                    details={'issue_type': issue_type}
                )
                
                yield self.env.timeout(outage_duration)
    
    def power_outage(self):
        """
        Simula falhas de energia
        """
        while True:
            # Falhas de energia são raras (verificar a cada 8-24h)
            yield self.env.timeout(random.uniform(480, 1440))
            
            # Probabilidade muito baixa (1%)
            if random.random() < 0.01:
                # Duração (5 min a 3 horas)
                outage_duration = random.uniform(5, 180)
                
                severity = 'critical' if outage_duration > 60 else 'major'
                
                self.log_anomaly(
                    anomaly_type='power_outage',
                    checkout='both',
                    start_time=self.env.now,
                    duration=outage_duration,
                    severity=severity,
                    description="Falha de energia elétrica",
                    details={'backup_power': random.choice([True, False])}
                )
                
                yield self.env.timeout(outage_duration)
    
    def environmental_issue(self):
        """
        Simula problemas ambientais (temperatura, umidade)
        """
        while True:
            yield self.env.timeout(random.uniform(180, 480))  # 3-8 horas
            
            # Problemas ambientais são moderadamente raros (3%)
            if random.random() < 0.03:
                issue_duration = random.uniform(20, 90)
                
                environmental_problems = [
                    'superaquecimento',
                    'umidade_alta',
                    'temperatura_baixa',
                    'ventilacao_inadequada'
                ]
                
                problem = random.choice(environmental_problems)
                
                # Checkout mais afetado (C2 é mais sensível)
                affected_checkout = 2 if random.random() < 0.7 else 1
                
                severity = 'warning' if issue_duration < 60 else 'major'
                
                self.log_anomaly(
                    anomaly_type='environmental_issue',
                    checkout=affected_checkout,
                    start_time=self.env.now,
                    duration=issue_duration,
                    severity=severity,
                    description=f"Problema ambiental: {problem.replace('_', ' ')}",
                    details={'problem_type': problem}
                )
                
                yield self.env.timeout(issue_duration)
    
    def log_anomaly(self, anomaly_type, checkout, start_time, duration, 
                   severity, description, details=None):
        """
        Registra uma anomalia no log
        
        Args:
            anomaly_type: Tipo da anomalia
            checkout: Checkout afetado (1, 2, ou 'both')
            start_time: Tempo de início (em minutos da simulação)
            duration: Duração da anomalia (em minutos)
            severity: Severidade (critical, major, warning, minor)
            description: Descrição da anomalia
            details: Informações adicionais (dict)
        """
        end_time = start_time + duration
        
        # Converter tempo de simulação para hora do dia
        start_hour = int(start_time // 60) % 24
        end_hour = int(end_time // 60) % 24
        
        anomaly_record = {
            'anomaly_id': self.anomaly_id_counter,
            'type': anomaly_type,
            'checkout': checkout,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'severity': severity,
            'description': description,
            'details': details or {}
        }
        
        self.anomaly_log.append(anomaly_record)
        self.anomaly_id_counter += 1
        
        # Log para console se necessário
        print(f"🚨 ANOMALIA {self.anomaly_id_counter}: {description} "
              f"({start_hour:02d}h - {end_hour:02d}h, {duration:.1f}min)")
    
    def run_simulation(self, duration_hours=24):
        """
        Executa a simulação de anomalias
        
        Args:
            duration_hours: Duração da simulação em horas
            
        Returns:
            DataFrame com anomalias detectadas
        """
        # Reiniciar ambiente
        self.env = simpy.Environment()
        self.anomaly_log = []
        self.anomaly_id_counter = 0
        
        # Iniciar processos de falha para cada checkout
        self.env.process(self.hardware_failure(1, self.mtbf_checkout1))
        self.env.process(self.hardware_failure(2, self.mtbf_checkout2))
        
        # Iniciar processos de software para cada checkout
        self.env.process(self.software_glitch(1))
        self.env.process(self.software_glitch(2))
        
        # Iniciar processos do sistema
        self.env.process(self.network_issue())
        self.env.process(self.power_outage())
        self.env.process(self.environmental_issue())
        
        # Executar simulação
        self.env.run(until=duration_hours * 60)  # Converter para minutos
        
        # Converter para DataFrame
        if self.anomaly_log:
            df = pd.DataFrame(self.anomaly_log)
            
            # Adicionar colunas calculadas
            df['impact_score'] = df.apply(self.calculate_impact_score, axis=1)
            df['business_hours'] = df['start_hour'].apply(
                lambda x: 1 if 9 <= x <= 18 else 0
            )
            
            return df
        else:
            return pd.DataFrame(columns=[
                'anomaly_id', 'type', 'checkout', 'start_time', 'end_time',
                'duration', 'start_hour', 'end_hour', 'severity', 
                'description', 'details', 'impact_score', 'business_hours'
            ])
    
    def calculate_impact_score(self, anomaly_row):
        """
        Calcula score de impacto da anomalia
        
        Args:
            anomaly_row: Linha do DataFrame com dados da anomalia
            
        Returns:
            Score de impacto (0-100)
        """
        base_score = 0
        
        # Score por severidade
        severity_scores = {
            'critical': 80,
            'major': 60,
            'warning': 30,
            'minor': 10
        }
        base_score += severity_scores.get(anomaly_row['severity'], 10)
        
        # Multiplicador por duração
        if anomaly_row['duration'] > 120:  # > 2h
            base_score *= 1.5
        elif anomaly_row['duration'] > 60:  # > 1h
            base_score *= 1.2
        
        # Multiplicador por horário comercial
        if anomaly_row['business_hours']:
            base_score *= 1.3
        
        # Multiplicador por checkout afetado
        if anomaly_row['checkout'] == 'both':
            base_score *= 1.8
        elif anomaly_row['checkout'] == 2:  # C2 já é mais problemático
            base_score *= 1.1
        
        return min(100, base_score)  # Cap em 100
    
    def get_anomaly_summary(self, anomalies_df):
        """
        Gera resumo das anomalias
        
        Args:
            anomalies_df: DataFrame com anomalias
            
        Returns:
            Dict com estatísticas
        """
        if anomalies_df.empty:
            return {}
        
        summary = {
            'total_anomalies': len(anomalies_df),
            'by_severity': anomalies_df['severity'].value_counts().to_dict(),
            'by_type': anomalies_df['type'].value_counts().to_dict(),
            'by_checkout': anomalies_df['checkout'].value_counts().to_dict(),
            'avg_duration': anomalies_df['duration'].mean(),
            'total_downtime': anomalies_df['duration'].sum(),
            'business_hours_incidents': anomalies_df['business_hours'].sum(),
            'avg_impact_score': anomalies_df['impact_score'].mean(),
            'peak_impact_hour': anomalies_df.groupby('start_hour')['impact_score'].sum().idxmax()
        }
        
        return summary