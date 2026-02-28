import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

headers = {
    'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'
}

economist_url = "https://en.wikipedia.org/wiki/The_Economist_Democracy_Index"

response = requests.get(economist_url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')


def get_table_after_heading(soup, heading_text):
    # Find the h2/h3 tag whose text contains the heading we're looking for
    heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and heading_text.lower() in tag.get_text(strip=True).lower())
    # Return the first <table> that appears after that heading in the HTML
    return heading.find_next('table')


def extract_list_by_country(soup):
    table = get_table_after_heading(soup, 'List by country')
    # Parse the table HTML into a DataFrame; wrapping in StringIO is required by pandas
    df = pd.read_html(StringIO(str(table)))[0]
    # Convert rank to numeric, setting non-numeric values (e.g. stray country names
    # from duplicate rows in the HTML) to NaN so we can filter them out
    df['2024 rank'] = pd.to_numeric(df['2024 rank'], errors='coerce')
    # Drop the duplicate rows that had no rank value
    df = df.dropna(subset=['2024 rank'])
    # Convert rank from float to int now that NaNs are gone
    df['2024 rank'] = df['2024 rank'].astype(int)
    # Reset index so rows are numbered 0, 1, 2... after dropping duplicates
    return df.reset_index(drop=True)


def extract_components(soup):
    table = get_table_after_heading(soup, 'Components')
    # header=[0] tells pandas to use only the first row as column names, ignoring
    # the extra "Full democracies / Flawed democracies" section rows pandas would
    # otherwise treat as a second header level
    df = pd.read_html(StringIO(str(table)), header=[0])[0]
    # Remove soft-hyphen characters (\xad) that Wikipedia uses for word-breaking
    # in long column names like "Electoral process and pluralism"
    df.columns = [col.replace('\xad', '') for col in df.columns]
    # Same duplicate-row cleanup as above: coerce non-numeric ranks to NaN
    df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    df = df.dropna(subset=['Rank'])
    df['Rank'] = df['Rank'].astype(int)
    return df.reset_index(drop=True)


list_by_country = extract_list_by_country(soup)
components = extract_components(soup)

print(list_by_country)
print()
print(components)
