import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3

# Disable warning for st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Create SQLite database connection
    conn = sqlite3.connect('data.db')
    df.to_sql('data_table', conn, if_exists='replace', index=False)

    # Define SQL query
    query = "SELECT time, today, yesterday, same_day_last_week, " \
            "avg_last_week, avg_last_month FROM data_table"

    # Execute SQL query
    results_df = pd.read_sql_query(query, conn)

    # Close database connection
    conn.close()

    # Checkbox to show/hide lines
    show_today = st.checkbox("Show Today Sales")
    show_yesterday = st.checkbox("Show Yesterday Sales")
    show_same_day_last_week = st.checkbox("Show Same Day Last Week Sales")

    # Plot the scatter plot using Matplotlib for POS by hour
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    if show_today:
        ax1.plot(
            results_df['time'],
            results_df['today'],
            color="r",
            linestyle="--",
            label="Today"
        )
        ax1.scatter(
            results_df['time'],
            results_df['today'],
            marker=".",
            s=200,
            color="r"
        )

    if show_yesterday:
        ax1.plot(
            results_df['time'],
            results_df['yesterday'],
            color="b",
            linestyle="--",
            label="Yesterday"
        )
        ax1.scatter(
            results_df['time'],
            results_df['yesterday'],
            marker=".",
            s=200,
            color="b"
        )

    if show_same_day_last_week:
        ax1.plot(
            results_df['time'],
            results_df['same_day_last_week'],
            color="g",
            linestyle="--",
            label="Same Day Last Week Sales"
        )
        ax1.scatter(
            results_df['time'],
            results_df['same_day_last_week'],
            marker=".",
            s=200,
            color="g"
        )

    ax1.set_xlabel('Hours')
    ax1.set_ylabel('Sales')
    ax1.set_title('POS by hour')

    # Verifica se pelo menos um elemento com rótulo está presente
    handles, labels = ax1.get_legend_handles_labels()
    if any(labels):
        ax1.legend()  # Adiciona a legenda

    st.pyplot(fig1)

    # Plot the line plot using Matplotlib for AVG Sales
    show_avg_last_week = st.checkbox("Show Avg Last Week Sales", value=True)
    show_avg_last_month = st.checkbox("Show Avg Last Month Sales")

    # Verifica se pelo menos uma checkbox está marcada
    show_avg_sales = show_avg_last_week or show_avg_last_month

    if show_avg_sales:
        fig2, ax2 = plt.subplots(figsize=(10, 6))

        if show_avg_last_week:
            ax2.plot(
                results_df['time'],
                results_df['avg_last_week'],
                color="r",
                linestyle="-",
                marker=".",
                markersize=8,
                label="Avg Last Week"
            )

        if show_avg_last_month:
            ax2.plot(
                results_df['time'],
                results_df['avg_last_month'],
                color="m",
                linestyle="-",
                marker=".",
                markersize=8,
                label="Avg Last Month"
            )

        ax2.set_xlabel('Hours')
        ax2.set_ylabel('Average Sales')
        ax2.set_title('Average Sales by Hour')

        # Verifica se pelo menos um elemento com rótulo está presente
        handles, labels = ax2.get_legend_handles_labels()
        if any(labels):
            ax2.legend()  # Adiciona a legenda

        st.pyplot(fig2)

    # Display the DataFrame using Streamlit
    st.dataframe(df, width=2000)
