
import re
import os
from time import sleep

from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import json
import logging
from dotenv import load_dotenv
from components.data_extraction import Data_extraction
from schemas import Founders_data

logging.basicConfig(
    filename='scraper.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

logger = logging.getLogger(__name__)

load_dotenv()

username =  os.getenv("YC_Username")
password = os.getenv("YC_password")


def save_data_in_json(filename, data):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4) 



def Login(ycusername , ycpassword, number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
        
            page.goto("https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F", wait_until="domcontentloaded")
            
            
            logger.info("Login Page")
            username = page.locator('//div//input[@id="ycid-input"]')
            username.wait_for(state="visible", timeout=10000)
            username.click()
            username.fill(ycusername)
            
            page.wait_for_timeout(5000)
            password = page.locator('//div//input[@id="password-input"]')
            password.wait_for(state="visible", timeout=10000)
            password.click()
            password.fill(ycpassword)
            page.wait_for_timeout(5000)
            
            login_button = page.locator('//button//span[text()="Log in"]')
            login_button.wait_for(state="visible", timeout=10000)
            login_button.click()
            
            logger.info("Logged In")
            page.wait_for_timeout(40000)
            
            role = page.locator('//div[@id="role"]//div[@class=" css-tlfecz-indicatorContainer"]')
            role.wait_for(state="visible", timeout=10000)
            role.click()
            
            option = page.locator('//div[@id="role"]//div[contains(text(), "Engineering")]')
            option.wait_for(state="visible", timeout=10000)
            option.click()
            
            page.wait_for_timeout(5000)
            
            page.mouse.wheel(0, 1000)
            remote = page.locator('//div[@id="remote"]//div[@class=" css-tlfecz-indicatorContainer"]')
            remote.wait_for(state="visible", timeout=10000)
            remote.click()
            
            option_remote = page.locator('//div[@id="remote"]//div[contains(text(), "Remote only")]')
            option_remote.wait_for(state="visible", timeout=10000)
            option_remote.click()
            
            
            sleep(3)
            div_locator = page.locator('//div[@class="mb-4 mt-3 flex w-full w-full items-center justify-between lg:mt-0 lg:w-auto"]')
            p_locator = div_locator.locator('p')  # Locate the <p> tag inside the div
            
            # Extract the text content from the <p> tag
            p_text = p_locator.text_content()
            # print(f"Text content of <p>: {p_text}")

            # Use a regular expression to extract only the number from the text
            number_match = re.search(r'\d+', p_text)  # Extract the first number (digits)

            if number_match:
                extracted_number = int(number_match.group())  # Get the matched number
                logger.info(f"Extracted number: {extracted_number}")
            else:
                logger.error("No number found in the text.")
                
            extracted_YC_data = Data_extraction(page, context, number) 
            
            logging.info(f"Extracted data: {extracted_YC_data}")
            save_data_in_json("extracted_data.json", extracted_YC_data)   
            
            logger.info(f"data extracted successfully") 
            
            if extracted_YC_data:
                return extracted_YC_data
            else:
                return {"error": "No data found"}      
             
        except Exception as e:
            logger.error("error",e)   
        finally:
            browser.close()     


if __name__ == "__main__":
    res = Login(username, password, 3)
    print("res", type(res))    
        
        