import re

import pandas as pd


def read_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf8') as file:
        return file.read().encode("ascii", "ignore").decode().splitlines()


def log2df(lines: list[str]) -> pd.DataFrame:
    lines = str(lines).replace(r'\n', ' ')
    lines = lines.replace(r"'", r'"')

    split_lines = re.split(r'.(?="\d+/\d+/\d+)', str(lines))

    split_lines = [strng for strng in split_lines if len(strng) > 4]

    df = pd.DataFrame(index=range(len(split_lines)), columns=['Date', 'Time', 'Sender', 'Text'], data='')

    for idx, st in enumerate(split_lines):
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

        df.iloc[idx, 0] = date
        df.iloc[idx, 1] = time
        df.iloc[idx, 2] = sender
        df.iloc[idx, 3] = text

    return df


def main():
    lines = read_file('TNT_Val.txt')
    return log2df(lines)


if __name__ == '__main__':
    datf = main()
