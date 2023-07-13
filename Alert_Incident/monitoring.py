import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


class DataLoader:
    def __init__(self, file_path, columns):
        self.file_path = file_path
        self.columns = columns

    def load_data(self):
        df = pd.read_csv(self.file_path, names=self.columns)
        return df


class TransactionsDataLoader(DataLoader):
    def __init__(self, file_path, columns):
        super().__init__(file_path, columns)

    def load_data(self):
        df = super().load_data()
        if df['time'].dtype != 'datetime64[ns]':
            df['time'] = pd.to_datetime(
                df['time'], format="%Hh %M", errors='coerce'
                )
        return df


class Transactions1DataLoader(TransactionsDataLoader):
    def __init__(self, file_path):
        columns = ['time', 'status', 'transacoes']
        super().__init__(file_path, columns)


class Transactions2DataLoader(TransactionsDataLoader):
    def __init__(self, file_path):
        columns = ['time', 'status', 'count']
        super().__init__(file_path, columns)


class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination)

    def train_model(self, df, column_name):
        label_encoder = LabelEncoder()
        df[column_name] = label_encoder.fit_transform(df[column_name])
        self.model.fit(df[[column_name]])

    def generate_alerts(self, df, column_name):
        df['anomaly'] = self.model.predict(df[[column_name]])
        anomalies = df[df['anomaly'] == -1]
        return anomalies


class RuleBasedAlerts:
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def check_alerts(self, df):
        failed_transactions = df[df['status'] == 'failed']
        reversed_transactions = df[df['status'] == 'reversed']
        denied_transactions = df[df['status'] == 'denied']

        alerts = []
        if len(failed_transactions) > len(df) * self.threshold:
            alerts.append("High number of failed transactions")
        if len(reversed_transactions) > len(df) * self.threshold:
            alerts.append("High number of reversed transactions")
        if len(denied_transactions) > len(df) * self.threshold:
            alerts.append("High number of denied transactions")

        return alerts


class Plotter:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 6))

    def plot_data(self, df, column_name):
        plt.plot(df['time'], df[column_name])
        plt.xlabel('Time')
        plt.ylabel('Transaction Count')
        plt.title('Real-time Transaction Data')
        plt.xticks(rotation=45)
        st.pyplot(self.fig)


def main():
    # Load and preprocess data from transactions_1.csv
    loader1 = Transactions1DataLoader('data/transactions_1.csv')
    df1 = loader1.load_data()

    # Train the anomaly detection model for transactions_1.csv
    detector1 = AnomalyDetector()
    detector1.train_model(df1, 'transacoes')

    # Generate alerts for anomalies in transactions_1.csv
    anomalies1 = detector1.generate_alerts(df1, 'transacoes')
    if not anomalies1.empty:
        st.warning("Anomalies Detected in transactions_1.csv:")
        st.dataframe(anomalies1)

    # Rule-based alerts for transactions_1.csv
    rule_alerts1 = RuleBasedAlerts()
    alerts1 = rule_alerts1.check_alerts(df1)
    if alerts1:
        st.warning("Alerts in transactions_1.csv:")
        st.write(alerts1)

    # Plot real-time transaction data for transactions_1.csv
    plotter1 = Plotter()
    plotter1.plot_data(df1, 'transacoes')

    # Load and preprocess data from transactions_2.csv
    loader2 = Transactions2DataLoader('data/transactions_2.csv')
    df2 = loader2.load_data()

    # Train the anomaly detection model for transactions_2.csv
    detector2 = AnomalyDetector()
    detector2.train_model(df2, 'count')

    # Generate alerts for anomalies in transactions_2.csv
    anomalies2 = detector2.generate_alerts(df2, 'count')
    if not anomalies2.empty:
        st.warning("Anomalies Detected in transactions_2.csv:")
        st.dataframe(anomalies2)

    # Rule-based alerts for transactions_2.csv
    rule_alerts2 = RuleBasedAlerts()
    alerts2 = rule_alerts2.check_alerts(df2)
    if alerts2:
        st.warning("Alerts in transactions_2.csv:")
        st.write(alerts2)

    # Plot real-time transaction data for transactions_2.csv
    plotter2 = Plotter()
    plotter2.plot_data(df2, 'count')


if __name__ == '__main__':
    main()
