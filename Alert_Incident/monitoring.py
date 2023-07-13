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


class Transactions1DataLoader(DataLoader):
    def __init__(self, file_path):
        columns = ['time', 'status', 'transacoes']
        super().__init__(file_path, columns)

    def load_data(self):
        df = super().load_data()
        if df['time'].dtype != 'datetime64[ns]':
            df['time'] = pd.to_datetime(
                df['time'], format="%Hh %M", errors='coerce'
            )
        return df


class Transactions2DataLoader(DataLoader):
    def __init__(self, file_path):
        columns = ['time', 'status', 'count']
        super().__init__(file_path, columns)

    def load_data(self):
        df = super().load_data()
        if df['time'].dtype != 'datetime64[ns]':
            df['time'] = pd.to_datetime(
                df['time'], format="%Hh %M", errors='coerce'
            )
        return df


def train_model(df, column_name):
    # Codificar os valores não numéricos usando LabelEncoder
    label_encoder = LabelEncoder()
    df[column_name] = label_encoder.fit_transform(df[column_name])

    model = IsolationForest(contamination=0.05)
    model.fit(df[[column_name]])
    return model


def generate_alerts(df, model, column_name):
    df['anomaly'] = model.predict(df[[column_name]])
    anomalies = df[df['anomaly'] == -1]
    return anomalies


def plot_data(df, column_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df[column_name])
    plt.xlabel('Time')
    plt.ylabel('Transaction Count')
    plt.title('Real-time Transaction Data')
    plt.xticks(rotation=45)
    st.pyplot(plt)


def main():
    # Load and preprocess data from transactions_1.csv
    loader1 = Transactions1DataLoader('data/transactions_1.csv')
    df1 = loader1.load_data()

    # Train the anomaly detection model for transactions_1.csv
    model1 = train_model(df1, 'transacoes')

    # Generate alerts for anomalies in transactions_1.csv
    anomalies1 = generate_alerts(df1, model1, 'transacoes')
    if not anomalies1.empty:
        st.warning("Anomalies Detected in transactions_1.csv:")
        st.dataframe(anomalies1)

    # Plot real-time transaction data for transactions_1.csv
    plot_data(df1, 'transacoes')  # Usar o novo nome da coluna 'transacoes'

    # Load and preprocess data from transactions_2.csv
    loader2 = Transactions2DataLoader('data/transactions_2.csv')
    df2 = loader2.load_data()

    # Train the anomaly detection model for transactions_2.csv
    model2 = train_model(df2, 'count')

    # Generate alerts for anomalies in transactions_2.csv
    anomalies2 = generate_alerts(df2, model2, 'count')
    if not anomalies2.empty:
        st.warning("Anomalies Detected in transactions_2.csv:")
        st.dataframe(anomalies2)

    # Plot real-time transaction data for transactions_2.csv
    plot_data(df2, 'count')


if __name__ == '__main__':
    main()
