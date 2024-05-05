# Imports
import re
import pandas as pd


def read_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as file:
        # The string is decoded to ASCII and encoded back to utf8 to remove  english characters
        return file.read().encode("ascii", "ignore").decode().splitlines()


def log2df(lines: list[str]) -> pd.DataFrame:
    # Remove the new line character from the entire text because new lines will be spit later using regex
    lines = str(lines).replace(r'\n', ' ')
    lines = lines.replace(r"'", r'"')

    # Split text into lines by considering date as delimiter
    split_lines = re.split(r'.(?="\d+/\d+/\d+)', str(lines))

    # Remove all entries which have less than 4 characters in them as they are junk
    split_lines = [strng for strng in split_lines if len(strng) > 4]

    # Instantiate a blank DataFrame with the required columns and required number of rows initialed to blank
    df = pd.DataFrame(index=range(len(split_lines)), columns=['Date', 'Time', 'Sender', 'Text'], data='')

    # Iterate over each line in the log to extract the required fields
    for idx, st in enumerate(split_lines):
        # Every match attempt is surrounded by try...except blocks to catch the case when the match return empty
        try:
            date = re.findall(r'\d+/\d+/\d+', st)[0].strip()
        except IndexError:
            date = None

        try:
            time = re.findall(r'\b\d{1,2}:\d{2}[ap]m\b', st)[0].strip()
        except IndexError:
            time = None

        try:
            sender = re.findall(r'-\s.+:', st)
            sender = sender[0].split()[1].replace(':', '').strip() if len(sender) > 0 else ''
        except IndexError:
            sender = None

        try:
            text = re.findall(r':\s.+', st)
            text = text[0].split(':')[1].strip() if len(text) > 0 else ''
            text = text[:-2]
        except IndexError:
            text = None

        # Place the date, time, sender and text info to the respect row in the dataframe
        df.iloc[idx, 0] = date
        df.iloc[idx, 1] = time
        df.iloc[idx, 2] = sender
        df.iloc[idx, 3] = text

    return df
