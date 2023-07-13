import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        raise NotImplementedError


class Transactions1DataLoader(DataLoader):
    def load_data(self):
        df = pd.read_csv(self.file_path, names=['time', 'status', 'f0_'])
        df['time'] = pd.to_datetime(df['time'], format='%Hh %M')
        return df


class Transactions2DataLoader(DataLoader):
    def load_data(self):
        df = pd.read_csv(self.file_path, names=['time', 'status', 'count'])
        df['time'] = pd.to_datetime(df['time'], format='%Hh %M')
        return df
