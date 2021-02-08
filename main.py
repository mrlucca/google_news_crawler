import requests
from bs4 import BeautifulSoup
from typing import Generator
import pandas as pd


# ,sbd:1&tbm=nws
# &tbm=nws&tbas=0

"""
PEGAR DADOS DO GOOGLE POR RANGE DE DATA:
    &tbs=qdr->
        :h -> HOUR
        :w -> WEEK
        :d -> DAY
        :m -> MONTH
        :y -> YEAR

"""

all_words = dict()


def get_news(search_find_name: str, range_info: int) -> Generator:

    base_url = "https://www.google.com/search?source=lnms&tbm=nws"
    return (requests.get(f"{base_url}&q={search_find_name}&start={i}")
            for i in range(0, range_info))


def get_all_content(html_content: requests.Response) -> list:
    page = BeautifulSoup(html_content.text, 'html.parser')
    divs_content = page.select("div.kCrYT")
    all_content_data = []
    for div_content in divs_content:
        content_data = dict()
        content = div_content.find("a")
        if content:
            print("GET LINK >> ")
            content_data['link'] = (
                content
                .get("href")
                .replace("/url?q=", "")
                .split("&sa")[0]
            )
            print("| > link: ", content_data['link'])
            print("GET TITLE >> ")
            content_data['title'] = content.text
            print("| > title: ", content_data['title'], end="\n\n")
            all_content_data.append(content_data)

    return all_content_data


def search():
    search_news = ["vale3", "mypk3"]
    news = []
    for search_new in search_news:
        for page in get_news(search_new, 5):
            content = get_all_content(page)
            [news.append(new_content) for new_content in content]

    return news


def get_content_in_news_link(news_link: str):
    response = requests.get(news_link)
    page = BeautifulSoup(response.text, 'html.parser')
    text = page.text
    text = (
        text
        .replace("\n", "")
        .replace("\r", "")
        .strip()
        .upper()
        .split()
    )
    return [raw_text for raw_text in text if len(raw_text) > 3]

    # import ipdb; ipdb.set_trace()


def agregation_words(text_splited: list):
    for word in text_splited:
        if not all_words.get(word):
            all_words[word] = 1
        else:
            all_words[word] = 1 + all_words[word]


if __name__ == "__main__":
    news = search()
    for link in news:
        text_splited = get_content_in_news_link(news_link=link['link'])
        agregation_words(text_splited=text_splited)

    # import ipdb; ipdb.set_trace()

    # news_df = pd.DataFrame(news)
    # news_df = news_df.drop_duplicates()
    # news_df.to_csv("./news.csv", sep=";", index=False)
