import pandas as pd
import streamlit as st

st.set_page_config(page_title="VOEN and Data Search System", layout="wide")

st.title("📊 VOEN and Data Search Panel")
st.write(
    "Fayllara və onların ayrı-ayrı səhifələrinə tək-tək baxmaq və axtarış"
    " etmək üçün panel."
)

uploaded_files = st.file_uploader(
    "Excel fayllarını seçin (.xlsx formatında)",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
)


# Hansı xanada "vöen" və ya "voen" varsa, həmin sətri avtomatik tapır
def find_header_row(file, sheet_name):
  try:
    temp_df = pd.read_excel(
        file, sheet_name=sheet_name, header=None, nrows=15
    )
    for idx, row in temp_df.iterrows():
      for val in row.values:
        val_str = str(val).lower()
        if "voen" in val_str or "vöen" in val_str:
          return idx
  except Exception:
    pass
  return 0  # Tapılmasa 0-cı sətir götürülür


if uploaded_files:
  # Faylları adları ilə birlikdə lüğətdə saxlayırıq
  file_dict = {file.name: file for file in uploaded_files}

  st.markdown("### 📁 Fayl və Səhifə Seçimi")
  col_f, col_s = st.columns(2)

  with col_f:
    selected_file_name = st.selectbox(
        "Baxılacaq Excel faylını seçin:", list(file_dict.keys())
    )

  selected_file = file_dict[selected_file_name]

  try:
    xl = pd.ExcelFile(selected_file)
    sheet_names = xl.sheet_names

    with col_s:
      selected_sheet = st.selectbox(
          f"'{selected_file_name}' faylındakı səhifəni seçin:", sheet_names
      )

    # Seçilmiş fayl və səhifə üçün başlıq sətrini avtomatik tapırıq
    detected_header = find_header_row(selected_file, selected_sheet)

    # Məlumatı oxuyuruq
    df = pd.read_excel(
        selected_file, sheet_name=selected_sheet, header=detected_header
    )
    df.columns = [str(col).strip() for col in df.columns]

    st.success(
        f"'{selected_file_name}' — '{selected_sheet}' səhifəsi uğurla"
        f" yükləndi! (Başlıq tapılan sətir: {detected_header + 1}-ci sətir)"
    )

    columns = [str(col) for col in df.columns.tolist()]

    st.markdown("### 🔍 Axtarış Parametrləri")
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
      st.info(
          "Axtarışa başlamaq üçün yuxarıdakı xanaya məlumat yazın və ya"
          " aşağıdan cədvələ baxın."
      )

      with st.expander(
          f"'{selected_sheet}' səhifəsinin ümumi görünüşü (ilk 10 sətir)"
      ):
        st.dataframe(df.head(10), use_container_width=True)

  except Exception as e:
    st.error(f"Xəta baş verdi: {e}")
else:
  st.info(
      "Zəhmət olmasa başlamaq üçün bir və ya bir neçə Excel faylı yükləyin."
  )
