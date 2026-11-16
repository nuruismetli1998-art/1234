import pandas as pd
import streamlit as st

st.set_page_config(page_title="VOEN and Data Search System", layout="wide")

st.title("📊 VOEN and Data Search Panel")
st.write("Upload your Excel file and search quickly.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an Excel file (.xlsx format)", type=["xlsx", "xls"]
)

if uploaded_file is not None:

  @st.cache_data
  def load_data(file):
    return pd.read_excel(file)

  try:
    df = load_data(uploaded_file)
    st.success("File uploaded successfully!")

    columns = df.columns.tolist()

    st.markdown("### Search Parameters")
    col1, col2 = st.columns(2)

    with col1:
      search_column = st.selectbox("Select column to search (e.g. VOEN):", columns)

    with col2:
      search_query = st.text_input("Enter number or keyword to search:")

    if search_query:
      filtered_df = df[
          df[search_column]
          .astype(str)
          .str.contains(search_query, case=False, na=False)
      ]

      st.markdown(f"### Results ({len(filtered_df)} rows found):")

      if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
      else:
        st.warning("No matching records found.")
    else:
      st.info("Enter a query in the box above to start searching.")

      with st.expander("Preview Excel file (first 10 rows)"):
        st.dataframe(df.head(10), use_container_width=True)

  except Exception as e:
    st.error(f"Error reading file: {e}")
else:
  st.info("Please upload an Excel file to begin.")
