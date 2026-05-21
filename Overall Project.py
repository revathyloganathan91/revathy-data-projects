# ======================================================
# IMPORT LIBRARIES
# ======================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Sachi Info Tech Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# PASTEL THEME + FIXED SIDEBAR
# ======================================================

st.markdown("""
<style>
/* Main App */
.stApp {
    background-color: #F8F6FF;
    color: black;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EDE7F6 !important;
}
/* Sidebar scroll only */
section[data-testid="stSidebar"] > div {
    overflow-y: auto;
    height: 100vh;
}
/* Main Content */
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
/* Global Text */
html, body, p, div, span, label {
    color: black !important;
}
/* Headers */
h1, h2, h3, h4 {
    color: #5E548E !important;
}
/* Buttons */
.stButton > button {
    background-color: #CDB4DB !important;
    color: black !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #B8C0FF !important;
}
/* Download Buttons */
.stDownloadButton > button {
    background-color: #CDB4DB !important;
    color: black !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}
.stDownloadButton > button:hover {
    background-color: #B8C0FF !important;
    color: black !important;
}
/* Inputs */
.stTextInput input,
.stDateInput input {
    background-color: white !important;
    color: black !important;
}
/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}
/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}
/* Dropdown Popup Container */
div[data-baseweb="popover"] {
    background: white !important;
}
/* Dropdown List Container */
ul {
    background-color: white !important;
}
/* Dropdown Options */
li {
    background-color: white !important;
    color: black !important;
}
/* Hover Option */
li:hover {
    background-color: #EDE7F6 !important;
    color: black !important;
}
/* Selected Value */
div[data-baseweb="select"] span {
    color: black !important;
}
/* Fix dark layer */
[data-baseweb="menu"] {
    background-color: white !important;
    color: black !important;
}
/* Dropdown */
div[data-baseweb="popover"] {
    background-color: white !important;
}
div[data-baseweb="option"] {
    background-color: white !important;
    color: black !important;
}
div[data-baseweb="option"]:hover {
    background-color: #EDE7F6 !important;
    color: black !important;
}
/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 10px;
    padding: 5px;
}
/* Metrics */
[data-testid="metric-container"] {
    background-color: #FFF8F0;
    border-radius: 10px;
    padding: 10px;
}
/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFF8F0 !important;
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN SETUP
# ======================================================

USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ======================================================
# LOGIN PAGE
# ======================================================

if not st.session_state.logged_in:

    st.title("🔐 Sachi Info Tech")

    st.subheader("Sales Analytics Login")

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True

            st.success("✅ Login Successful")

            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🏢 Sachi Info Tech")

st.sidebar.write("Sales Analytics System")

st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>",
unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):

    st.session_state.logged_in = False

    st.rerun()

# ======================================================
# HEADER
# ======================================================

st.title("📊 Sales Data Analytics Dashboard")

st.markdown("""
Analyze sales trends, clean datasets,
visualize reports and predict future sales.
""")

# ======================================================
# FILE UPLOAD
# ======================================================

st.subheader("📂 Upload Dataset")

file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# ======================================================
# MAIN
# ======================================================

if file:

    # READ FILE
    if file.name.endswith(".csv"):

        df = pd.read_csv(file)

    else:

        df = pd.read_excel(file)

    # ======================================================
    # ORIGINAL DATA
    # ======================================================

    st.subheader("📌 Original Data")

    st.dataframe(df)

    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    # ======================================================
    # DATA CLEANING
    # ======================================================

    st.subheader("🧹 Data Cleaning")

    null_option = st.selectbox(
        "Handle Missing Values",
        [
            "None",
            "Mean",
            "Median",
            "Zero"
        ]
    )

    remove_duplicates = st.button(
        "🗑️ Remove Duplicates"
    )

    apply_cleaning = st.button(
        "✅ Apply Cleaning"
    )

    df_clean = df.copy()

    # ======================================================
    # REMOVE DUPLICATES
    # ======================================================

    if remove_duplicates:

        before_rows = df_clean.shape[0]

        if "Order ID" in df_clean.columns:

            df_clean = df_clean.drop_duplicates(
                subset=["Order ID"]
            )

        else:

            df_clean = df_clean.drop_duplicates()

        after_rows = df_clean.shape[0]

        removed = before_rows - after_rows

        st.success(
            f"✅ {removed} Duplicate Rows Removed"
        )

    # ======================================================
    # APPLY CLEANING
    # ======================================================

    if apply_cleaning:

        for col in df_clean.columns:

            if pd.api.types.is_numeric_dtype(df_clean[col]):

                if null_option == "Mean":

                    df_clean[col] = df_clean[col].fillna(
                        df_clean[col].mean()
                    )

                elif null_option == "Median":

                    df_clean[col] = df_clean[col].fillna(
                        df_clean[col].median()
                    )

                elif null_option == "Zero":

                    df_clean[col] = df_clean[col].fillna(0)

            else:

                df_clean[col] = df_clean[col].fillna(
                    "Unknown"
                )

        # DATE CONVERSION
        if "Date" in df_clean.columns:

            df_clean["Date"] = pd.to_datetime(
                df_clean["Date"],
                errors="coerce"
            )

            df_clean = df_clean.dropna(
                subset=["Date"]
            )

        st.session_state["cleaned_data"] = df_clean

        st.success("✅ Data Cleaning Completed")

    # ======================================================
    # CLEANED DATA
    # ======================================================

    if "cleaned_data" in st.session_state:

        df = st.session_state["cleaned_data"]

        st.subheader("✅ Cleaned Data")

        st.dataframe(df.head(100))

        # ======================================================
        # FILTER
        # ======================================================

        st.subheader("🔍 Filter Data")

        filter_col = st.selectbox(
            "Select Column",
            df.columns
        )

        if df[filter_col].dtype == "object":

            values = df[filter_col].dropna().unique()

            selected = st.multiselect(
                "Select Values",
                values,
                default=values
            )

            filtered_df = df[
                df[filter_col].isin(selected)
            ]

        else:

            min_val = float(df[filter_col].min())

            max_val = float(df[filter_col].max())

            selected_range = st.slider(
                "Select Range",
                min_val,
                max_val,
                (min_val, max_val)
            )

            filtered_df = df[
                (df[filter_col] >= selected_range[0])
                &
                (df[filter_col] <= selected_range[1])
            ]

        st.dataframe(filtered_df.head(100))

        # ======================================================
        # VISUALIZATION
        # ======================================================

        st.subheader("📊 Data Visualization")

        x_col = st.selectbox(
            "X-axis",
            filtered_df.columns
        )

        numeric_cols = filtered_df.select_dtypes(
            include=np.number
        ).columns

        if len(numeric_cols) > 0:

            y_col = st.selectbox(
                "Y-axis",
                numeric_cols
            )

            chart = st.selectbox(
                "Chart Type",
                ["Bar", "Line", "Pie"]
            )

            grouped = (
                filtered_df.groupby(x_col)[y_col]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(8,4))

            if chart == "Bar":

                grouped.plot(kind="bar", ax=ax)

            elif chart == "Line":

                grouped.plot(
                    kind="line",
                    marker="o",
                    ax=ax
                )

            elif chart == "Pie":

                grouped.plot(
                    kind="pie",
                    autopct="%1.1f%%",
                    ax=ax
                )

                ax.set_ylabel("")

            plt.xticks(rotation=45)

            st.pyplot(fig)

        # ======================================================
        # DATABASE
        # ======================================================

        st.subheader("🗄️ Database Viewer")

        conn = sqlite3.connect(
            "sales_dashboard.db"
        )

        table_name = st.text_input(
            "Enter Table Name",
            "sales_data"
        )

        if st.button("💾 Save to Database"):

            filtered_df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            st.success("✅ Data Saved")

        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';",
            conn
        )

        if len(tables) > 0:

            selected_table = st.selectbox(
                "Select Table",
                tables["name"]
            )

            db_df = pd.read_sql_query(
                f"SELECT * FROM {selected_table}",
                conn
            )

            st.dataframe(db_df.head(100))

        # ======================================================
        # SALES PREDICTION
        # ======================================================

        st.subheader("🤖 Sales Prediction")

        date_cols = [
            col for col in filtered_df.columns
            if "date" in col.lower()
        ]

        if len(date_cols) > 0:

            date_col = st.selectbox(
                "Select Date Column",
                date_cols
            )

            sales_cols = filtered_df.select_dtypes(
                include=np.number
            ).columns

            if len(sales_cols) > 0:

                sales_col = st.selectbox(
                    "Select Sales Column",
                    sales_cols
                )

                future_days = st.slider(
                    "Days to Predict",
                    1,
                    30,
                    5
                )

                pred_df = filtered_df.copy()

                pred_df[date_col] = pd.to_datetime(
                    pred_df[date_col],
                    dayfirst=True,
                    errors='coerce'
                )

                pred_df = pred_df.sort_values(
                    date_col
                )

                pred_df["Days"] = (
                    pred_df[date_col]
                    - pred_df[date_col].min()
                ).dt.days

                X = pred_df[["Days"]]

                y = pred_df[sales_col]

                if len(pred_df) > 1:

                    model = LinearRegression()

                    model.fit(X, y)

                    future_day = (
                        pred_df["Days"].max()
                        + future_days
                    )

                    prediction = model.predict(
                        [[future_day]]
                    )[0]

                    st.success(
                        f"📈 Predicted Sales after "
                        f"{future_days} days: "
                        f"{prediction:.2f}"
                    )

                    # SQLite Dashboard Section (Add Below Your Existing Code)


# ======================================================
# SQLITE DATABASE DASHBOARD
# ======================================================

st.subheader("🗄️ SQLite Dashboard")

# CONNECT DATABASE
conn = sqlite3.connect("sales_dashboard.db")

# ======================================================
# SAVE TO SQLITE (ORDERWISE)
# ======================================================

if st.button("💾 Save to SQLite Database"):

    save_df = filtered_df.copy()

    # SAVE USING ORDERID IF AVAILABLE
    if "OrderID" in save_df.columns:

        save_df = save_df.drop_duplicates(subset=["OrderID"])

    save_df.to_sql(
        "sales_data",
        conn,
        if_exists="append",
        index=False
    )

    st.success("✅ Data Saved Order-wise into SQLite Database")

# ======================================================
# VIEW SQLITE TABLES
# ======================================================

tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

if len(tables) > 0:

    selected_table = st.selectbox(
        "📋 Select SQLite Table",
        tables["name"]
    )

    db_df = pd.read_sql_query(
        f"SELECT * FROM {selected_table}",
        conn
    )

    st.dataframe(db_df.head(100))

    st.write(f"📏 Rows: {db_df.shape[0]}")
    st.write(f"📏 Columns: {db_df.shape[1]}")

# ======================================================
# PASSWORD PROTECTED DATABASE DOWNLOAD
# ======================================================

st.subheader("🔒 Download SQLite Database")

download_password = st.text_input(
    "Enter Download Password",
    type="password"
)

if st.button("📥 Download SQL DB"):

    if download_password == "admin123":

        with open("sales_dashboard.db", "rb") as file:

            st.download_button(
                label="⬇️ Click to Download Database",
                data=file,
                file_name="sales_dashboard.db",
                mime="application/octet-stream"
            )

    else:

        st.error("❌ Incorrect Password")

# ======================================================
# DOWNLOAD TABLE AS CSV
# ======================================================

if len(tables) > 0:

    csv_data = db_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download Table CSV",
        data=csv_data,
        file_name=f"{selected_table}.csv",
        mime="text/csv"
    )

# CLOSE CONNECTION
conn.close()
