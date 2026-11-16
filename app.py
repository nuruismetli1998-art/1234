import pandas as pd
import streamlit as st

st.set_page_config(page_title="VOEN and Data Search System", layout="wide")

st.title("📊 VOEN and Data Search Panel")
st.write(
    "Bir neçə Excel faylını yükləyin (başlıqlar fərqli sətirdə olsa belə"
    " avtomatik tapılacaq)."
)

uploaded_files = st.file_uploader(
    "Excel fayllarını seçin (.xlsx formatında)",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
)


# Avtomatik başlıq sətrini tapan köməkçi funksiya
def find_header_row(file, sheet_name):
  # Faylın əvvəlki 10 sətrini oxuyuruq
  temp_df = pd.read_excel(file, sheet_name=sheet_name, header=None, nrows=10)
  for idx, row in temp_df.iterrows():
    row_str = row.astype(str).str.lower().values
    # Sətirdə "voen" və ya "vöen" sözü olub-olmamasını yoxlayırıq
    if any("voen" in str(val) or "vöen" in str(val) for val in row_str):
      return idx
  return 0  # Tapılmasa, 0-cı sətir götürülür


if uploaded_files:
  try:
    all_dfs = []

    for uploaded_file in uploaded_files:
      xl = pd.ExcelFile(uploaded_file)
      for sheet in xl.sheet_names:
        # Hər vərəq üçün başlıq sətrini avtomatik təyin edirik
        detected_header = find_header_row(uploaded_file, sheet)

        temp_df = pd.read_excel(
            uploaded_file, sheet_name=sheet, header=detected_header
        )
        temp_df["Fayl_Adi"] = uploaded_file.name
        temp_df["Sehife_Adi"] = sheet
        all_dfs.append(temp_df)

    df = pd.concat(all_dfs, ignore_index=True)
    st.success(f"Ümumi {len(uploaded_files)} fayl avtomatik uyğunlaşdırılaraq yükləndi!")

    # Sütun adlarındakı boşluqları təmizləyirik
    df.columns = [str(col).strip() for col in df.columns]

    columns = [str(col) for col in df.columns.tolist()]

    st.markdown("### Axtarış Parametrləri")
    col1, col2 = st.columns(2)

    with col1:
      search_column = st.selectbox("Axtarılacaq sütunu seçin:", columns)

    with col2:
      search_query = st.text_input("Axtarılacaq nömrə və ya sözü daxil edin:")

    if search_query:
      filtered_df = df[
          df[search_column]
          .astype(str)
          .str.contains(search_query, case=False, na=False)
      ]

      st.markdown(f"### Nəticələr ({len(filtered_df)} sətir tapıldı):")

      if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
      else:
        st.warning("Bu sorğuya uyğun heç bir məlumat tapılmadı.")
    else:
      st.info("Axtarışa başlamaq üçün yuxarıdakı xanaya məlumat yazın.")

      with st.expander("Bütün faylların ümumi görünüşü (ilk 10 sətir)"):
        st.dataframe(df.head(10), use_container_width=True)

  except Exception as e:
    st.error(f"Xəta baş verdi: {e}")
else:
  st.info("Zəhmət olmasa başlamaq üçün bir və ya bir neçə Excel faylı yükləyin.")
