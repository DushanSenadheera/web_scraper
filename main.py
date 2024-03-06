import csv
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def web_scraper(driver, writer):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    titles = soup.findAll("div", class_="XfVdV o AIbhI")
    reviews = soup.findAll("span", class_="biGQs _P pZUbB osNWb")
    categories = soup.findAll("div", class_="biGQs _P pZUbB hmDzD")

    for title, review, category in zip(titles, reviews, categories):
        original_tab = driver.current_window_handle
        title_link = driver.find_element(By.LINK_TEXT, title.text)
        title_link.click()
        time.sleep(random.randint(5, 15))

        new_tab = [tab for tab in driver.window_handles if tab != original_tab][0]
        driver.switch_to.window(new_tab)

        wait = WebDriverWait(driver, 10)
        details = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div/span")))
        location = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[1]/div[1]/div/div/div[5]/a/span/span")))
        rating = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[1]/div/div/div/div/div[1]/div[1]/a/div")))
        duration = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[2]/div/div/div/div[1]/div[1]/div/div[3]/div[2]/div/div")))

        # Extract the details
        details_text = details.text
        location_text = location.text
        rating_text = rating.text
        duration_text = duration.text

        writer.writerow([title.text, rating_text, review.text, category.text, details_text, location_text, duration_text])

        driver.close()
        driver.switch_to.window(original_tab)


def main():
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.tripadvisor.com/Attractions-g2467810-Activities-oa0-Southern_Province.html")
    time.sleep(random.randint(5, 15))

    with open("destination.csv", "a", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Rating", "Review", "Category", "About", "Location", "Duration"])

        while True:
            try:
                web_scraper(driver, writer)
                next_button_xpath = """/html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div"""
                next_page = driver.find_element(By.XPATH, next_button_xpath)
                next_page.click()
                time.sleep(random.randint(5, 15))
            except Exception as e:
                print("Error : ", e)
                break


if __name__ == "__main__":
    main()
