import argparse

from tabulate import tabulate
import os
import bs4 as soup
from preprocess import preprocess_content, prepare_raw_html, strip_html_elements
from collections import defaultdict
import time
from create_db import connect, close

get_words = '''
    SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
    FROM Posting p
    WHERE
        p.word in ?
    GROUP BY p.documentName
    ORDER BY freq DESC;
'''


def modify_get_query(no_of_arguments):
    idx = get_words.find("?")
    variables = "(" + "?," * (no_of_arguments - 1) + "?)"
    new_query = "{}{}{}".format(get_words[:idx], variables, get_words[idx + 1:])
    return new_query


def print_query(item_dict, query, pretty_print):
    printing_list = []
    for key, val in item_dict.items():
        with open(os.path.join("data", key), encoding="utf-8") as file:
            html = soup.BeautifulSoup(file.read(), features="lxml")
        body = html.find("body")
        # stripped_html = strip_html_elements(body)
        # stripped_html = stripped_html.text
        text = prepare_raw_html(body.text, True)
        parts = text.split()
        snippet = ""
        for count, i in enumerate(val["idx"]):
            start = max(i - 3, 0)
            end = min(i + 4, len(parts))
            dots_start = " ... "
            dots_end = " ... "
            if count != 0:
                dots_start = ""
            if start == 0:
                dots_start = ""
            if end == len(parts):
                dots_end = ""
            part = parts[start: end]
            if count % 3 == 2 and pretty_print:
                snippet += "\n... "
            snippet += f"{dots_start}{' '.join(part)}{dots_end}"
        item_list = [val["freq"], key, snippet]
        printing_list.append(item_list)

    headers = ["Frequencies", "Document", "Snippet"]
    print(tabulate(printing_list, headers=headers))
    with open("{}_results.txt".format(query.replace(" ", "_")), "w") as file:
        file.write(tabulate(printing_list, headers=headers))


def process_query_data(items):
    d = defaultdict()
    for document in items:
        idxs = sorted([int(x) for x in (document[2]).split(",")])
        for i in range(len(idxs) - 1):
            try:
                if idxs[i] - idxs[i + 1] == -1:
                    idxs.remove(idxs[i + 1])
            except IndexError as e:
                break
        d[document[0]] = {
            "freq": document[1],
            "idx": idxs
        }
    return d


def get_query(query):
    start = time.time()
    query_items = preprocess_content(query, False)
    new_query = modify_get_query(len(query_items))
    conn, curr = connect()
    items = []
    try:
        cursor = curr.execute(new_query, tuple(query_items))
        items = cursor.fetchall()
    except BaseException as e:
        print(e)
    close(conn)
    end = time.time() - start
    return items, end * 1000


def search_with_inverted_index(query, pretty_print):
    items, exec_T = get_query(query)
    items = process_query_data(items)
    # items = process_query_data(items)
    print(f"Results for query: {query}")
    print(f"Results found in: {round(exec_T, 2)} ms")
    print_query(items, query, pretty_print)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help='the query that you want to check')
    parser.add_argument("--pretty_print", default=False, help='True if you want to format the output with new lines')
    args = parser.parse_args()
    search_with_inverted_index(args.query, args.pretty_print)
