import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.tripadvisor.com/Hotels-g304138-Kandy_Kandy_District_Central_Province-Hotels.html"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")
elements = soup.find_all("h3", class_="nBrpc Wd o W")

with open("data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for element in elements:
        writer.writerow(["Title", element])

print("finished web scraping")


