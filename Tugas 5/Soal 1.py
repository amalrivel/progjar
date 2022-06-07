import re

import requests
from bs4 import BeautifulSoup


link = 'https://go.dev/doc/'
html = requests.get(link).text
soup = BeautifulSoup(html, 'html.parser')

def getGoBlog(num):
    
    track_title = num.text.strip().replace(': ', '-')
    download_url = '{}{}'.format(link, num['href'])
    file_name = '{}.html'.format(track_title)

    r = requests.get(download_url, allow_redirects=True)
    with open(file_name, 'wb') as f:
        f.write(r.content)

    print('Akan mengambil: {}'.format(track_title, download_url))

if __name__ == '__main__':
    input_link = soup.find_all('a', string=re.compile(r'^((?!\().)*$'))
    count = 1;
    print("List Data Pada Website:")
    for item in input_link[12:21]:
        print(count,item)
        count += 1
    
    print("\nDownload Data No Berapa?")
    num = int(input(">"))

    getGoBlog(input_link[num+11])



