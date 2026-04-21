import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Smart Data Analyzer", layout="wide")

# -------- TITLE --------
st.title("📊 Smart Data Analyzer")
st.markdown("Upload your dataset → Clean → Analyze → Visualize 🚀")

# -------- SIDEBAR --------
st.sidebar.title("⚙️ Options")
file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

# -------- MAIN LOGIC --------
if file is not None:

    # -------- READ DATA --------
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # -------- CLEANING --------
    df_cleaned = df.drop_duplicates()

    for col in df_cleaned.columns:
        if df_cleaned[col].dtype in ["int64", "float64"]:
            df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
        else:
            df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)

    # -------- COLUMN TYPES --------
    numeric_cols = df_cleaned.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df_cleaned.select_dtypes(include=["object"]).columns

    # -------- METRICS --------
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    # -------- TABS --------
    tab1, tab2, tab3 = st.tabs(["📄 Data", "🧹 Cleaning", "📊 Visualization"])

    # -------- TAB 1: RAW DATA --------
    with tab1:
        st.subheader("📄 Raw Data")
        st.write(df)

    # -------- TAB 2: CLEANED DATA --------
    with tab2:
        st.subheader("🧹 Cleaned Data")
        st.write(df_cleaned)

        st.subheader("📉 Missing Values (Before)")
        st.write(df.isnull().sum())

        st.subheader("📉 Missing Values (After)")
        st.write(df_cleaned.isnull().sum())

        st.write("Duplicates removed:", df.shape[0] - df_cleaned.shape[0])

        # Download button
        st.download_button(
            "⬇️ Download Cleaned Data",
            df_cleaned.to_csv(index=False),
            "cleaned_data.csv"
        )

    # -------- TAB 3: VISUALIZATION --------
    with tab3:
        st.subheader("📊 Visualization")

        selected_col = st.selectbox("Select column", df_cleaned.columns)

        if selected_col in numeric_cols:
            st.write("📌 Suggested: Histogram")

            fig, ax = plt.subplots()
            ax.hist(df_cleaned[selected_col])
            st.pyplot(fig)

        elif selected_col in categorical_cols:
            st.write("📌 Suggested: Bar Chart")

            value_counts = df_cleaned[selected_col].value_counts()

            fig, ax = plt.subplots()
            ax.bar(value_counts.index, value_counts.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Bonus: full dataset line chart
        st.subheader("📈 Dataset Overview")
        st.line_chart(df_cleaned.select_dtypes(include=["int64", "float64"]))

# -------- FOOTER --------
st.markdown("---")
st.markdown("✨ Built by Samiksha")