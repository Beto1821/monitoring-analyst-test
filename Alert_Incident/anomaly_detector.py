from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05)

    def train_model(self, df):
        self.model.fit(df[['status', 'count']])

    def generate_alerts(self, df):
        df['anomaly'] = self.model.predict(df[['status', 'count']])
        anomalies = df[df['anomaly'] == -1]
        return anomalies
