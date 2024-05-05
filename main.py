from io import StringIO

import streamlit as st

from whatsapp import log2df


def main() -> None:
    # Create an upload section to the StreamLit app
    uploaded_file = st.file_uploader(label='Upload WhatsApp chat export')

    if uploaded_file is not None:
        # Capture the user upload data and parse it as a string
        stringio = StringIO(uploaded_file.getvalue().decode())

        # Split the input string to separate lines for parsing
        string_data = stringio.read().encode("ascii", "ignore").decode()
        string_data = string_data.encode("ascii", "ignore").decode().splitlines()

        # Parse the string to get a DataFrame with the required information
        df = log2df(string_data)

        # Embed the DataFrame to the StreamLit app
        st.dataframe(data=df, use_container_width=True)


if __name__ == '__main__':
    main()
