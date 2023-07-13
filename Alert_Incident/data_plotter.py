import matplotlib.pyplot as plt


class DataPlotter:
    def plot_data(self, df):
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'], df['count'])
        plt.xlabel('Time')
        plt.ylabel('Transaction Count')
        plt.title('Real-time Transaction Data')
        plt.xticks(rotation=45)
        plt.show()
