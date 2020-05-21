import glob
import bs4 as soup
from preprocess import preprocess_content, prepare_raw_html, strip_html_elements
from collections import Counter
from collections import defaultdict
from create_db import connect, close
from tqdm import tqdm
from tabulate import tabulate
import string
import os

add_word_to_index_word = """INSERT INTO IndexWord (word) VALUES (?)"""
insert_data_query = """INSERT INTO Posting VALUES (?,?,?,?)"""
check_existing_word = """SELECT word FROM IndexWord WHERE word = ?"""
get_words = '''
    SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
    FROM Posting p
    WHERE
        p.word = ?
    GROUP BY p.documentName
    ORDER BY freq DESC;
'''


def print_query(item_dict):
    printing_list = []
    for key, val in item_dict.items():
        with open(os.path.join("..", "data", key)) as file:
            html = soup.BeautifulSoup(file.read(), features="lxml")
        body = html.find("body")
        stripped_html = strip_html_elements(body)
        stripped_html = stripped_html.text
        text = prepare_raw_html(stripped_html, True)
        parts = text.split()
        snippet = ""
        for i in val["idx"]:
            part = parts[max(i - 3, 0): min(i + 3, len(parts))]
            snippet += f"... {' '.join(part)} ... "
        item_list = [val["freq"], key, snippet]
        printing_list.append(item_list)
    headers = ["Frequencies", "Document", "Snippet"]
    print(tabulate(printing_list, headers=headers))


def process_query_data(items):
    item_dict = defaultdict()
    for word_queries in items:
        for single_query in word_queries:
            if single_query[0] not in item_dict.keys():
                item_dict[single_query[0]] = {}
                item_dict[single_query[0]]["freq"] = int(single_query[1])
                item_dict[single_query[0]]["idx"] = [int(x) for x in (single_query[2]).split(",")]
            else:
                item_dict[single_query[0]]["freq"] += int(single_query[1])
                current = [int(x) for x in (single_query[2]).split(",")]
                idxs = item_dict[single_query[0]]["idx"]
                idxs.extend(current)
                idxs = sorted(idxs)
                for i in range(len(idxs) - 1):
                    try:
                        if idxs[i] - idxs[i + 1] == -1:
                            idxs.remove(idxs[i + 1])
                    except IndexError as e:
                        break
                item_dict[single_query[0]]["idx"] = idxs
    return item_dict


def get_query(query):
    query_items = preprocess_content(query, False)
    conn, curr = connect()
    items = []
    try:
        for q in query_items:
            cursor = curr.execute(get_words, (q,))
            items.append(cursor.fetchall())
    except BaseException as e:
        print(e)
    close(conn)
    return items


def index():
    documents = glob.glob('../data/**/*.html', recursive=True)
    conn, curr = connect()
    nn = set()
    for doc in tqdm(documents, position=0, leave=True):
        d = defaultdict(list)
        document = doc.replace("../data/", "")
        with open(doc) as file:
            content = soup.BeautifulSoup(file.read(), features="lxml")
        body = strip_html_elements(content.find("body"))
        text = body.text
        html_text = prepare_raw_html(text, sub_at=True)
        content = preprocess_content(text, False)
        lower_text_parts = html_text.lower().split()
        counter = Counter(content)
        for i, e in enumerate(lower_text_parts):
            e = e.strip(string.punctuation)
            d[e].append(str(i))
        # print(counter)
        # for word, count in counter.items():
        #     print(word, count, d[word])
        # print(len(content), len(lower_text_parts))
        # print(lower_text_parts[360])
        # break
        for word, count in counter.items():
            try:
                if word not in nn:
                    curr.execute(add_word_to_index_word, (word,))
                curr.execute(insert_data_query, (word, document, count, ",".join(d[word])))
                conn.commit()
                nn.add(word)
            except BaseException as e:
                print(e)
    close(conn)


if __name__ == '__main__':
    # index()
    items = get_query("social services")
    items = process_query_data(items)
    print_query(items)
