import re
import json
from utils.utils import *


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
        r"<figcaption itemprop=\"caption description\">\s*<span class=\"icon-photo\"><\/span>(.*?)<\/figcaption>.*?<script.*?<p.*?>(.*?)<div",
        re.MULTILINE | re.DOTALL)

    content_lst = re.findall(content_regex, content)

    content_final = []
    for c in content_lst[0]:
        # c_2 = re.sub(r"<br>|</?strong>|</figcaption>", "\n", c)
        c_2 = re.sub(r"<br>|</?strong>|</figcaption>", " ", c)
        c_final = re.sub(r"</?\w+.*?>|\t|\n", "", c_2)
        content_final.append(c_final)

    final_dict = {
        "Author": author,
        "PublishedTime": published_time,
        "Title": title[0],
        "SubTitle": subtitle[0],
        "Lead": lead[0],
        "Content": "\n".join([content_final[0], content_final[1]])
    }

    # for key, val in final_dict.items():
    #     print(key, ":", val)

    print(json.dumps(final_dict, indent=4, ensure_ascii=False))


def extract_contents_gsc(file_name):
    content = parse_file(file_name, "utf-8")
    title_extractor = re.compile(r"class=\"product_title\s+entry-title\">\s*(.*?)</h1>", re.MULTILINE | re.DOTALL)
    price_from_extractor = re.compile(
        r"<p\s+class=\"price\"><span\s+class=\"woocommerce-Price-amount\samount\">.*?([$€])</span>([0-9.,]+)</span>\s+–\s+")
    price_to_extractor = re.compile(
        r"<span\s+class=\"woocommerce-Price-amount\samount\">.*?([$€])</span>([0-9.,]+)</span></p>")
    price_from = price_from_extractor.search(content)
    price_to = price_to_extractor.search(content)

    title = title_extractor.search(content).group(1)
    price_to = "{}{}".format(price_to.group(1), price_to.group(2))
    price_from = "{}{}".format(price_from.group(1), price_from.group(2))
    description_extractor = re.compile(r"woocommerce-product-details__short-description\">(.*?)</div>",
                                       re.MULTILINE | re.DOTALL)
    description = re.sub(r"</?p>|\n", "", description_extractor.search(content).group(1))

    category_extractor = re.compile(r"class=\"posted_in\">Category:\s+<a.*?rel=\"tag\">(.*?)</a></span>")
    category = category_extractor.search(content).group(1)

    tags_extractor = re.compile(r"<a href=\".*?product-tag.*?\"\s+rel=\"tag\">(.*?)</a>")
    tags = tags_extractor.findall(content)

    attribute_extractor = re.compile(r"<label>(.*?)\s*</label>")
    attributes = attribute_extractor.findall(content)

    var_dict = {}
    for attr in attributes:
        attr_extractor = re.compile(rf"<td\s+data-title=\"{re.escape(attr)}\">(.*?)</td>")
        attr_val = attr_extractor.findall(content)
        var_dict[attr] = attr_val

    separate_list_price_extractor = re.compile(
        r"<span\sclass=\"item\"><span\sclass=\"price\">(?:<del>)?.*?([$€])</span>([0-9.,]+)</span>(?:</del>)?")
    separate_list_price = ["{}{}".format(curr, amount) for curr, amount in
                           separate_list_price_extractor.findall(content)]

    separate_discount_price_extractor = re.compile(r"<ins>.*?([$€])</span>([0-9.,]+)</span></ins>")
    separate_discount_price = ["{}{}".format(curr, amount) for curr, amount in
                               pad_list(separate_discount_price_extractor.findall(content), var_dict["Model"],
                                        "currency")]

    variations = zip(separate_list_price, separate_discount_price)
    results = generate_json_gsc(title, price_from, price_to, description, category, tags, var_dict, variations)
    print(json.dumps(results, indent=4))
