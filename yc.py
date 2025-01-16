import re
from time import sleep
from playwright.sync_api import sync_playwright

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
        
            page.goto("https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F", wait_until="domcontentloaded")
            # page.wait_for_timeout(50000)
            
            print("found")
            username = page.locator('//div//input[@id="ycid-input"]')
            username.wait_for(state="visible", timeout=10000)
            username.click()
            username.fill("Swapnil444")
            
            page.wait_for_timeout(5000)
            password = page.locator('//div//input[@id="password-input"]')
            password.wait_for(state="visible", timeout=10000)
            password.click()
            password.fill("Swapnil@04")
            page.wait_for_timeout(5000)
            
            login_button = page.locator('//button//span[text()="Log in"]')
            login_button.wait_for(state="visible", timeout=10000)
            login_button.click()
            
            print("in login")
            page.wait_for_timeout(40000)
            
            role = page.locator('//div[@id="role"]//div[@class=" css-tlfecz-indicatorContainer"]')
            role.wait_for(state="visible", timeout=10000)
            role.click()
            
            option = page.locator('//div[@id="role"]//div[contains(text(), "Engineering")]')
            option.wait_for(state="visible", timeout=10000)
            option.click()
            # role.fill("Engineering")
            # role.press('Enter')
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
            print(f"Text content of <p>: {p_text}")

            # Use a regular expression to extract only the number from the text
            number_match = re.search(r'\d+', p_text)  # Extract the first number (digits)

            if number_match:
                extracted_number = int(number_match.group())  # Get the matched number
                print(f"Extracted number: {extracted_number}")
            else:
                print("No number found in the text.")
                
                
            
            
            
            # jobcount = job_divs_locator.count()
            
            
            for i in range(extracted_number):
                job_divs_locator = page.locator('//div[@class="bg-beige-lighter  mb-5 rounded pb-4"]')
                job_div = job_divs_locator.nth(i)
                
                job_div.scroll_into_view_if_needed()  # Scroll into view if needed
                job_div.wait_for(state="visible")
                
                print("found the job")
                job_div.click()
                print("job is clicked")
                sleep(5)
                
                # new_window = context.wait_for_event("popup")
                
                # new_page = new_window

                # new_page.wait_for_selector('//div[@class="text-2xl font-medium"]//a', timeout=10000)  # Explicit wait

                
                # link_locator = new_page.locator('//div[@class="text-2xl font-medium"]//a').first()
                # job_link = link_locator.get_attribute('href')
                # print(f"Job Link: {job_link}")

                # company_name_locator = new_page.locator('//div[@class="text-2xl font-medium"]//a//span[@class="company-name hover:underline"]')
                # company_name = company_name_locator.text_content()
                # print(f"Company Name: {company_name}")

                # description_locator = new_page.locator('//div[@class="mt-3 text-gray-700"]')
                # company_description = description_locator.text_content()
                # print(f"Company Description: {company_description}")

                # image_locator = new_page.locator('//div//img[@class="mt-2 sm:w-28"]')
                # company_image_url = image_locator.get_attribute('src')
                # print(f"Company Image URL: {company_image_url}")
                
                # page.go_back()
                
                sleep(2)
                     
                
        except Exception as e:
            print("error",e)    
        
        
if __name__ == "__main__":
    login()
    
        
        