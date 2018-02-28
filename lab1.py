import re
import requests
from urllib.parse import urlparse

mail_regex_pattern = re.compile(r'<a href=\"mailto\:[a-zA-Z0-9\.\_\-]+@[a-zA-Z0-9\-\.\_]+\"')

URL = input('format: protocol://domains\n')
power = int(input('power\n'))

info = urlparse(URL)

try:
    domain = info.netloc
    nameList = domain.split(".")
    domain = '%s.%s' % (nameList[-2], nameList[-1])
except:
    print('Bad addr')
    exit()

page_regex_pattern = re.compile(r'<a href=\"/[a-zA-z0-9\/\_\- ]+\"|'
                                r'<a href=\"[a-zA-z0-9\/\_\- ]+\"|'
                                r'<a href=\"[a-zA-Z0-9\/\:\.\_\-]+.' + domain + r'[a-zA-z0-9\/\_\- ]+\"')


def search_mails(url, power):
    visitedPages.add(url)

    try:
        page = requests.get(url)

    except requests.exceptions.RequestException:
        print('Bad page ' + url)
        return

    dirty_mails = set(mail_regex_pattern.findall(page.text))

    for mail in dirty_mails:
        mails.add(''.join(re.findall(r'(?<=\:)[^}]*(?=\")', mail)))

    dirty_pages = set(page_regex_pattern.findall(page.text))
    pages = set()

    for page in dirty_pages:
        page = ''.join(re.findall(r'(?<=\")[^}]*(?=\")', page))
        if re.findall(domain, page):
            pages.add(page)
        elif page.__len__() > 0 and page[0] != '/':
            pages.add(URL + '/' + page)
        else:
            pages.add(URL + page)

    print(url)
    print(mails.__len__())
    print()

    for page in pages:
        if visitedPages.__contains__(page):
            continue

        if power <= 0:
            continue

        search_mails(page, power - 1)


visitedPages = set()
mails = set()

if URL[-1] == '/':
    URL = URL[:-1]


search_mails(URL, power)
print(mails.__len__())
print(mails)