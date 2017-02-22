import hashlib

import time


def build_page(title, message):
    page = """
        <html>
            <head><title>" + %s + "</title></head>
            <body>
                <h2>" + %s + "</h2>
                <p>" + %s + "</p>
            </body>
        </html>
    """ % (title, title, message)
    return page


def generate_new_state():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf-8'))
    return m.hexdigest()[0:6]


