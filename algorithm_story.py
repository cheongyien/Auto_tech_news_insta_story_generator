import feedparser
import textwrap
from datetime import date
from bs4 import BeautifulSoup
from generate_story import output_cert
from keywords_extract import get_topic
from generate_short_link import generate_short_link
import csv
import random


INVOLED_DAY = 1


def generate():
    title, text, link = get_algorithm()
    output_title, output_link, output_text = "", "", ""

    key = ""
    with open("api_key.txt", 'r')as f:
        key = f.read().replace(" ", "").replace("\n", "")

    res = generate_short_link(
        link, key, 'stc-insta-story-'+str(date.today().month)+"-"+str(date.today().day))
    output_short_link = res['url'].get('shortLink', link)

    paragraph = text
    text_len = 0
    text = textwrap.wrap(paragraph, width=40)
    text_len += len(text)
    for i in text:
        output_text += i + "\n"
    output_text += "\n"

    title = textwrap.wrap(title, width=40)
    title_len = len(title)
    for i in title:
        output_title += i + "\n"
    output_title += "\n"

    link = textwrap.wrap(link, width=40)
    link_len = len(link)
    for i in link:
        output_link += i + "\n"

    output_link = "Read more on: \n"+output_link + \
        "(or get the link in our bio!)"
    output_title = "Today's algorithm:\n" + output_title
    output_cert('title', output_title, title_len)
    output_cert('link', output_link, link_len)
    output_cert('summary', output_text, text_len)

    link = open("output_link.txt", "w")
    link.write(output_link)
    link.close()


def get_algorithm():
    rows = list(get_rows())
    rand = random.randint(0, len(rows)-1)
    header = rows[rand]['header']
    content = rows[rand]['content']
    url = rows[rand]['url']
    return (header, content, url)


def get_rows():
    f = open('output.csv', 'r', encoding='utf-8')

    reader = csv.DictReader(f)
    return reader


if __name__ == "__main__":
    generate()
