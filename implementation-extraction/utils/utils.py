from bs4 import BeautifulSoup as bs
import re


def parse_file(file_name, encoding_type="iso-8859-1"):
    with open(file_name, "r", encoding=encoding_type) as file:
        content = file.read()

    return content


def pad_list(first, second, t="list"):
    end = len(second)
    while len(first) < end:
        if t == "tuple":
            first.append(('0', '(0%)'))
        elif t == "currency":
            first.append(('$', '0'))
        elif t == "currency_xpath":
            end = len(second) * 2
            first.extend(['$', '0'])
        elif t == "list":
            first.append('0')
    return first


def generate_json(product):
    results = []
    for title, content, list_price, price, saving in product:
        prod_dict = {
            "Title": title,
            "Content": content.replace("\n", " "),
            "ListPrice": list_price,
            "Price": price,
            "Saving": saving[0],
            "SavingPercent": saving[1]
        }
        results.append(prod_dict)
    return results


def generate_json_gsc(title, price_from, price_to, description, category, tags, variation_attributes, variation_prices):
    variations_list = []
    keys = list(variation_attributes.keys())
    i = 0
    for separate_list_price, separate_discount_price in variation_prices:
        var = {}
        for key in keys:
            var[key] = variation_attributes[key][i]
        var.update({
            "VariationListPrice": separate_list_price,
            "VariationPrice": separate_discount_price if separate_discount_price else "0"
        })
        variations_list.append(var)
        i += 1
    results = []
    prod_dict = {
        "Title": title,
        "Description": description,
        "ListPriceFrom": price_from,
        "ListPriceTo": price_to,
        "Category": category,
        "Tags": tags,
        "Variations": variations_list
    }
    results.append(prod_dict)
    return results


def remove_empty_items(array, mode="basic"):
    result = []
    for i in range(len(array) - 1):
        if mode == "basic":
            if array[i] != '' and array[i + 1] == '':
                result.append(array[i])
            elif array[i] == '' and array[i + 1] == '':
                result.append('N/A')
        elif mode == "tuples":
            if array[i][0] != '' and array[i + 1][0] == '' and array[i][1] != '' and array[i + 1][1] == '':
                result.append(array[i])
            elif array[i][0] == '' and array[i + 1][0] == '' and array[i][1] == '' and array[i + 1][1] == '' and result[-1] != ("N/A", "N/A"):

                result.append(("N/A", "N/A"))
            elif array[i][0] != '' and array[i][1] == '':
                result.append((array[i][0], "N/A"))
            elif array[i][0] == '' and array[i][1] != '':
                result.append(("N/A", array[i][1]))
    return result


# remove all attributes except some tags(only saving ['href','src'] attr)
def _remove_all_attrs_except_saving(soup):
    whitelist = []
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            tag.attrs = {}
        else:
            attrs = dict(tag.attrs)
            for attr in attrs:
                # if attr not in ['src', 'href']:
                del tag.attrs[attr]
    return soup


def prettify(file_name, encoding = "iso-8859-1"):
    """
    Restructure a HTML so that each component is in new line.
    Unnecessary tags are removed:
    "<b>", "</b>", "<i>", "</i>", "<br>", "<br/>", " <br>", " <br/>", "&gt;", "-", "|", "<s>", "</s>", "<strong>", "</strong>"
    :param file_name: html file path
    :return: list of strings
    """

    content = parse_file(file_name, encoding)
    soup = bs(content, features="lxml")  # make BeautifulSoup
    soup = _remove_all_attrs_except_saving(soup)
    [script.extract() for script in soup(["script", "style", "meta", "link", "map"])]  # remove the tags in the list
    skip_tags = ["<b>", "</b>", "<i>", "</i>", "<br>", "<br/>", " <br>", " <br/>", "&gt;", "-", "|", "<s>", "</s>",
                 "<strong>", "</strong>"]  # skip this tags, i.e remove them
    pretty_html = soup.prettify().splitlines(1)  # prettify the html and create list of the tags
    sentence = ""
    combined_sentences = []
    for line in pretty_html:
        line = line.strip()

        # if the current item is not a tag, add it to the sentence list
        if not check_tag(line) and line not in skip_tags:
            # Combine consecutive items (sentences) into one sentence. If there are new lines in the sentence, remove them
            sentence = "{} {}".format(sentence, line.replace("\n", ""))
        else:
            if len(sentence) > 0:  # if sentences were found, add them as one item in the list.
                combined_sentences.append(sentence)
                sentence = ""  # reset the sentence
            if line not in skip_tags:  # the item is not sentence, so add it as tag if not part of the unwanted ones
                combined_sentences.append(line)
    return combined_sentences


