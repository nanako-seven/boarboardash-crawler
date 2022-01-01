from bs4 import BeautifulSoup
import requests

r = requests.get('https://j.eastday.com/p/1639190835035499')
print(r.text)
html = r.text
soup = BeautifulSoup(html)
