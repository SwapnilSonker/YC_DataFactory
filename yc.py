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
            
            
            sleep(10)
            
            # page.screenshot(path="logged_in_screenshot.png")
        except Exception as e:
            print("error",e)    
        
        
if __name__ == "__main__":
    login()
    
        
        