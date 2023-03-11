import csv
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


def main():
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
    driver.get("https://qldt.hust.edu.vn/#company")

    # Click button
    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/table[1]/tbody/tr/td[3]/table/tbody/tr/td[2]/select")))
    except:
        print("Error!")

    # Select more rows
    numRowsList = Select(driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/table[1]/tbody/tr/td[3]/table/tbody/tr/td[2]/select"))
    numRowsList.select_by_visible_text("200")

    # Get number of rows and columns
    sleep(2)
    numRows = len(driver.find_elements(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table/tbody[1]/tr"))

    # Sort rows
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table/thead/tr/th[5]").click()
    sleep(2)
    driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table/thead/tr/th[5]").click()

    # Get table1
    table1 = driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table")

    # Pass table1 to Beautiful Soup
    html1 = table1.get_attribute("innerHTML")
    data1 = get_data1(html1)

    # Write data1 to file
    with open("data1.txt", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerows(data1)

    # Loop through rows
    data2 = None
    startRow = int(input("=> Start [1]: ") or "1")
    for i in range(startRow, numRows + 1):
        # Print progress
        print(
            f"=> Company {str(i).zfill(len(str(numRows)))}/{numRows}")

        # Show more details
        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, f"/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table/tbody[1]/tr[{i}]/td[2]/div/a")))
        except:
            print("Error!")
        entry = driver.find_element(
            By.XPATH, f"/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/table/tbody[1]/tr[{i}]/td[2]/div/a")
        driver.execute_script(
            "arguments[0].scrollIntoView(true); window.scrollBy(0, -window.innerHeight / 4);", entry)
        entry.click()
        sleep(4)

        # Get name of company
        try:
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div[class='BOB']")))
        except:
            print("Error!")
        companyTag = driver.find_element(
            By.CSS_SELECTOR, "div[class='BOB']")
        driver.execute_script(
            "arguments[0].scrollIntoView(true); window.scrollBy(0, -window.innerHeight / 4);", companyTag)
        companyTxt = companyTag.text

        sleep(4)
        navBarTag = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/ul")
        navBarTag.find_element(By.PARTIAL_LINK_TEXT, "Đề tài").click()
        sleep(4)

        # Handle popup
        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[7]/div/div/div[2]/button")))
            driver.find_element(
                By.XPATH, "/html/body/div[7]/div/div/div[2]/button").click()
        except:
            pass

        # Select more rows
        numRowsList = Select(driver.find_element(
            By.XPATH, "//*[@id='topic']/div/div/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]/select"))
        numRowsList.select_by_visible_text("200")

        # Get table2
        table2 = driver.find_element(
            By.XPATH, "//*[@id='topic']/div/div/div[3]/div/table")

        # Pass table2 to Beautiful Soup
        html2 = table2.get_attribute("innerHTML")
        data2 = get_data2(html2, companyTxt)

        # Write data2 to file
        with open("data2.txt", "a", encoding="utf-8") as file:
            file.write(f"{data2}\n")

        navBarTag = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/ul")
        driver.execute_script(
            "arguments[0].scrollIntoView(true); window.scrollBy(0, -window.innerHeight / 4);", navBarTag)
        navBarBtn = driver.find_element(By.PARTIAL_LINK_TEXT, "Thông tin")
        driver.execute_script(
            "arguments[0].scrollIntoView(true); window.scrollBy(0, -window.innerHeight / 4);", navBarBtn)
        navBarBtn.click()

        # Close popup
        closeBtn = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div[1]/button")
        driver.execute_script(
            "arguments[0].scrollIntoView(true); window.scrollBy(0, -window.innerHeight / 4);", closeBtn)
        closeBtn.click()
        sleep(2)

    print("=> Extract complete!")
    print("=> Exiting...")
    driver.quit()


def get_data1(doc):
    data = []
    soup = BeautifulSoup(doc, "html.parser")

    # Add list of headers to data
    thead = soup.find("thead")
    data.append([header.get_text("\n", strip=True)
                for header in thead.find_all("th")])

    # Add list of rows to data
    tbody = soup.find("tbody")
    for row in tbody.find_all("tr"):
        data.append([cell.get_text("\n", strip=True)
                    for cell in row.find_all("td")])

    return data


def get_data2(doc, company):
    data = ""
    soup = BeautifulSoup(doc, "html.parser")

    data += f"{'#' * 80}\n"
    data += f"# {company}\n"
    data += f"{'#' * 80}\n"

    # Add list of rows to data
    rows = soup.find("tbody").children
    for row in rows:
        data += f"{'*' * 80}\n"
        for cell in row.children:
            data += f"{'-' * 80}\n"
            strs = [" ".join(text.split()) for text in cell.stripped_strings]
            data += "\n".join(strs) + "\n"
        data += f"{'*' * 80}\n\n"

    return data


if __name__ == "__main__":
    main()
