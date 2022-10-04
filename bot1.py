from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Login info
username = ""
password = ""

def get_data(html):
    data = ""
    soup = BeautifulSoup(html, "html.parser")

    lines = soup.find("table").find_all("tr")
    for line in lines:
        if "color: yellow" in str(line):
            helper = line.get_text().strip()
            data += f"{'~' * 50}\n\n"
            data += f"{'#' * 50}\n"
            data += f"{'#' + helper}\n"
            data += f"{'#' * 50}\n\n"
            continue

        for cell in line.find_all("td"):
            data += cell.get_text(separator="\n").strip() + " | "
        data += "\n\n"

    return data

def main():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    print("=> Loading...")

    driver.get("https://qldt.hust.edu.vn/")

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-login-main-style")))
    except:
        print("Error!")
    driver.find_element(By.CLASS_NAME, "btn-login-main-style").click()

    try:
        wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "đăng nhập")))
    except:
        print("Error!")
    driver.find_element(By.PARTIAL_LINK_TEXT, "đăng nhập").click()

    driver.find_element(By.CSS_SELECTOR, "input[class='texBoxLogin'][type='text']").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "input[class='texBoxLogin'][type='password']").send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn-login").click()

    sleep(7)
    driver.get("https://qldt.hust.edu.vn/#dang-ky-nguyen-vong")
    
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]")))
    except:
        print("Error!")
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[4]/div[2]").click()

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "option[value='5129919684149249']")))
    except:
        print("Error!")
    driver.find_element(By.CSS_SELECTOR, "option[value='5129919684149249']").click()

    sleep(7)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/form/div[1]/div/div/div[16]/div[2]/a").click()
    sleep(7)
    entry = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/table")

    # Pass the page to Beautiful Soup
    html = entry.get_attribute("innerHTML")
    data = get_data(html)

    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Close']")))
    except:
        print("Error!")
    driver.find_element(By.XPATH, "//*[text()='Close']").click()

    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(data)

    print("=> Extract complete!")
    print("=> Exiting...")
    driver.quit()

if __name__ == "__main__":
    main()