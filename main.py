from io import StringIO
from whatsapp import log2df
import streamlit as st

uploaded_file = st.file_uploader(label='Upload WhatsApp chat export')

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode())
    string_data = stringio.read().encode("ascii", "ignore").decode()
    string_data = string_data.encode("ascii", "ignore").decode().splitlines()
    print(string_data)
    df = log2df(string_data)
    print(df)
    st.dataframe(data=df, use_container_width=True)

