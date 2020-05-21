import glob
from collections import defaultdict, Counter
import bs4 as soup
from preprocess import strip_html_elements, preprocess_content, prepare_raw_html
import string
from tabulate import tabulate
from tqdm import tqdm


def search(query):
    documents = glob.glob('../data/**/*.html', recursive=True)
    results_list = []
    query_parts = preprocess_content(query, False)
    headers = ["Frequencies", "Document", "Snippet"]
    for doc in tqdm(documents, position=0, leave=True):
        d = defaultdict(list)
        document = doc.replace("../data/", "")
        with open(doc) as file:
            content = soup.BeautifulSoup(file.read(), features="lxml")
        body = strip_html_elements(content.find("body"))
        text = body.text
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
            for i in indexes:
                part = parts[max(i - 3, 0): min(i + 3, len(parts))]
                snippet += f"... {' '.join(part)} ... "
            item_list = [freq, document, snippet]
            results_list.append(item_list)
    print(tabulate(results_list, headers=headers))


if __name__ == '__main__':
    search("social services")
