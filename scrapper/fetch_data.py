import bs4 
import requests

def get_xml(url):
  raw_data = requests.get(url)
  soup_indeed = bs4.BeautifulSoup(raw_data.text, "lxml")
  return soup_indeed