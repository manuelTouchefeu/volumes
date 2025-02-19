from models import *
import urllib3
import shutil
import re

books = BookManager().get_books()
books.reverse()
for b in books:
    #break
    if b.isbn:
        resp = urllib3.request("GET", "https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.isbn all '%s'" % b.isbn)
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
                        with open("static/images/cover_%s.jpg" % b.isbn, 'wb') as out:
                            r = http.request('GET', cover, preload_content=False)
                            shutil.copyfileobj(r, out)

