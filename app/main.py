import json
import os
import re
import time
from bs4 import BeautifulSoup
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_target_urls():
    file_path = os.path.join(current_dir, '../urls.json')

    with open(file_path, "r") as f:
        file = json.load(f)
        return file["urls"]


def scrape_url(target_url):
    response = requests.get(target_url, timeout=30)
    return BeautifulSoup(response.content, 'html.parser')


def extract_from_html(soup: BeautifulSoup):
    text_div = soup.find_all(class_ = "txt_detail urdu ar rtl")

    inner_text = text_div[0].find('div', style='text-align: justify;')
    return inner_text.get_text()


def strip_non_urdu(text):
    urdu_pattern = re.compile(r'[\s\u0600-\u06FF]+')
    urdu_matches = urdu_pattern.findall(text)
    urdu_text = ''.join(urdu_matches)
    return urdu_text


def parse_text(par, counter):
    parse_urdu = par.replace('\n', '').split(" ")

    for w in parse_urdu:
        if w not in counter:
            counter[w] = 0
        counter[w] += 1


def output_common_words(counter):
    most_common = sorted(counter, key=counter.get, reverse=True)[:5]
    file_path = os.path.join(current_dir, '../out.txt')

    with open(file_path, 'w', encoding='utf-8') as my_file:
        for out in most_common:
            line = f"{out}"
            my_file.write(f"{line}\n")


if __name__ == "__main__":
    word_count = {}
    target_urls = get_target_urls()
    for url in target_urls:
        html = scrape_url(url)
        text = extract_from_html(html)
        urdu_text = strip_non_urdu(text)
        parse_text(urdu_text, word_count)
        time.sleep(1)

    output_common_words(word_count)
