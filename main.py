from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import random


def web_scraper(driver, writer):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    titles = soup.findAll("div", class_="XfVdV o AIbhI")
    ratings = soup.findAll("svg", class_="UctUV d H0 hzzSG")
    reviews = soup.findAll("span", class_="biGQs _P pZUbB osNWb")
    categories = soup.findAll("div", class_="biGQs _P pZUbB hmDzD")

    rows = [[title.text, rating, review.text, category.text] for title, rating, review, category in
            zip(titles, ratings, reviews, categories)]
    writer.writerows(rows)


def main():
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tripadvisor.com/Attractions-g2467810-Activities-oa0-Southern_Province.html")
    time.sleep(random.randint(5, 15))

    with open("destination.csv", "a", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Rating", "Review", "Category"])

        while True:
            try:
                web_scraper(driver, writer)
                next_button_xpath = """/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div"""
                next_page = driver.find_element(By.XPATH, next_button_xpath)
                next_page.click()
                time.sleep(random.randint(5, 15))
            except Exception as e:
                print("An error occurred:", e)
                break


if __name__ == "__main__":
    main()
