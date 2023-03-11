import os
from time import sleep

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Login info
load_dotenv()
username = os.getenv("USER")
password = os.getenv("PASSWORD")

# Others
search = None


def main():
    search = input("Enter your search: ")
    if os.path.exists("jobs.html"):
        with open("jobs.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            data = get_data(soup)
            data_filtered = get_data(soup, search)
        with open("jobs.txt", "w", encoding="utf-8") as f:
            f.write(data)
        with open("jobs-filtered.txt", "a", encoding="utf-8") as f:
            f.write(data_filtered)
        print("=> Extract complete!")
        return

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    print("=> Loading...")

    driver.get("https://qldt.hust.edu.vn/")

    try:
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "btn-login-main-style")))
    except:
        print("Error!")
    driver.find_element(By.CLASS_NAME, "btn-login-main-style").click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "đăng nhập")))
    except:
        print("Error!")
    driver.find_element(By.PARTIAL_LINK_TEXT, "đăng nhập").click()

    driver.find_element(
        By.CSS_SELECTOR, "input[class='texBoxLogin'][type='text']").send_keys(username)
    driver.find_element(
        By.CSS_SELECTOR, "input[class='texBoxLogin'][type='password']").send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    sleep(4)

    driver.get("https://qldt.hust.edu.vn/#dang-ky-nguyen-vong")

    try:
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, "Đăng ký")))
    except:
        print("Error!")
    driver.find_element(By.PARTIAL_LINK_TEXT, "Đăng ký").click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]/div")))
    except:
        print("Error!")
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]/div").click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]/div/div/ul/li[4]/a")))
    except:
        print("Error!")
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]/div/div/ul/li[4]/a").click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "option[value='IT4948']")))
    except:
        print("Error!")
    driver.find_element(
        By.CSS_SELECTOR, "option[value='IT4948']").click()

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[16]/div[2]/a")))
    except:
        print("Error!")
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[16]/div[2]/a").click()
    sleep(4)

    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[4]/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table")))
    except:
        print("Error!")
    entry = driver.find_element(
        By.XPATH, "/html/body/div[4]/div/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table")

    # Pass the page to Beautiful Soup
    html = entry.get_attribute("innerHTML")
    with open("jobs.html", "w", encoding="utf-8") as f:
        f.write(html)
    soup = BeautifulSoup(html, "html.parser")
    data = get_data(soup)
    data_filtered = get_data(soup, search)
    with open("jobs.txt", "w", encoding="utf-8") as f:
        f.write(data)
    with open("jobs-filtered.txt", "a", encoding="utf-8") as f:
        f.write(data_filtered)

    print("=> Extract complete!")
    print("=> Exiting...")
    driver.quit()


def get_data(soup, search=None):
    data = ""
    lines = soup.find("tbody").find_all(recursive=False)
    for i, line in enumerate(lines):
        if "background-color: yellow; color: blue; font-size: 1.2em" in str(line):
            if not search:
                helper = line.get_text().strip()
                data += f"{'#' * 50}\n"
                data += f"{'#' + ' ' + helper}\n"
                data += f"{'#' * 50}\n\n"
            continue

        cells = line.find_all("td")
        cell0 = "# " + cells[0].get_text(separator=" | ").strip() + "\n"
        cell1 = cells[1].get_text(separator="\n").strip() + "\n\n"

        if search:
            if search.lower() in cell1.lower():
                data += cell0
        else:
            data += cell0
            data += cell1

    return data


if __name__ == "__main__":
    main()
