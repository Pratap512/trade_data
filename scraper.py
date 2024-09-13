from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://p2p.binance.com/en/trade/all-payments/USDT?fiat=INR"

driver.get(url)
time.sleep(5)

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