def ending_tag(tag):
    """
    :param tag: word that needs to be checked
    :return: whether the word is closing tag
    """
    matcher = re.compile(r"</\w+>")
    return matcher.search(tag) is not None


def starting_tag(tag):
    """
    :param tag: word that needs to be checked
    :return: whether the word is opening tag
    """
    matcher = re.compile(r"<\w+>")
    return matcher.search(tag) is not None


def check_tag(word):
    """
    :param word: word that needs to be checked
    :return: whether the word is an HTML tag
    """
    matcher = re.compile(r"</?\w+>")
    return matcher.search(word) is not None


def compare_base_of_tags(tag1, tag2, mode="both"):
    """
    This function compares two strings and returns the answer. There are three modes that can be chosen.
    Both: compares the base of the tag, without the parentheses
    End: compares the first tag as is, checks if the second is closing tag and compares them as if both are opening
    Start: compares the second tag as is, checks if the second is opening tag and compares them as if both are opening
    :param tag1: first word to be compared.
    :param tag2: second word to be compared.
    :param mode: type of comparison. Available: both, end, start
    :return: weather the tags match given the criteria
    """
    if mode == "both":
        return tag1.replace("/", "") == tag2.replace("/", "")
    elif mode == "end":
        return starting_tag(tag1) and ending_tag(tag2) and tag1 == tag2.replace("/", "")
    elif mode == "start":
        return starting_tag(tag2) and ending_tag(tag1) and tag2 == tag1.replace("/", "")


def assess_next_lines(tag, page, index):
    """
    Looks for the first matching tag, to the given one, in the page list.
    As long as it does not find match, it adds the passed items from the page list
    :param tag: the tag that we are looking for
    :param page: wrapper or sample list
    :param index: the current position of the index in the page component
    :return: whether it found a match, the number of passed items until match and a string of the passed items
    """
    counter = 1
    next_tag = page[index]
    potential_expressions = [page[index - 1]]
    while counter + index < len(page) and tag != next_tag:  # must be full match
        next_tag = page[index + counter]
        potential_expressions.append(next_tag)
        counter += 1
    return len(potential_expressions) > 1, counter if counter == 1 else counter - 1, "({})?".format(
        " ".join(potential_expressions))


def find_closest_ending_tag(page, opening_tag, i):
    """
    Looks for the closest closing tag that is of the same nature as the given opening tag in the page list
    :param page: Wrapper or sample
    :param opening_tag: the opening tag that needs closing
    :param i: current position in the page list
    :return: The index of the closest matching tag
    """
    next_tag = page[i + 1]
    temp = i
    while i < len(page) and not compare_base_of_tags(opening_tag, next_tag, mode="end"):
        i += 1
        next_tag = page[i + 1]
    return i + 1 if i != temp else -1


def find_beginning_of_loop(page, tag, i):
    """
        Looks for the closest opening tag that is of the same nature as the given closing tag in the page list\n
        Loops backwards
        :param page: Wrapper or sample
        :param tag: the opening tag that needs closing
        :param i: current position in the page list
        :return: The index of the closest opening tag
        """
    prev_tag = page[i - 1]
    temp = i
    while i > 0 and not compare_base_of_tags(tag, prev_tag, mode="start"):
        i -= 1
        prev_tag = page[i - 1]
    return i - 1 if i != temp else -5


def match_square(part, tag, i):
    """
    Finds squares in the HTML code.
    IT RETURNS THE CORRECT VALUES!
    :param part: Wrapper or sample
    :param tag: the opening tag that needs closing
    :param i: current position in the page list
    :return: The part of the wrapper/sample that makes a square
    """
    closing_tag_id = find_closest_ending_tag(part, tag, i)
    beginning_tag_id = find_beginning_of_loop(part, part[i - 1], i - 1)
    if closing_tag_id > 0 and beginning_tag_id > 0:
        internal_wrapper = part[i:closing_tag_id + 1]
        internal_sample = part[beginning_tag_id:i]
        return internal_wrapper, internal_sample, closing_tag_id + 1
    return None, None, -1
