from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.com/Attractions-g297896-Activities-oa0-Galle_Galle_District_Southern_Province.html")

with open("location_pg1.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Rating"])


    time.sleep(2)  # wait for the page to load
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    titles = soup.findAll("div", class_="XfVdV o AIbhI")
    ratings = soup.findAll("svg", class_="UctUV d H0 hzzSG")['aria-label']
    reviews = soup.findAll("span", class_="biGQs _P pZUbB osNWb")
    categories = soup.findAll("div", class_="biGQs _P pZUbB hmDzD")

    # see = driver.find_element(By.CLASS_NAME, "rmyCe _G B- z _S c Wc wSSLS pexOo sOtnj")
    # see.click()

    for title, rating, review, category in zip(titles, ratings, reviews, categories):
        title_text = title.text
        rating_text = ratings.text
        review_text = review.text
        categories_text = category
        writer.writerow([title_text, rating_text, review_text, categories_text])

        # next_button = driver.find_element(By.CLASS_NAME, "BrOJk u j z _F wSSLS tIqAi unMkR")
        # next_button.click()



print("finished web scraping")
driver.quit()