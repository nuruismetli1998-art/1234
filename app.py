import pandas as pd
import streamlit as st

st.set_page_config(page_title="Excel Data Search System", layout="wide")

st.title("📊 Excel Axtarış Paneli")
st.write(
    "Fayllara, səhifələrə ayrı-ayrı baxın və istədiyiniz sütunla (Ad, Soyad, VÖEN"
    " və s.) axtarış edin."
)

uploaded_files = st.file_uploader(
    "Excel fayllarını seçin (.xlsx formatında)",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
)


# Ən çox dolu xanası olan sətri avtomatik başlıq seçən funksiya
def find_header_row(file, sheet_name):
  try:
    temp_df = pd.read_excel(
        file, sheet_name=sheet_name, header=None, nrows=20
    )
    # Hər sətirdəki dolu (boş olmayan) xanaların sayını hesablayırıq
    non_empty_counts = temp_df.notna().sum(axis=1)
    if not non_empty_counts.empty:
      # Ən çox dolu xanası olan sətrin indeksini qaytarırıq
      return int(non_empty_counts.idxmax())
  except Exception:
    pass
  return 0


if uploaded_files:
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

    # Avtomatik tapılan başlıq indeksi
    auto_header = find_header_row(selected_file, selected_sheet)

    # Əgər avtomatik tapılan səhv olarsa, istifadəçi özü əl ilə dəyişə bilsin deyə nömrə paneli qoyuruq
    header_row = st.number_input(
        "Başlıq sətrinin nömrəsi (lazım gələrsə dəyişə bilərsiniz):",
        min_value=0,
        max_value=20,
        value=auto_header,
        step=1,
    )

    # Məlumatı oxuyuruq
    df = pd.read_excel(
        selected_file, sheet_name=selected_sheet, header=header_row
    )
    df.columns = [str(col).strip() for col in df.columns]

    st.success(
        f"'{selected_file_name}' — '{selected_sheet}' səhifəsi yükləndi!"
        f" (Başlıq sətri: {header_row + 1}-ci sətir)"
    )

    columns = [str(col) for col in df.columns.tolist()]

    st.markdown("### 🔍 Axtarış Parametrləri")
    col1, col2 = st.columns(2)

    with col1:
      search_column = st.selectbox("Axtarış aparılacaq sütunu seçin:", columns)

    with col2:
      search_query = st.text_input("Axtarılacaq sözü və ya nömrəni daxil edin:")

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
