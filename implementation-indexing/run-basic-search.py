import argparse
import glob
from collections import defaultdict, Counter
import bs4 as soup
from preprocess import strip_html_elements, preprocess_content, prepare_raw_html
import string
from tabulate import tabulate
from tqdm import tqdm
import time

def search(query, pretty_print):
    start = time.time()
    documents = glob.glob('./data/**/*.html', recursive=True)
    results_list = []
    query_parts = preprocess_content(query, False)
    headers = ["Frequencies", "Document", "Snippet"]
    for doc in tqdm(documents, position=0, leave=True):
        d = defaultdict(list)
        document = doc.replace("./data/", "")
        with open(doc, encoding="utf-8") as file:
            content = soup.BeautifulSoup(file.read(), features="lxml")
        text = strip_html_elements(content.find("body"))
        html_text = prepare_raw_html(text, sub_at=True)
        content = preprocess_content(text, False)
        counter = Counter(content)
        for i, e in enumerate(html_text.lower().split()):
            e = e.strip(string.punctuation)
            d[e].append(i)
        indexes = []
        freq = 0
        for q in query_parts:
            if q in counter.keys():
                freq += counter[q]
                indexes.extend(d[q])
        if freq > 0:
            indexes = sorted(indexes)
            for i in range(len(indexes) - 1):
                try:
                    if indexes[i] - indexes[i + 1] == -1:
                        indexes.remove(indexes[i + 1])
                except IndexError as e:
                    break
            snippet = ""
            parts = html_text.split()
            for count, i in enumerate(indexes):
                start = max(i - 3, 0)
                end = min(i + 3, len(parts))
                dots_start = " ... "
                dots_end = " ... "
                if start == 0 or count != 0:
                    dots_start = ""
                if end == len(parts):
                    dots_end = ""
                part = parts[start: end]
                if count % 3 == 2 and pretty_print:
                    snippet += "\n... "
                snippet += f"{dots_start}{' '.join(part)}{dots_end}"
            item_list = [freq, document, snippet]
            results_list.append(item_list)
    end = time.time() - start
    results_list = sorted(results_list, key=lambda x: x[0], reverse=True)
    print(f"Results for query: {query}")
    print(f"\tResults found in: {round(end)} s")
    print(tabulate(results_list, headers=headers))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help='the query that you want to check')
    parser.add_argument("--pretty_print", default=False, help='True if you want to format the output with new lines')
    args = parser.parse_args()
    search(args.query, args.pretty_print)

