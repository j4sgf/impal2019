import urllib.request
import re
import csv
import pandas
import logging
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from time import time
from multiprocessing import Pool

from qna.global_constant import CORPUS_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def get_url(web_url):
    logger.warning('Finding all available links')
    web_url_req = urllib.request.Request(
        web_url)  # Request handler to open url
    web_url_open = urllib.request.urlopen(web_url_req)  # Variable to open url
    respData1 = web_url_open.read()  # Variable to keep web readbale data
    link = re.findall(
        r'<a href="([^~]+?)"\sclass="Style8"', str(respData1))  # Regular expression used to find all related urls from site-map
    return link


def append_link(link):
    logger.warning('Appending all found links into "link.txt"')
    url = []
    D = open('link.txt', 'w')  # Open a text file to keep all found links
    for allurl in link:
        # Appending all found links to the list 'url'
        url.append("http://www.sahih-bukhari.com/" + allurl)

    for alllink in url:
        D.write("\n" + alllink)  # Print an output of all links found
    D.close()
    return url


def scrap_hadith(web_url1, columns):
    startt = time()
    hadith_sitemap = get_url(web_url)
    hadith_url = append_link(hadith_sitemap)
    hadith = []
    logger.warning('All links saved. Scrapping hadith...')
    # Open all found links, and using Regex, append all related data to a list.
    for allink in hadith_url:
        req = urllib.request.Request(allink)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        hadithraw = re.findall(
            r'Volume\s(\d{1,2}),\sBook\s(\d{1,3}),\sNumber\s(\d{1,4})(?:[^~]+?)<strong>Narrated\sby\s([^~]+?)</strong>(?:[^~]+?)<blockquote>([^~]+?)</blockquote>', str(respData))
        for hadith_data in hadithraw:
            hadith.append(hadith_data)
    vol = []
    book = []
    number = []
    narrator = []
    ayah = []
    for a in hadith:
        vol.append(a[0])
        book.append(a[1])
        number.append(a[2])
        narrator.append(a[3])
        ayah.append(a[4])

    logger.warning(
        'All hadith had been saved. Converting hadith list into a dataframe')
    not_index_list = [i[0:] for i in hadith]
    pd = pandas.DataFrame(not_index_list, columns=columns,)
    return pd
    endd = time()
    print(endd - startt)


if __name__ == "__main__":

    columns = ["Volume", "Book", "Number",
               "Narrator", "Verse"]  # a csv with 5 columns
    # first element of every list in yourlist
    start_time = time()
    web_url = 'http://www.sahih-bukhari.com'  # Variable to keep website url
    hadith_df = scrap_hadith(web_url, columns)
    end_time = time()
    logger.warning("Total scrapping time : {0}".format(end_time - start_time))
    hadith_df.to_csv("hadith.csv")
# pd.to_json(r"hadith.json", orient='records', lines=True)
# for j, k, l, m, n in zip(vol, book, number, narrator, ayah):
#     # F.write("Vol : " + j)
#     # F.write("\nBook : " + k)
#     # F.write("\nNumber : " + l)
#     # F.write("\nNarrated by : " + m)
#     # F.write("\nVerse : " + n)
#     # F.write("\n")
#     # F.write("\n")

# G.close()
# F.close()
