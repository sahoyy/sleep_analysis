import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


DB_HOST = "sql304.infinityfree.com" 
DB_USER = "if0_38340859"
DB_PASSWORD = "STAsalsabila" 
DB_NAME = "if0_38340859_sleep_analysis" 
TABLE_NAME = "sleep_data"

def create_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Insert Data
def insert_data(name, sleep_hours, age):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {TABLE_NAME} (name, sleep_hours, age) VALUES (%s, %s, %s)", (name, sleep_hours, age))
    conn.commit()
    conn.close()

# Fetch Data
def fetch_data():
    conn = create_connection()
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

# Streamlit UI
st.title("Sleep Analysis Data Entry & Statistics")

# User Input Form
with st.form("input_form"):
    name = st.text_input("Name")
    sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)
    age = st.number_input("Age", min_value=0, max_value=100, step=1)
    submit = st.form_submit_button("Submit")

if submit:
    insert_data(name, sleep_hours, age)
    st.success("Data submitted successfully!")

# Display Stored Data
data = fetch_data()
st.write("### Stored Data", data)

# Statistical Analysis
if not data.empty:
    # Frequency Distribution
    st.write("### Frequency Distribution")
    sleep_hours_counts = data["sleep_hours"].value_counts().sort_index()
    st.bar_chart(sleep_hours_counts)
    
    # Normal Distribution Plot
    st.write("### Normal Distribution")
    mean_sleep = np.mean(data["sleep_hours"])
    std_sleep = np.std(data["sleep_hours"])
    x = np.linspace(min(data["sleep_hours"]), max(data["sleep_hours"]), 100)
    y = norm.pdf(x, mean_sleep, std_sleep)
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"Mean: {mean_sleep:.2f}, Std Dev: {std_sleep:.2f}")
    ax.hist(data["sleep_hours"], density=True, alpha=0.5, bins=10)
    ax.legend()
    st.pyplot(fig)
