import re
import json
from .utils import *


def extract_contents(file_name):
    content = parse_file(file_name)

    title_extractor = re.compile(
        r"<td\s*valign=\"top\">\s*<a href=\"http://www\.overstock\.com/cgi-bin/d2\.cgi\?PAGE=PROFRAME&amp;PROD_ID=\d+\"><b>(\d{,2}-[K|k][T|t]\.?\s*(?:\S*\s*){,6}\(?\d*\.?\d*\s\S*\)?)</b></a>",
        re.MULTILINE | re.DOTALL)
    # the_tr = title_extractor.search(content)
    titles = re.findall(title_extractor, content)
    list_price_extractor = re.compile(r"nowrap=\"nowrap\"><s>([$€]\s*[0-9.,]+)</s>")
    price_extractor = re.compile(r"nowrap=\"nowrap\"><span\s*class=\"bigred\"><b>([$€]\s*[0-9.,]+)</b></span>")
    savings_extractor = re.compile(
        r"nowrap=\"nowrap\"><span\s*class=\"littleorange\">([$€]\s*[0-9.,]+)\s*(\(\d{,2}%\))</span>")
    list_prices = list_price_extractor.findall(content)
    list_prices = pad_list(list_prices, titles)
    prices = price_extractor.findall(content)
    prices = pad_list(prices, titles)
    savings = savings_extractor.findall(content)
    savings = pad_list(savings, titles, "tuple")
    print(savings)
    content_extractor = re.compile(r"valign=\"top\"><span\s*class=\"\w+\">(.*?)<br>", re.DOTALL | re.MULTILINE)
    contents = content_extractor.findall(content)
    product = zip(titles, contents, list_prices, prices, savings)
    results = generate_json(product)
    print(len(results))
    print(json.dumps(results, indent=4))


def extract_contents_rtvslo(file_name):
    content = parse_file(file_name, "utf-8")

    author_time_regex = re.compile(
        r"<div class=\"author-name\">(.*?)<\/div>\s*<\/div>\s*<div class=\"publish-meta\">\s*(.*?)\s*<br>",
        re.MULTILINE | re.DOTALL)
    author_time = re.findall(author_time_regex, content)
    author = author_time[0][0]
    published_time = author_time[0][1]

    title_regex = re.compile(r"<h1>(.*?)<\/h1>\s*<div class=\"subtitle\">", re.MULTILINE | re.DOTALL)
    title = re.findall(title_regex, content)

    subtitle_regex = re.compile(r"<div class=\"subtitle\">(.*?)<\/div>", re.MULTILINE | re.DOTALL)
    subtitle = re.findall(subtitle_regex, content)

    lead_regex = re.compile(r"<p class=\"lead\">(.*?)\s*<\/p>", re.MULTILINE | re.DOTALL)
    lead = re.findall(lead_regex, content)

    content_regex = re.compile(
        r"<figcaption itemprop=\"caption description\">\s*<span class=\"icon-photo\"><\/span>(.*?)\s*<\/figcaption>.*?\s*<p class=\"Body\"><\/p><p class=\"Body\">(.*?)\s*<p><\/p>\s*<div",
        re.MULTILINE | re.DOTALL)

    content_lst = re.findall(content_regex, content)
    img_caption = content_lst[0][0]

    content_lst_2 = re.sub(r"<br>|</?strong>", "\n", content_lst[0][1])
    content_final = re.sub(r"</?\w+.*?>", "", content_lst_2)

    # print(content_lst[0][0])
    # print(author, published_time, title, subtitle, lead)
    # print(content_final)

    final_dict = {
        "Author": author,
        "PublishedTime": published_time,
        "Title": title[0],
        "SubTitle": subtitle[0],
        "Lead": lead[0],
        "Content": "\n".join([img_caption, content_final])
    }

    for key, val in final_dict.items():
        print(key, ":", val)

    # print(json.dumps(final_dict, indent=4, ensure_ascii=False))
