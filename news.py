import datetime
import PyRSS2Gen

class news:
    title = ''
    date = ''
    description = ''
    href = ''
    def __init__(self, title, date, description, href):
        self.title = title
        self.date = date
        self.description = description
        self.href = href
    def genRSSItem(self):
        if self.date == '':
            pubDate = datetime.datetime(2000,1,1,0,0)
        else :
            pdate = self.date.split('-')
            pubDate = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), 0, 0)

        return PyRSS2Gen.RSSItem(
            title = self.title, 
            link = self.href,
            pubDate = pubDate,
            description = self.description,
            # guid = PyRSS2Gen.Guid(self.href)
        )

newslist = []