import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import io
import re
from sklearn.linear_model import LinearRegression
from datetime import timedelta

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Analytics Dashboard")

# -------------------------------
# File Upload
# -------------------------------
file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if file:
    try:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        st.session_state["file_name"] = file.name
    except Exception:
        st.error("Invalid file!")
        st.stop()

    st.subheader("📌 Original Data")
    st.dataframe(df)

    st.write(f"📏 Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # -------------------------------
    # Data Cleaning
    # -------------------------------
    st.subheader("🧹 Data Cleaning")

    remove_dup = st.checkbox("Remove Duplicates")
    null_option = st.selectbox("Handle Missing Values", ["None", "Mean", "Median", "Zero"])

    df_clean = df.copy()

    if remove_dup:
        df_clean = df_clean.drop_duplicates(subset=['OrderID']) if 'OrderID' in df_clean.columns else df_clean.drop_duplicates()

    for col in df_clean.columns:
        if df_clean[col].dtype in ['int64', 'float64']:
            if null_option == "Mean":
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            elif null_option == "Median":
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            elif null_option == "Zero":
                df_clean[col] = df_clean[col].fillna(0)
        else:
            df_clean[col] = df_clean[col].fillna("Unknown")

    # Date handling
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Date'])

    st.session_state["cleaned_data"] = df_clean

# -------------------------------
# Cleaned Data Section
# -------------------------------
if "cleaned_data" in st.session_state:
    df = st.session_state["cleaned_data"]

    st.subheader("✅ Cleaned Data")
    st.dataframe(df)

    st.write(f"📏 Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # -------------------------------
    # Visualization
    # -------------------------------
    st.subheader("📊 Visualization")

    col1 = st.selectbox("X-axis", df.columns)
    col2 = st.selectbox("Y-axis", df.columns)
    chart = st.selectbox("Chart Type", ["Bar", "Line", "Pie"])

    fig, ax = plt.subplots()

    try:
        grouped = df.groupby(col1)[col2].sum()

        if chart == "Bar":
            grouped.plot(kind="bar", ax=ax)
        elif chart == "Line":
            grouped.plot(kind="line", ax=ax)
        elif chart == "Pie":
            grouped.plot(kind="pie", autopct="%1.1f%%", ax=ax)

        st.pyplot(fig)
    except Exception as e:
        st.warning(f"⚠️ Invalid selection: {e}")

    # -------------------------------
    # Save to SQLite (Dynamic Table Name)
    # -------------------------------
    st.subheader("💾 Store Data in SQLite")

    if st.button("Save to Database"):
        try:
            # Get file name safely
            file_name = st.session_state.get("file_name", "table_data")

            table_name = file_name.split('.')[0]
            table_name = re.sub(r'\W+', '_', table_name)

            conn = sqlite3.connect("sales_data.db")

            df.to_sql(table_name, conn, if_exists="replace", index=False)

            conn.commit()
            conn.close()

            st.success(f"✅ Data stored in table: {table_name}")

        except Exception as e:
            st.error(f"Error: {e}")

    # -------------------------------
    # Download Excel
    # -------------------------------
    st.subheader("📥 Download Data")

    def to_excel(data):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            data.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        "⬇️ Download Excel",
        to_excel(df),
        "cleaned_data.xlsx"
    )

    # -------------------------------
    # ML Prediction
    # -------------------------------
    st.subheader("🤖 Sales Prediction")

    days = st.number_input("Days to Predict", 1, 30, 5)

    if st.button("Predict"):
        if 'Date' not in df.columns or 'Amount' not in df.columns:
            st.error("Dataset must contain 'Date' and 'Amount'")
        else:
            df_ml = df.copy()
            df_ml['Date'] = pd.to_datetime(df_ml['Date'], errors='coerce')
            df_ml['Amount'] = pd.to_numeric(df_ml['Amount'], errors='coerce')
            df_ml = df_ml.dropna()

            df_group = df_ml.groupby('Date')['Amount'].sum().reset_index()
            df_group['ord'] = df_group['Date'].map(pd.Timestamp.toordinal)

            X = df_group[['ord']]
            y = df_group['Amount']

            model = LinearRegression()
            model.fit(X, y)

            last = df_group['Date'].max()
            future_dates = pd.date_range(last + timedelta(days=1), periods=days)

            future_ord = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
            preds = model.predict(future_ord)

            pred_df = pd.DataFrame({
                "Date": future_dates,
                "Prediction": preds
            })

            st.dataframe(pred_df)

            fig2, ax2 = plt.subplots()
            ax2.plot(df_group['Date'], df_group['Amount'], label="Actual")
            ax2.plot(pred_df['Date'], pred_df['Prediction'], '--', label="Predicted")
            ax2.legend()
            st.pyplot(fig2)

# -------------------------------
# Database Viewer
# -------------------------------
st.subheader("🗄️ Database Viewer")

if st.button("Load Database"):
    try:
        conn = sqlite3.connect("sales_data.db")
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

        if not tables.empty:
            st.write("📋 Tables:")
            st.write(tables)

            table = st.selectbox("Select Table", tables['name'])

            if table:
                df_db = pd.read_sql(f"SELECT * FROM {table}", conn)
                st.dataframe(df_db)

                st.download_button(
                    "⬇️ Download Table CSV",
                    df_db.to_csv(index=False),
                    f"{table}.csv"
                )
        else:
            st.warning("⚠️ No tables found")

        conn.close()
    except Exception as e:
        st.error(e)

# -------------------------------
# Download Full Database
# -------------------------------
st.subheader("💾 Download Full Database")

try:
    with open("sales_data.db", "rb") as f:
        st.download_button(
            label="⬇️ Download SQLite DB",
            data=f,
            file_name="sales_data.db",
            mime="application/octet-stream"
        )
except:
    st.warning("⚠️ Database not created yet")