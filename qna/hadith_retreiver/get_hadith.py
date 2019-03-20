import urllib.request
import re
import csv
import pandas


web_url = 'http://www.sahih-bukhari.com'  # Variable to keep website url
web_url_req = urllib.request.Request(web_url)  # Request handler to open url
web_url_open = urllib.request.urlopen(web_url_req)  # Variable to open url
respData1 = web_url_open.read()  # Variable to keep web readbale data
link = re.findall(
    r'<a href="([^~]+?)"\sclass="Style8"', str(respData1))  # Regular expression used to find all related urls from site-map
print(link)

url = []
D = open('link.txt', 'w')  # Open a text file to keep all found links
for allurl in link:
    # Appending all found links to the list 'url'
    url.append("http://www.sahih-bukhari.com/" + allurl)

for alllink in url:
    D.write("\n" + alllink)  # Print an output of all links found
D.close()

hadith = []

# Open all found links, and using Regex, append all related data to a list.
for allink in url:
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

F = open('hadith.txt', 'w')
G = open('hadith.csv', 'w')

columns = ["Volume", "Book", "Number",
           "Narrator", "Verse"]  # a csv with 5 columns
# first element of every list in yourlist

not_index_list = [i[0:] for i in hadith]
pd = pandas.DataFrame(not_index_list, columns=columns,)
pd.to_csv("hadith.csv")
# for j, k, l, m, n in zip(vol, book, number, narrator, ayah):
#     # F.write("Vol : " + j)
#     # F.write("\nBook : " + k)
#     # F.write("\nNumber : " + l)
#     # F.write("\nNarrated by : " + m)
#     # F.write("\nVerse : " + n)
#     # F.write("\n")
#     # F.write("\n")

G.close()
F.close()
