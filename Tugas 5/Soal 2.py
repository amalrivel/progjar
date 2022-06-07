from platform import java_ver
import requests
import re
from bs4 import BeautifulSoup

def rapibaris(num):
    space = ''
    for i in num:
        space += i + '\n'
    print("\nOutput Link:")
    print(space)


def getGoPackage(num, query):
    if query=="llrb":
        print("Query : https://pkg.go.dev/search?q=llrb")
        if int(num) < 25:
            r = requests.get('https://pkg.go.dev/search?q=llrb')
        r= requests.get('https://pkg.go.dev/search?limit=100&m=package&q=llrb#more-results')
     
    if query=="sort":
        print("Query : https://pkg.go.dev/search?q=sort")
        if int(num) < 25:
            r = requests.get('https://pkg.go.dev/search?q=sort')
        r = requests.get('https://pkg.go.dev/search?limit=100&m=package&q=sort#more-results')
    soup = BeautifulSoup(r.content, 'html.parser')
    link = []

    for i in soup.find('div', {'class':'go-Content'}).find_all('a'):
        text = i.get("href").replace('?tab=licenses', '').replace('?tab=importedby', '')
        link.append(text)
        
        # space = ''
        # for j in link:
        #     space += j + '\n'

    a = " ".join(sorted(set(link), key=link.index))
    b = a.split()
    space = ''
    for i in b:
        space += i + '\n'
    b=space.split()

    rapibaris(b[1:int(num)+1])

if __name__ == '__main__':
    num = input("Masukkan Banyaknya Link: ")
    query = input("Masukkan Query:")
    getGoPackage(num, query)
