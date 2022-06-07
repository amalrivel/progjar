from platform import java_ver
import requests
import re
from bs4 import BeautifulSoup

def rapibaris(num):
    space = ''
    for i in num:
        space += i + '\n'
    return space


def readGoDoc():
    print("Hasil Query : https://pkg.go.dev/search?q=llrb+petar")
    r= requests.get('https://pkg.go.dev/search?q=llrb+petar')
    soup = BeautifulSoup(r.content, 'html.parser')
    link = []

    for i in soup.find('div', {'class':'go-Content'}).find_all('a'):
        text = i.get("href")
        link.append(text)

    a = " ".join(sorted(set(link), key=link.index))
    b = a.split()
    space = ''
    for i in b:
        space += i + '\n'
    b=space.split()

    newlink = rapibaris(b[1:2])
    a = f"https://pkg.go.dev{newlink}"
    return a

if __name__ == '__main__':
    a = readGoDoc()
    print("\nLink Terbaru :")
    print(a)
    r = requests.get('https://pkg.go.dev/github.com/petar/GoLLRB/llrb')
    soup = BeautifulSoup(r.content, 'html.parser')
    link = []
    print("\nRoot Index :")
    for i in soup.find('section', {'class':'Documentation-index'}).find_all('a'):
        print(i.get("href"))

    print("\nLink Index :")
    for i in soup.find('section', {'class':'Documentation-index'}).find_all('li'):
        print(i)

    # input_link = soup.find('div', {'class':'Documentation'}).find_all('ul')
    # print("List Data Pada Website: \n")
    # for item in input_link:
    #     print(item.get('href'))

