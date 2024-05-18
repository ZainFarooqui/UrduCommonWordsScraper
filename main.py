import json
import os
import re
from bs4 import BeautifulSoup
import requests

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_COUNTER = {}

def get_target_urls():
    file_path = os.path.join(CURRENT_DIR, 'config.json')

    with open(file_path, "r", encoding='utf-8') as f:
        file = json.load(f)
        return file["urls"], file["excludedWords"]


def get_page(target_url):
    response = requests.get(target_url, timeout=30)
    return BeautifulSoup(response.content, 'html.parser')


def strip_non_urdu(page: BeautifulSoup):
    text = page.get_text(separator=' ', strip=True)
    urdu_pattern = re.compile(r'[\u0600-\u06FF]+')
    urdu_matches = urdu_pattern.findall(text)
    text = ' '.join(urdu_matches)
    return text


def parse_text(par, excluded_words):
    list_of_words = [w for w in par.replace('\n', '').split(" ") if w and w not in excluded_words]

    for w in list_of_words:
        if w not in WORD_COUNTER:
            WORD_COUNTER[w] = 0
        WORD_COUNTER[w] += 1

    return

def output_common_words(size=100, slack=0):
    most_common = sorted(WORD_COUNTER, key=WORD_COUNTER.get, reverse=True)[slack:size]
    file_path = os.path.join(CURRENT_DIR, 'out.txt')

    with open(file_path, 'w', encoding='utf-8') as my_file:
        for out in most_common:
            line = f"{out}"
            my_file.write(f"{line}\n")


if __name__ == "__main__":
    word_count = {}
    target_urls, excluded_words = get_target_urls()
    for url in target_urls:
        try:
            html = get_page(url)
        except requests.exceptions.RequestException as e:
            print(f"Failed to GET from URL: {url} with exception {e}")
        else:
            urdu_text = strip_non_urdu(html)
            parse_text(urdu_text, excluded_words)

    output_common_words()
