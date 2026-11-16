import pandas as pd
import streamlit as st

st.set_page_config(page_title="VÖEN v? M?lumat Axtaris Sistemi", layout="wide")

st.title("?? VÖEN v? M?lumat Axtaris Paneli")
st.write("Excel faylinizi yükl?yin v? sür?tli s?kild? axtaris edin.")

# Fayl yükl?m? hiss?si
uploaded_file = st.file_uploader(
    "Excel faylini seçin (.xlsx formatinda)", type=["xlsx", "xls"]
)

if uploaded_file is not None:
  # Fayli oxumaq
  @st.cache_data
  def load_data(file):
    return pd.read_excel(file)

  try:
    df = load_data(uploaded_file)
    st.success("Fayl ugurla yükl?ndi!")

    # Sütun seçimi v? axtaris paneli
    columns = df.columns.tolist()

    st.markdown("### Axtaris Parametrl?ri")
    col1, col2 = st.columns(2)

    with col1:
      search_column = st.selectbox(
          "Axtaris aparilacaq sütunu seçin (m?s: VÖEN):", columns
      )

    with col2:
      search_query = st.text_input(
          "Axtarilacaq nömr? v? ya sözü daxil edin:"
      )

    if search_query:
      # Sütunu m?tn? çevirib axtaris apaririq
      filtered_df = df[
          df[search_column]
          .astype(str)
          .str.contains(search_query, case=False, na=False)
      ]

      st.markdown(
          f"### N?tic?l?r ({len(filtered_df)} s?tir tapildi):"
      )

      if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
      else:
        st.warning("Bu sorguya uygun heç bir m?lumat tapilmadi.")
    else:
      st.info("Axtaris? baslamaq üçün yuxaridaki xanaya m?lumat yazin.")

      # Ilkin önizl?m?
      with st.expander("Excel faylinin ümumi görünüsü (ilk 10 s?tir)"):
        st.dataframe(df.head(10), use_container_width=True)

  except Exception as e:
    st.error(f"Fayl oxunark?n x?ta bas verdi: {e}")
else:
  st.info("Z?hm?t olmasa is? baslamaq üçün Excel faylinizi yükl?yin.")