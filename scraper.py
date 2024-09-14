from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


def set_search_filters(driver):
    try:
        try:
            cookie_reject_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))
            )
            cookie_reject_button.click()
            print("Cookie consent rejected")
        except:
            print("Cookie consent not found or already handled")

        driver.implicitly_wait(10)
        open_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__APP"]/div[2]/main/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div/div'))
        )
        open_button.click()
        driver.implicitly_wait(10)

        search_box = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__APP"]/div[2]/main/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[1]/div/input'))
        )
        search_box.send_keys("India")

        india_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__APP"]/div[2]/main/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]'))
        )
        india_button.click()

        time.sleep(5)
        driver.implicitly_wait(10)
    except Exception as e:
        raise e


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://p2p.binance.com/en/trade/all-payments/USDT?fiat=INR"
driver.get(url)
time.sleep(5)

set_search_filters(driver)

csv_filename = "binance_trade_data.csv"
headers = ["Trader Name", "Price", "Available", "Order Limit", "Completion Percentage", "Payment Modes"]

data_list = []

try:
    total_rows = 10
    for row in range(total_rows):
        data_row_list = []

        trader_name = driver.find_element(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[1]/div/div[1]/div[1]/a').text
        data_row_list.append(trader_name)

        price = driver.find_element(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[2]/div/div[1]').text
        data_row_list.append('₹' + price)

        available = driver.find_element(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[3]/div/div[1]').text
        data_row_list.append(available)

        order_limit_elements = driver.find_elements(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[3]/div/div[2]/*')
        order_limit_text = ' '.join([element.text for element in order_limit_elements])
        data_row_list.append(order_limit_text)

        completion_percentage = driver.find_element(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[1]/div/div[3]/div[1]/div[1]/div/div').text
        data_row_list.append(completion_percentage)

        payment_modes = driver.find_elements(By.XPATH, f'//*[@id="__APP"]/div[2]/main/div[2]/div[3]/div/div[1]/div/div/div/table/tbody/tr[{row+1}]/td[4]/div')
        payment_modes_text = ', '.join([mode.text for mode in payment_modes])
        data_row_list.append(payment_modes_text)

        data_list.append(data_row_list)

        with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(headers)
            writer.writerows(data_list)

        print(f"Saved: Trader: {trader_name}, Price: {price}, Available: {available}, Order Limit: {order_limit_text}, Completion: {completion_percentage}, Payment Modes: {payment_modes_text}")

finally:
    driver.quit()

print(f"Data has been saved to {csv_filename}")
