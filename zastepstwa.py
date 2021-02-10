from urllib import request
from bs4 import BeautifulSoup


class Zastepstwa:
    def __init__(self, doc=""):
        self.doc = doc

    def get_text(self, url):
        with request.urlopen(url) as url:
            text = url.read()
        soup = BeautifulSoup(text, 'html.parser')
        self.doc = soup.prettify()

    def check(self, date, cl):
        msg = ""
        if " " not in cl:
            cl = cl[:1] + " " + cl[1:]
        cl = cl.upper()
        if self.doc.find(cl) == -1:
            msg += "\nDnia "+date+" nie przewidziano zastepstw dla klasy "+cl
        else:
            msg += "\nZastepstwa na dzień "+date+" dla klasy "+cl+":\n\n"
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
