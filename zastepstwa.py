import urllib
import bs4
import datetime

def getText(url):
    with urllib.request.urlopen(url) as url:
        text = url.read()
    soup = bs4.BeautifulSoup(text, 'html.parser')
    doc = soup.prettify()
    return doc

def check(doc, date, cl="1 B"):
    msg = ""
    if doc.find(cl) == -1:
        msg += "\nDnia "+date+" nie przewidziano zastepstw dla klasy "+cl
    else:
        msg += "\nZastepstwa na dzień "+date+" dla klasy "+cl+":\n\n"
        rows = doc.split('<tr>')
        for row in reversed(rows):
            if row.find(cl) != -1:
                soup = bs4.BeautifulSoup(row, 'html.parser')
                row = soup.get_text()
                elems = row.split('\n')
                for elem in elems:
                    elem = elem.strip()
                if elems[2][5:] != "":                 
                    msg += "Lekcja: "+elems[2][5] + "\n"
                    msg += "Zastępstwo: "+elems[5][5:]+"\n\n" 
    return msg