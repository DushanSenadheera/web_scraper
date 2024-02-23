# import requests
# from bs4 import BeautifulSoup
# import csv
#
# url = "https://www.tripadvisor.com/Hotels-g304138-Kandy_Kandy_District_Central_Province-Hotels.html"
# response = requests.get(url)
# html_content = response.content
#
# soup = BeautifulSoup(html_content, "html.parser")
# elements = soup.find_all("h3", class_="nBrpc Wd o W")
#
# with open("data.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     for element in elements:
#         writer.writerow(["Title", element])
#
# print("finished web scraping")

from selenium import webdriver
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.com/Hotels-g304138-Kandy_Kandy_District_Central_Province-Hotels.html")
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

title = soup.findAll("h3", class_="nBrpc Wd o W")
rating = soup.findAll("div", class_="luFhX o W f u w JSdbl")

with open("data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Rating"])
    for title, rating in zip(title, rating):
        title_text = title.text
        rating_text = rating.text
        writer.writerow([title_text, rating_text])


print("finished web scraping")

driver.quit()


