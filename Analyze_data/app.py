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
    conn = sqlite3.connect(':memory:')
    df.to_sql('data_table', conn, if_exists='replace', index=False)

    # Define SQL query
    query = "SELECT time, today, yesterday, same_day_last_week, " \
        "avg_last_week, avg_last_month FROM data_table"

    # Execute SQL query
    results_df = pd.read_sql_query(query, conn)

    # Close database connection
    conn.close()

    # Plot the scatter plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        results_df['time'],
        results_df['today'],
        color="k",
        linestyle="--"
    )
    ax.scatter(
        results_df['time'],
        results_df['today'],
        marker=".",
        s=200
    )
    ax.set_xlabel('Hours')
    ax.set_ylabel('POS')
    ax.set_title('POS by hour')
    st.pyplot(fig)

    # Display the DataFrame using Streamlit
    st.dataframe(df, width=2000)
