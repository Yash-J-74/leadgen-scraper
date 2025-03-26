import time
from typing import List, Dict
from playwright.sync_api import sync_playwright
import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

BASE_URL = "https://www.google.com/maps"

def launch_browser():
    """Initialize a Playwright browser session."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    return browser, p

def scrape_business(query: str, location: str) -> Dict:
    """Scrape business details from Google Maps."""
    browser, p = launch_browser()
    try:
        page = browser.new_page()
        page.goto(BASE_URL)

        # Search for the query and location
        search_query = f"{query} in {location}"
        page.fill("input[name='q']", search_query)
        page.keyboard.press("Enter")
        time.sleep(5)  # Wait for results to load

        # Check if the page is a direct business page                          
        if page.locator("div.w6VYqd").is_visible():
            print(f"Found {query} businesses in {location}.")
            # Extract details from the direct business page
            try:                    
                name = page.get_by_role("heading", name=query).text_content()
                
                category_locator = page.locator("button.DkEaL")
                category = category_locator.inner_text() if category_locator.count() > 0 else "NA"
                    
                address = page.locator("div.rogA2c div.Io6YTe").nth(0).text_content()
                
                rating_div = page.locator(".dmRWX")
                if (rating_div.count() == 0):
                    rating = "NA"
                else:
                    is_rating_visible = page.locator(".dmRWX").evaluate("el => getComputedStyle(el).display !== 'none'")
                    rating = page.locator("div.F7nice span[aria-hidden='true']").text_content() if is_rating_visible else "N/A"
                    
                phone_btn = page.locator("button[aria-label^='Phone:']")
                phone_no = phone_btn.get_attribute("aria-label").replace("Phone: ", "").strip() if phone_btn.count() > 0 else "N/A"  
                
                website_locator = page.locator("a[aria-label^='Website:']")
                website = website_locator.get_attribute("href") if website_locator.count() > 0 else "N/A"
                    
                # print(f"Extracted: {name}, {category}, {address}, {website}, {rating}")
                return {
                    "Name": name,
                    "Category": category,
                    "Address": address,
                    "Rating": rating,
                    "Phone": phone_no,
                    "Website": website
                }
                
            except Exception as e:
                raise Exception(f"Error extracting data: {e}")
        else:
            return {"error": f"No business details found for {query} in {location}."}
                
    except Exception as e:
        raise RuntimeError(f"An error occurred while scraping: {e}")
    finally:
        browser.close()
        p.stop()
        

def scrape_multiple_businesses(query: str, location: str) -> List[Dict]:
    """Scrape multiple businesses from Google Maps."""
    browser, p = launch_browser()
    try:
        page = browser.new_page()
        page.goto(BASE_URL)

        # Search for the query and location
        search_query = f"{query} in {location}"
        page.fill("input[name='q']", search_query)
        page.keyboard.press("Enter")
        time.sleep(5)  # Wait for results to load
        
        business_containers = page.locator("div.bfdHYd.Ppzolf.OFBs3e")
        print(f"Found {business_containers.count()} businesses for {query} in {location}.")
        if business_containers.count() == 0:
            print("No businesses found.")
            browser.close()
            exit()
            return []
        else:
            business_list = []
                
            for i in range(business_containers.count()):
                container = business_containers.nth(i)
                try:
                    company_name = container.locator("div.qBF1Pd.fontHeadlineSmall").text_content().strip() if container.locator("div.qBF1Pd.fontHeadlineSmall").count() > 0 else "NA"
                    
                    second_info_div = container.locator("div.W4Efsd").nth(2)
                    info_spans = second_info_div.locator("span").all()
                    info_texts = [span.text_content().strip() for span in info_spans if span.text_content().strip() and span.text_content().strip() != "·"]

                    category = info_texts[0] if len(info_texts) > 0 else "NA"
                    address = info_texts[-1] if len(info_texts) > 1 else "NA"
                    
                    rating_element = container.locator("span[aria-label*='stars']")
                    rating = rating_element.get_attribute("aria-label").split(" stars")[0] if rating_element.count() > 0 else "NA"

                    phone_element = container.locator("span.UsdlK")
                    phone = phone_element.text_content().strip() if phone_element.count() > 0 else "NA"

                    website_element = container.locator("a[aria-label^='Visit']")
                    website = website_element.get_attribute("href") if website_element.count() > 0 else "NA"
                    
                    business_list.append({
                        "Name": company_name,
                        "Category": category,
                        "Address": address,
                        "Rating": rating,
                        "Phone": phone,
                        "Website": website
                    })
                except Exception as e:
                    raise Exception(f"Error extracting data: {e}")
                
            return business_list
                
    except Exception as e:
        raise RuntimeError(f"An error occurred while scraping: {e}")
        
    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    # Example usage
    query = "Banks"
    location = "Vancouver, BC"
    print(scrape_multiple_businesses(query, location))
    # find_competitors(query, location)