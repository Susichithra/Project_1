import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Title
st.title("🌍 Global Seismic Trends Dashboard")

# Connect DB
conn = sqlite3.connect("project1.db")

# Load data (ONLY ONCE)
df = pd.read_sql("SELECT * FROM prj", conn)

# Clean column names (IMPORTANT FIX)
df.columns = df.columns.str.strip()

# Show columns (for debugging)
st.write("Columns:", df.columns)

# Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Detect correct magnitude column
mag_col = "mag" if "mag" in df.columns else "magnitude"

# Metrics
st.subheader("Key Metrics")
st.write("Total Earthquakes:", len(df))
st.write("Maximum Magnitude:", df[mag_col].max())
st.write("Average Magnitude:", round(df[mag_col].mean(), 2))

# Visualization
st.subheader("Magnitude Distribution")

fig, ax = plt.subplots()
ax.hist(df[mag_col], bins=20)
st.pyplot(fig)

# Sidebar filter
magnitude_filter = st.sidebar.slider("Magnitude", 0.0, 10.0, 5.0)

filtered_df = df[df[mag_col] >= magnitude_filter]
st.subheader("Filtered Data")
st.write(filtered_df)

query = """SELECT country, COUNT(*) AS total
FROM prj
GROUP BY country
ORDER BY total DESC
LIMIT 10"""

df = pd.read_sql(query, conn)

st.write(df)
st.bar_chart(df.set_index("country"))

#SQl

mag = st.slider("Select Magnitude", 0.0, 10.0, 5.0)

query = f"""
SELECT *
FROM prj
WHERE mag >= {mag}
"""

df = pd.read_sql(query, conn)
st.write(df)