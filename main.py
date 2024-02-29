from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

driver = webdriver.Chrome()
driver.get("https://www.tripadvisor.com/Attractions-g297896-Activities-oa0-Galle_Galle_District_Southern_Province.html")
time.sleep(2)

csvfile = open("destination.csv", "a", newline="")
writer = csv.writer(csvfile)
writer.writerow(["Title", "Rating", "Review", "Category"])

def web_scraper():
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    titles = soup.findAll("div", class_="XfVdV o AIbhI")
    ratings = [svg.get('aria-label') for svg in soup.findAll("svg", class_="UctUV d H0 hzzSG")]
    reviews = soup.findAll("span", class_="biGQs _P pZUbB osNWb")
    categories = soup.findAll("div", class_="biGQs _P pZUbB hmDzD")

    rows = [[title.text, rating, review.text, category.text] for title, rating, review, category in
            zip(titles, ratings, reviews, categories)]
    writer.writerows(rows)

    csvfile.close()


while True:
    try:
        web_scraper()
        next_button_xpath = """/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div"""
        next_page = driver.find_element(By.XPATH, next_button_xpath)
        next_page.click()
        time.sleep(2)
    except Exception as e:
        print("Pagination over")
        break

driver.quit()
print("Finished web scraping")
