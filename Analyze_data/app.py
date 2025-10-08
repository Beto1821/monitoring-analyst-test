import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3

# Disable warning for st.pyplot() - option deprecated in newer Streamlit versions
# st.set_option('deprecation.showPyplotGlobalUse', False)

# Load CSV files
df1 = pd.read_csv("data/checkout_1.csv")
df2 = pd.read_csv("data/checkout_2.csv")
df3 = pd.read_csv("data/transactions_1.csv")
df4 = pd.read_csv("data/transactions_2.csv")

# Create SQLite database connections
conn1 = sqlite3.connect('data1.db')
df1.to_sql('data_table', conn1, if_exists='replace', index=False)

conn2 = sqlite3.connect('data2.db')
df2.to_sql('data_table', conn2, if_exists='replace', index=False)

# Define SQL queries
query1 = "SELECT time, today, yesterday, same_day_last_week, " \
         "avg_last_week, avg_last_month FROM data_table"

query2 = "SELECT time, today, yesterday, same_day_last_week, " \
         "avg_last_week, avg_last_month FROM data_table"

# Execute SQL queries
results_df1 = pd.read_sql_query(query1, conn1)
results_df2 = pd.read_sql_query(query2, conn2)

# Close database connections
conn1.close()
conn2.close()

st.title("Analise de Dados - Tarefa 1")


# Checkbox to show/hide lines for checkout_1.csv
show_today_1 = st.checkbox("Show Today Sales (Checkout 1)", value=True)
show_yesterday_1 = st.checkbox("Show Yesterday Sales (Checkout 1)", value=True)
show_same_day_last_week_1 = st.checkbox(
    "Show Same Day Last Week Sales (Checkout 1)", value=True
    )

# Checkbox to show/hide lines for checkout_2.csv
show_today_2 = st.checkbox("Show Today Sales (Checkout 2)", value=True)
show_yesterday_2 = st.checkbox("Show Yesterday Sales (Checkout 2)", value=True)
show_same_day_last_week_2 = st.checkbox(
    "Show Same Day Last Week Sales (Checkout 2)", value=True
    )

# Plot the scatter plot using Matplotlib for POS by hour
fig1, ax1 = plt.subplots(figsize=(10, 6))

if show_today_1:
    ax1.plot(
        results_df1['time'],
        results_df1['today'],
        color="r",
        linestyle="--",
        label="Today (Checkout 1)"
    )
    ax1.scatter(
        results_df1['time'],
        results_df1['today'],
        marker=".",
        s=200,
        color="r"
    )

if show_yesterday_1:
    ax1.plot(
        results_df1['time'],
        results_df1['yesterday'],
        color="b",
        linestyle="--",
        label="Yesterday (Checkout 1)"
    )
    ax1.scatter(
        results_df1['time'],
        results_df1['yesterday'],
        marker=".",
        s=200,
        color="b"
    )

if show_same_day_last_week_1:
    ax1.plot(
        results_df1['time'],
        results_df1['same_day_last_week'],
        color="g",
        linestyle="--",
        label="Same Day Last Week Sales (Checkout 1)"
    )
    ax1.scatter(
        results_df1['time'],
        results_df1['same_day_last_week'],
        marker=".",
        s=200,
        color="g"
    )

if show_today_2:
    ax1.plot(
        results_df2['time'],
        results_df2['today'],
        color="m",
        linestyle="--",
        label="Today (Checkout 2)"
    )
    ax1.scatter(
        results_df2['time'],
        results_df2['today'],
        marker=".",
        s=200,
        color="m"
    )

if show_yesterday_2:
    ax1.plot(
        results_df2['time'],
        results_df2['yesterday'],
        color="c",
        linestyle="--",
        label="Yesterday (Checkout 2)"
    )
    ax1.scatter(
        results_df2['time'],
        results_df2['yesterday'],
        marker=".",
        s=200,
        color="c"
    )

if show_same_day_last_week_2:
    ax1.plot(
        results_df2['time'],
        results_df2['same_day_last_week'],
        color="y",
        linestyle="--",
        label="Same Day Last Week Sales (Checkout 2)"
    )
    ax1.scatter(
        results_df2['time'],
        results_df2['same_day_last_week'],
        marker=".",
        s=200,
        color="y"
    )

ax1.set_xlabel('Horas')
ax1.set_ylabel('Número de Transações')
ax1.set_title('Número de Transações por Hora')

# Verifica se pelo menos um elemento com rótulo está presente
handles, labels = ax1.get_legend_handles_labels()
if any(labels):
    ax1.legend()  # Adiciona a legenda

st.pyplot(fig1)

# Plot the line plot using Matplotlib for AVG Sales
show_avg_last_week = st.checkbox("Show Avg Last Week Sales", value=True)
show_avg_last_month = st.checkbox("Show Avg Last Month Sales", value=True)

# Verifica se pelo menos uma checkbox está marcada
show_avg_sales = show_avg_last_week or show_avg_last_month

if show_avg_sales:
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    if show_avg_last_week:
        ax2.plot(
            results_df1['time'],
            results_df1['avg_last_week'],
            color="r",
            linestyle="-",
            marker=".",
            markersize=8,
            label="Avg Last Week (Checkout 1)"
        )

        ax2.plot(
            results_df2['time'],
            results_df2['avg_last_week'],
            color="b",
            linestyle="-",
            marker=".",
            markersize=8,
            label="Avg Last Week (Checkout 2)"
        )

    if show_avg_last_month:
        ax2.plot(
            results_df1['time'],
            results_df1['avg_last_month'],
            color="m",
            linestyle="-",
            marker=".",
            markersize=8,
            label="Avg Last Month (Checkout 1)"
        )

        ax2.plot(
            results_df2['time'],
            results_df2['avg_last_month'],
            color="c",
            linestyle="-",
            marker=".",
            markersize=8,
            label="Avg Last Month (Checkout 2)"
        )

    ax2.set_xlabel('Horas')
    ax2.set_ylabel('Número de Transações')
    ax2.set_title('Número de Transações por Hora')

    # Verifica se pelo menos um elemento com rótulo está presente
    handles, labels = ax2.get_legend_handles_labels()
    if any(labels):
        ax2.legend()  # Adiciona a legenda

    st.pyplot(fig2)
st.markdown("<p style='font-size:24px;'>Analisando os gráficos concluímos que "
            " o Checkout_1 está dentro da normalidade comparado à semelhança "
            " entre os dias.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:24px;'>O gráfico Checkout_2 mostra "
            " anomalia entre as 13h ás 19h.Havendo uma grande queda das"
            " transações e zerando entre as"
            " 15h ás 17h.</p>", unsafe_allow_html=True)

# Display the DataFrames using Streamlit
st.subheader("Checkout 1 Data")
st.dataframe(df1, width=2200)

st.subheader("Checkout 2 Data")
st.dataframe(df2, width=2200)
