def parse_file(file_name, encoding_type="iso-8859-1"):
    with open(file_name, "r", encoding=encoding_type) as file:
        content = file.read()

    return content


def pad_list(first, second, t="list"):
    while len(first) < len(second):
        if t == "tuple":
            first.append(('0', '(0%)'))
        else:
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
