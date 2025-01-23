
from time import sleep
import logging

logging.basicConfig(
    filename='scraper.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

logger = logging.getLogger(__name__)

all_extracted_data = []
def Data_extraction(page, context, extracted_number):
    # all_extracted_data = []
    for i in range(extracted_number):
                job_divs_locator = page.locator('//div[@class="mr-4 hidden sm:flex"]')
                job_div = job_divs_locator.nth(i)
                
                try:
                    job_div.wait_for(state="attached")
                    job_div.scroll_into_view_if_needed()
                    page.wait_for_timeout(500)  # Optional stability delay
                    
                    # Debug to confirm element interaction
                    logger.info(f"Attempting to click jobs")
                    job_div.hover()  # Optional: Check targeting
                    job_div.click(force=True)  # Use force to bypass potential obstructions
                    # print(f"Clicked job {i}")
                    sleep(3)
                    
                    new_window = context.wait_for_event("page",timeout=10000)
                    new_page = new_window

                    new_page.wait_for_selector('//div[@class="text-blue-600 ellipsis"]//a', timeout=30000) 
                    link_locator = new_page.locator('//div[@class="text-blue-600 ellipsis"]//a')
                    link_count = link_locator.count()
                    
                    unique_list = set()
                    for i in range(link_count):
                        try:
                            job_link = link_locator.nth(i).get_attribute('href')
                            if job_link:
                                unique_list.add(job_link)
                            # print(f"Job Link: {job_link}")
                        except Exception as e:
                            print("link not found")  
                    
                    href = list(unique_list)
                    # print(f"hrefs: ${href}")    
                    
                    # Founder data
                    new_page.wait_for_selector('//div[@class="ml-2 w-full sm:ml-9"]//div[@class="mb-1 font-medium"]', timeout=10000)
                    new_page.wait_for_selector('//div[@class="ml-2 w-full sm:ml-9"]//a', timeout=10000)      
                    
                    founder_names = new_page.locator('//div[@class="ml-2 w-full sm:ml-9"]//div[@class="mb-1 font-medium"]')
                    founder_count = founder_names.count()
                    
                    founder_links = new_page.locator('//div[@class="ml-2 w-full sm:ml-9"]//a')
                    founder_links_count = founder_links.count()
                    
                    unique_founder_names = set()
                    unique_founder_links = set()
                    for i in range(founder_count):
                        try:
                            name = founder_names.nth(i).text_content().strip()
                            if name:  # Ensure the name is not empty
                                unique_founder_names.add(name)
                        except Exception as e:
                            logger.error(f"Error extracting founder name {i + 1}: {e}")
                            
                    for i in range(founder_links_count):
                        try:
                            href = founder_links.nth(i).get_attribute('href')
                            if href and "linkedin.com" in href:  # Filter only LinkedIn URLs
                                unique_founder_links.add(href)
                        except Exception as e:
                            logger.error(f"Error extracting LinkedIn link {i + 1}: {e}")
                            
                    founder_names_list = list(unique_founder_names)
                    founder_links_list = list(unique_founder_links)    
                    
                    if len(founder_names_list) == len(founder_links_list):
                        paired_founders = list(zip(founder_names_list, founder_links_list))
                        # print("Paired Founders (Name, LinkedIn):", paired_founders)
                    else:
                        logger.error("Mismatched counts; cannot pair names with links.")    
                        
                        
                    # Job data    
                    new_page.wait_for_selector('//div[@class="job-name"]//a', timeout=10000)
                    new_page.wait_for_selector('//div[@class="mr-2 text-sm sm:mr-3 sm:flex sm:flex-wrap"]//span', timeout=10000)

                    # Extract job names and their links
                    job_links = new_page.locator('//div[@class="job-name"]//a')
                    job_count = job_links.count()

                    # Extract job specifications
                    job_specs = new_page.locator('//div[@class="mr-2 text-sm sm:mr-3 sm:flex sm:flex-wrap"]//span')
                    spec_count = job_specs.count()

                    # Using sets to avoid duplicates
                    unique_jobs = set()
                    unique_specs = set()

                    # Extract job names and links
                    for i in range(job_count):
                        try:
                            job_name = job_links.nth(i).text_content().strip()
                            job_href = job_links.nth(i).get_attribute('href')
                            if job_name and job_href:  # Ensure both name and link exist
                                unique_jobs.add((job_name, job_href))  # Store as tuple for easy pairing
                        except Exception as e:
                            logger.error(f"Error extracting job {i + 1}: {e}")

                    # Extract job specifications
                    for i in range(spec_count):
                        try:
                            spec = job_specs.nth(i).text_content().strip()
                            if spec:  # Ensure the specification is not empty
                                unique_specs.add(spec)
                        except Exception as e:
                            logger.error(f"Error extracting job specification {i + 1}: {e}")

                    # Convert sets to lists for further processing
                    job_list = list(unique_jobs)
                    spec_list = list(unique_specs)

                    
                    
                   # Tech Stack data
                    new_page.wait_for_selector('//p', timeout=10000)

                    # Locate all <p> elements
                    paragraphs = new_page.locator('//p')
                    p_count = paragraphs.count()

                    # Store the formatted tech stack
                    formatted_tech_stack = []

                    for i in range(p_count):
                        try:
                            # Extract content from <strong> and its surrounding text
                            paragraph_text = paragraphs.nth(i).evaluate(
                                """el => {
                                    const strongElement = el.querySelector('strong');
                                    if (strongElement) {
                                        const strongText = strongElement.textContent.trim();
                                        const surroundingText = el.textContent.replace(strongText, '').trim();
                                        return `${strongText}: ${surroundingText}`;
                                    } else {
                                        return el.textContent.trim();
                                    }
                                }"""
                            )
                            # print(f"Extracted Tech Stack from Paragraph {i+1}: {paragraph_text}")
                            if paragraph_text and paragraph_text not in formatted_tech_stack:  # Avoid duplicates
                                formatted_tech_stack.append(paragraph_text)
                        except Exception as e:
                            logger.error(f"Error extracting tech stack from paragraph {i+1}: {e}")

                    # logger.info(f"Formatted Tech Stack: {formatted_tech_stack}")
                    
                    new_page.wait_for_selector('//div[@class="text-2xl font-medium"]//span', timeout=10000)
                    new_page.wait_for_selector('//img[@class="mt-2 sm:w-28"]', timeout =10000)
                    new_page.wait_for_selector('//img[@class="ml-2 mr-2 h-20 w-20 rounded-full sm:ml-5"]', timeout=10000)
                    
                    company_image_locator = new_page.locator('//img[@class="mt-2 sm:w-28"]')
                    founder_image_locator = new_page.locator('//img[@class="ml-2 mr-2 h-20 w-20 rounded-full sm:ml-5"]')
                    company_name_locator = page.locator('//div[@class="text-2xl font-medium"]//span')
                    
                    company_images = []
                    founder_images = []
                    company_names = []
                    
                    company_image_count = company_image_locator.count()
                    # logger.info(f"Found {company_image_count} company images.")
                    
                    for i in range(company_image_count):
                        try:
                            src = company_image_locator.nth(i).get_attribute("src")
                            if src and src not in company_images:
                                company_images.append(src)
                        except Exception as e:
                            logger.error(f"Error extracting company image {i+1}: {e}")    
                    
                    company_name_count = company_name_locator.count()
                    # logger.info(f"Found {company_name_count} company names.")

                    # Extract company names
                    for i in range(company_name_count):
                        try:
                            # Extract and clean the company name text
                            company_name = company_name_locator.nth(i).inner_text().strip()

                            if company_name and company_name not in company_names:  # Avoid duplicates
                                company_names.append(company_name)
                                # logger.info(f"Extracted company name: {company_name}")

                        except Exception as e:
                            logger.error(f"Error extracting company name {i+1}: {e}")

                    # Print the final list of company names
                    # print(f"Company names: {company_names}")
                    
                            
                    founder_image_count = founder_image_locator.count()
                    # print(f"Found {founder_image_count} profile images.")     
                    
                    for i in range(founder_image_count):
                        try:
                            src = founder_image_locator.nth(i).get_attribute("src")
                            if src and src not in founder_images:
                                founder_images.append(src)   
                        except Exception as e:
                            logger.error(f"Error extracting profile image {i+1}: {e}")
                
                    
                    extracted_data = {
                        "hrefs": {
                            "link":href,
                            "company_image":company_images},
                        "founders": {
                            "founder_images": founder_images,
                            "founder_names": paired_founders
                            },
                        "jobs": job_list,
                        "specifications": spec_list,
                        "tech_stack": formatted_tech_stack,
                    }
                    
                    all_extracted_data.append(extracted_data)
                    # Close the new page to return to the main page (if needed)
                    new_page.close()
                    # print(f"Processed job {i} successfully")

                    # Add a small delay before processing the next job
                    page.wait_for_timeout(2000)


                    # Add logic for further processing after click
                    sleep(10)  # Debugging delay (replace with appropriate waits in production)
                
                except Exception as e:
                    logger.error(f"Error clicking job {i}: {e}")   
    return all_extracted_data
