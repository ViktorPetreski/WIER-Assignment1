from nltk.tokenize import word_tokenize
from utils.stopwords import stop_words_slovene
import string
import re


def strip_html_elements(content):
    pero = content
    [script.extract() for script in
     pero(["script", "footer", "[document]", "svg"])]  # remove the tags in the list
    return pero.text


def prepare_raw_html(html, sub_at=False):
    # html = strip_html_elements(html)
    # text = html.getText()
    text = re.sub(r"\n{2,}", " ", html)
    text = re.sub(r"\s+", " ", text)
    if sub_at:
        text = re.sub(r"@", " ", text)
    return text


def tokenize(content):
    return word_tokenize(content, "slovene")


def remove_stopwords_and_make_lowercase(content):
    table = str.maketrans(dict.fromkeys(string.punctuation))  # OR {key: None for key in string.punctuation}
    res = []
    for x in content:
        word = x.lower().strip(string.punctuation).strip()
        if word not in stop_words_slovene and len(x.translate(table)) > 0:
            res.append(word)
    return res

def preprocess_content(content, is_html_object=True):
    if is_html_object:
        # content = strip_html_elements(content)
        content = content.getText()
    tokenized_content = tokenize(content)
    content = remove_stopwords_and_make_lowercase(tokenized_content)
    return content
