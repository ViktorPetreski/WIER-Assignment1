from lxml import html
import json
import re
from utils.utils import parse_file, pad_list, generate_json, generate_json_gsc


def extract_content_overstock(file_name):
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


def extract_content_rtvslo(file_name):
    tree = html.fromstring(parse_file(file_name, "utf-8"))

    author = tree.xpath('//div[@class="author-name"]/text()')
    publishedTime = tree.xpath('//div[@class="publish-meta"]/text()')
    publishedTime = re.sub('\t|\n', "", publishedTime[0])

    title = tree.xpath('//header[@class="article-header"]//h1/text()')
    subtitle = tree.xpath('//div[@class="subtitle"]/text()')
    lead = tree.xpath('//header[@class="article-header"]//p[@class="lead"]/text()')

    # content = tree.xpath(' //div[@class="article-body"]//figure[not[contains(class, \'gallery-bottom-thumb\')]]//figcaption[@itemprop="caption description"]/text()')
    content = tree.xpath(
        ' //div[@class="article-body"]//p/text() | //div[@class="article-body"]//p/strong/text() | //div[@class="article-body"]//figure[not(@class=\'photoswipe swiper-slide\') and not (@class=\'photoswipe gallery-bottom-thumb\')]/figcaption[@itemprop="caption description"]/text()')

    content_processed = []
    for c in content:
        content_processed.append(re.sub("\t|\n", "", c))

    # content = re.sub('\t',"", content[0])
    final_dict = {
        'Author': author[0],
        'PublishedTime': publishedTime,
        'Title': title[0],
        'SubTitle': subtitle[0],
        'Lead': lead[0],
        'Content': " ".join(content_processed)
    }

    print(json.dumps(final_dict, indent=4, ensure_ascii=False))


def extract_content_gsc(file_name):
    tree = html.fromstring(parse_file(file_name))
    title = tree.xpath('//h1[@class="product_title entry-title"]/text()')[0]
    price_from = tree.xpath(
        '//div[@class="summary entry-summary"]/p/span[1]/span/text() | //div[@class="summary entry-summary"]/p/span[1]/text()')
    price_from = "".join(price_from)

    price_to = tree.xpath(
        '//div[@class="summary entry-summary"]/p/span[2]/span/text() | //div[@class="summary entry-summary"]/p/span[2]/text()')
    price_to = "".join(price_to)

    description = tree.xpath('//div[@class="woocommerce-product-details__short-description"]/p/text()')
    description = ("".join(description)).replace("\n", "")

    category = tree.xpath('//span[@class="posted_in"]/a/text()')[0]

    tags = tree.xpath('//span[@class="tagged_as"]/a/text()')

    attributes = [attr.strip() for attr in
                  tree.xpath('//table[@class="table table-hover variations"]/thead/tr/th[not(@*)]/text()')]
    var_attr = {}
    for attr in attributes:
        var_attr[attr] = tree.xpath(
            f'//table[@class="table table-hover variations"]/tbody/tr/td[@data-title="{attr}"]/text()')

    separate_list_prices = tree.xpath(
        '//span[@class="price"]//span[1]/span/text() | //span[@class="price"]//span[1]/text()')

    c = 0
    separate_list_price = []
    while c < len(separate_list_prices) - 1:
        separate_list_price.append(f"{separate_list_prices[c]}{separate_list_prices[c + 1]}")
        c += 2

    separate_discount_prices = pad_list(tree.xpath('//ins/span/span/text() | //ins/span/text()'), var_attr["Model"],
                                        "currency_xpath")
    c = 0
    separate_discount_price = []
    while c < len(separate_discount_prices) - 1:
        separate_discount_price.append(f"{separate_discount_prices[c]}{separate_discount_prices[c + 1]}")
        c += 2

    variations = zip(separate_list_price, separate_discount_price)
    results = generate_json_gsc(title, price_from, price_to, description, category, tags, var_attr, variations)
    print(json.dumps(results, indent=4))
