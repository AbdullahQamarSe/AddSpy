from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .models import Category
import time

chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/ads/library")
time.sleep(10)

input_field_classes = ".xeuugli.x2lwn1j.x6s0dn4.x78zum5.x1q0g3np.x1iyjqo2.xozqiw3.x19lwn94.xh8yej3"
input_field = driver.find_elements(By.CSS_SELECTOR, input_field_classes)

data_array = []

for i in range(1, 300):  # Assuming there are 5 iterations
    try:
        select = input_field[1].find_element(By.XPATH, f"/html/body/div[1]/div[1]/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div/div[1]")
        select.click()
        
        select = input_field[1].find_element(By.XPATH, f"/html/body/div[1]/div[1]/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div[4]/div/div[2]/div[{i}]")
        select.click()
        
        print_text = input_field[1].text
        print_text2 = print_text.replace("\nAd category", "")
        data_array.append(print_text2)

        
        select = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div")
        select.click()
        
        print1 = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[2]")
        print_text = print1.text.replace("\n", " - ")
        data_array.append(print_text)
        
        segments = print_text.split(" - ")

        # Create a list to store all the words
        all_words = []

        # Loop through each segment and split it further by spaces
        for segment in segments:
            print(segment)
            
            Category.name = segment
            Category.country = print_text2
            Category.save
            


    except:
        continue


with open("output.txt", "w") as file:  # Use write mode
    for item in data_array:
        file.write("%s\n" % item)

# Close the browser
driver.quit()
