import markdown2


def load_markdown(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = markdown2.markdown(f.read())
        html = html.replace('<p>', '').replace('</p>', '')
        return html