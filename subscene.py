from bs4 import BeautifulSoup
import requests
import re
import traceback
import subprocess

# URL templates
URL_SEARCH   = "https://subscene.com/subtitles/searchbytitle?query={query}"
URL_LIST     = "https://subscene.com/subtitles/{title}"
URL_DOWNLOAD = "https://subscene.com/subtitles/{title}/{lang}/{id}"

# Messages
HELP_MSG = """HINTS:
    MISC
        [?]help, e[x]it, [cl]s
    SETTINGS
        [st] setTitle(title)
        [sl] setLang(lang)
        [sh] setHI(hi)
        [c] current()
    ACTIONS
        [s] search(query)
        [l] getlist(title, lang, hi_only)
        [d] download(id, lang)
    LANGUAGE
        Full name or 'all'"""
CURRENT_SETTINGS_MSG = """Current settings:
Language = {lang}; HI only = {hi}; Keyword Filter = {kf}
Title = {title}"""

# Context (for session)
TITLE = None
LANG = "english"
HI_ONLY = True
KEYWORD_1080 = True

# Context setters / Misc
def setTitle(title):
    global TITLE
    TITLE = title.lower()
def setLang(lang):
    global LANG
    LANG = lang.lower()
def setHI(hi):
    global HI_ONLY
    HI_ONLY = hi
def setKF(kf):
    global KEYWORD_1080
    KEYWORD_1080 = kf
def current():
    print(CURRENT_SETTINGS_MSG.format(lang=LANG, hi=HI_ONLY, title=TITLE, kf=KEYWORD_1080))

# Storage
class SearchResult:
    """An object representing a Subscene search result.
    """
    def __init__(self, title: str, cname: str) -> None:
        self.title = title
        self.cname = cname
    def __str__(self) -> str:
        template = "{title} | {cname}"
        return template.format(title=self.title, cname=self.cname)
class SubtitleListing:
    """An object representing a subtitle for a specific title.
    """
    def __init__(self, lang: str, rel: str, hi: bool, owner: str, comment: str, id: str) -> None:
        self.lang = lang
        self.rel = rel
        self.hi = hi
        self.owner = owner
        self.comment = comment
        self.id = id
        pass
    def __str__(self) -> str:
        template = "{id} | {lang} | {rel} | {owner}"
        return template.format(
            lang=self.lang,
            rel=self.rel,
            hi=self.hi,
            owner=self.owner,
            comment=self.comment,
            id=self.id
        )

# Meat

def __fetch_site(url):
    site = requests.get(url).text
    site = re.sub('[\r\n\t]', '', site)
    soup = BeautifulSoup(site, features="html.parser")
    return soup

def search(query):
    if not query:
        print('Enter a query.')
        return
    
    # Fetch site & soupify
    print('Fetching site (search)...')
    soup = __fetch_site(URL_SEARCH.format(query=query))
    
    # Extract
    r_exact = [
        SearchResult(
            title = each.select_one('.title > a')['href'].replace('/subtitles/', ''),
            cname = each.select_one('.title > a').text
        )
        for each in soup.select('.exact + ul > li')
    ]

    # Print r
    for each in r_exact:
        print(each)

def getlist():
    if not TITLE:
        print('Set a title first.')
        return
    
    # Fetch site & soupify
    print('Fetching site (listing)...')
    soup = __fetch_site(URL_LIST.format(title=TITLE))

    # Counters
    c_before = 0
    c_after = 0
    
    # Remove language headers & Extract
    r = [
        SubtitleListing(
                rel = each.select_one('.a1 > a > span:nth-child(2)').text,
                lang = each.select_one('.a1 > a > span:nth-child(1)').text,
                hi = each.select_one('.a41') != None,
                owner = each.select_one('.a5 > a').text
                        if each.select_one('.a5 > a')
                        else each.select_one('.a5').text,
                comment = each.select_one('.a6 > div').text,
                id = each.select_one('.a1 > a')['href'].split('/')[-1]
        )
        for each in soup.select('tbody > tr')
        if (
                not each.select_one('.language-start')
            and not each.select_one('.banner')
        )
    ]       
    c_before = len(r)

    # Filter languages
    if LANG != 'all':
        r = [each for each in r if each.lang.lower() == LANG]
    # Filter HI
    if HI_ONLY:
        r = [each for each in r if each.hi == True]
    # Filter keyword
    if KEYWORD_1080:
        r = [each for each in r if "1080p" in each.rel]
    c_after = len(r)

    # Print r
    print('{}/{} subtitles remains'.format(c_after, c_before))
    for each in r:
        print(each)

def download(id):
    if not id:
        print('Enter an ID.')
        return
    
    # Fetch site & soupify
    print('Fetching (download)...')
    soup = __fetch_site(URL_DOWNLOAD.format(title=TITLE, lang=LANG, id=id))

    # Download file
    file_url = "https://subscene.com" + soup.select_one('#downloadButton')['href']
    file_name = "{title}_{id}_{lang}.zip".format(title=TITLE, id=id, lang=LANG)
    r = requests.get(file_url, allow_redirects=True)
    file = open(file_name, 'wb')
    file.write(r.content)
    file.close()
    print('{} bytes written.'.format(len(r.content)))

# Aliases
st = setTitle
sl = setLang
sh = setHI
sk = setKF
c = current
s = search
l = getlist
d = download

if __name__ == "__main__":
    # A rudimentary REPL
    while True:
        try:
            command = input('> ')
            if command in ['exit', 'x']:
                exit()
            if command in ['help', '?']:
                print(HELP_MSG)
                continue
            if command in ['cls', 'cl']:
                _ = subprocess.call("cls", shell=True)
                continue
            eval(command)
        except NameError:
            print('Invalid command and/or reference.')
        except Exception:
            traceback.print_exc()
        finally:
            print()
