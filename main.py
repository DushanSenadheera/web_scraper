from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.com/Attractions-g297896-Activities-oa0-Galle_Galle_District_Southern_Province.html")
time.sleep(2)  # wait for the page to load

with open("destination.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Rating", "Review", "Category"])

    #while True:
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    titles = soup.findAll("div", class_="XfVdV o AIbhI")
    ratings = [svg.get('aria-label') for svg in soup.findAll("svg", class_="UctUV d H0 hzzSG")]
    reviews = soup.findAll("span", class_="biGQs _P pZUbB osNWb")  # replace with the actual class name
    categories = soup.findAll("div", class_="biGQs _P pZUbB alXOW oCpZu GzNcM nvOhm UTQMg ZTpaU W KxBGd")

    for title, rating, review, category in zip(titles, ratings, reviews, categories):
        title_text = titles.text
        rating_text = ratings.text
        review_text = reviews.text
        category_text = categories.text
        writer.writerow([title_text, rating_text, review_text, category_text])

        # try:
        #     next_button_xpath = """//*[@id="lithium-root"]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div"""  # replace with the actual XPath of the next button
        #     next_page = driver.find_element(By.XPATH, next_button_xpath)
        #     next_page.click()
        #     time.sleep(2)  # wait for the new page to load
        # except Exception as e:
        #     print("Scraping finished.")
        #     break

print("Finished web scraping")
driver.quit()