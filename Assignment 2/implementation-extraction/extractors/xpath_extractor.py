from lxml import html
import json
import re
from .utils import *

def extract_content(file_name):
    tree = html.fromstring(parse_file(file_name))
    titles = tree.xpath('//table[2]/tbody/tr/td[5]//td[2]/a/b/text()')
    contents = tree.xpath('//table[2]/tbody/tr/td[5]//td[2]/span[@class="normal"]/text()')

    list_prices = tree.xpath('//s/text()')
    list_prices = pad_list(list_prices, titles)
    prices = tree.xpath('//span[@class="bigred"]/b/text()')
    prices = pad_list(prices, titles)
    savings = " ".join(tree.xpath('//span[@class="littleorange"]/text()'))
    split_savings_matcher = re.compile(r"([$€]\s*[0-9.,]+)\s*(\([0-9.,]+%\))")
    savings = split_savings_matcher.findall(savings)
    savings = pad_list(savings, titles, "tuple")
    product = zip(titles, contents, list_prices, prices, savings)
    results = generate_json(product)
    print(json.dumps(results, indent=4))
