from models import *
import urllib3
import shutil
import re
import os

def get_cover(isbn):
    f = "static/images/cover_%s.jpg" % isbn
    cover = None
    resp = urllib3.request("GET", "https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.isbn all '%s'" % isbn)
    if resp.status == 200:
        resp = resp.data.decode("utf-8")
        p = re.compile("ark:/[0-9]+/[a-zA-Z0-9]+")
        res = p.search(resp)
        if res:
            ark = res.group(0)
            print(ark)
            target = urllib3.request("GET", "https://catalogue.bnf.fr/%s" % ark)
            if target.status == 200:
                target = target.data.decode("utf-8")
                cover = re.search("couverture\?appName=NE&idImage=[0-9]+&couverture=1", target)
                if cover:
                    cover = ("https://catalogue.bnf.fr/%s" % cover.group(0))
                    print(cover)
                    http = urllib3.PoolManager()
                    with open(f, 'wb') as out:
                        r = http.request('GET', cover, preload_content=False)
                        shutil.copyfileobj(r, out)
    return f if cover else None


if __name__ == '__main__':
    books = BookManager().get_books()
    books.reverse()
    nb_covers = 0
    for b in books:
        if b.isbn:
            if "cover_%s.jpg" % b.isbn in os.listdir("static/images"):
                print(b.title)
                continue
            if get_cover(b.isbn) is not None:
                nb_covers += 1
                print(nb_covers)
    print(nb_covers)


