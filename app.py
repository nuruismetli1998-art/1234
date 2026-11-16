import pandas as pd
import streamlit as st

st.set_page_config(page_title="VOEN and Data Search System", layout="wide")

st.title("📊 VOEN and Data Search Panel")
st.write("Bir neçə Excel faylını eyni vaxtda yükləyin və axtarış edin.")

# Birdən çox fayl yükləməyə icazə veririk
uploaded_files = st.file_uploader(
    "Excel fayllarını seçin (.xlsx formatında)",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
)

if uploaded_files:
  try:
    all_dfs = []

    for uploaded_file in uploaded_files:
      xl = pd.ExcelFile(uploaded_file)
      # Hər fayldakı bütün səhifələri oxuyub birləşdiririk
      for sheet in xl.sheet_names:
        temp_df = pd.read_excel(uploaded_file, sheet_name=sheet)
        # Fayl və səhifə adını da əlavə edə bilərik ki, hansından gəldiyi bilinsin
        temp_df["Fayl_Adi"] = uploaded_file.name
        temp_df["Sehife_Adi"] = sheet
        all_dfs.append(temp_df)

    # Bütün faylları tək cədvəldə birləşdiririk
    df = pd.concat(all_dfs, ignore_index=True)
    st.success(f"Ümumi {len(uploaded_files)} fayl uğurla yükləndi!")

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
