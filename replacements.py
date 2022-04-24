from urllib import request
from bs4 import BeautifulSoup


def get_rep_soup(url):
    with request.urlopen(url) as url:
        doc = url.read()
    soup = BeautifulSoup(doc, 'html.parser')
    return soup

def get_rows(soup, cl):
    rows = list()
    for row in soup:
        if cl in row:
            rows.append()

class Replacements:
    def __init__(self, doc=""):
        self.doc = doc

    def get_text(self, url):
        with request.urlopen(url) as url:
            text = url.read()
        soup = BeautifulSoup(text, 'html.parser')
        self.doc = soup.prettify()

    def check(self, cl):
        if " " in cl:
            cl = cl.replace(" ","")
        cl = cl.upper()
        if self.doc.find(cl) == -1:
            return False
        return True

    def get_message(self, date, cl):
        if check(cl):
            return "\nZastepstwa na dzień {} dla klasy {}:\n\n".format(date, cl) + get_replacemetns(date, cl)
        return "\nDnia {} nie przewidziano zastepstw dla klasy {}".format(date, cl)

    def get_replacements(self, cl):
        msg = ""
        rows = self.doc.split('<tr>')
        for row in reversed(rows):
            if row.find(cl) != -1:
                soup = BeautifulSoup(row, 'html.parser')
                row = soup.get_text()
                elems = row.split('\n')
                for elem in elems:
                    elem = elem.strip()
                if elems[2][5:] != "":
                    msg += "Lekcja: "+elems[2][5] + "\n"
                    msg += "Zastępstwo: "+elems[5][5:]+"\n\n"
        return msg
