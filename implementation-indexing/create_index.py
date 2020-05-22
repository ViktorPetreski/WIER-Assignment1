import glob
import bs4 as soup
from preprocess import preprocess_content, prepare_raw_html, strip_html_elements
from collections import Counter
from collections import defaultdict
from create_db import connect, close
from tqdm import tqdm
import string

add_word_to_index_word = """INSERT INTO IndexWord (word) VALUES (?)"""
insert_data_query = """INSERT INTO Posting VALUES (?,?,?,?)"""
check_existing_word = """SELECT word FROM IndexWord WHERE word = ?"""


def index():
    documents = glob.glob('../data/**/*.html', recursive=True)
    conn, curr = connect()
    nn = set()
    for doc in tqdm(documents, position=0, leave=True):
        d = defaultdict(list)
        document = doc.replace("../data/", "")
        with open(doc) as file:
            content = soup.BeautifulSoup(file.read(), features="lxml")
        raw_body = content.find("body")
        html_text = prepare_raw_html(raw_body.text, sub_at=True)
        text = strip_html_elements(raw_body)
        content = preprocess_content(text, False)
        lower_text_parts = html_text.lower().split()
        counter = Counter(content)
        for i, e in enumerate(lower_text_parts):
            e = e.strip(string.punctuation).strip()
            d[e].append(str(i))
        # print(counter)
        # print(document)
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
    index()
