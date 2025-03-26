import time
from typing import List, Dict
from scraper import launch_browser, scrape_business, scrape_multiple_businesses, BASE_URL

def find_competitors(query: str, location: str) -> List[Dict]:
    browser, p = launch_browser()
    try:
        page = browser.new_page()
        page.goto(BASE_URL)

        # Search for the query and location
        search_query = f"{query} in {location}"
        page.fill("input[name='q']", search_query)
        page.keyboard.press("Enter")
        time.sleep(3)  # Wait for results to load
        
        if page.locator("div.w6VYqd").is_visible():
            print(f"Found {query} in {location}.")
            
            competitors = page.locator('.Ymd7jc.Lnaw4c').all()
            print(f"Found {len(competitors)} competitors.")
            
            competitor_list = []
            
            for comp in competitors:
                try:
                    name = comp.locator("span.GgK1If.fontTitleSmall").text_content()
                    category = comp.locator("div.Q5g20").text_content()
                    rating_element = comp.locator("span.MW4etd")
                    rating = rating_element.text_content() if rating_element.count() > 0 else "NA"
                    # print(f"Extracted: {name}, {category}, {rating}")
                    competitor_list.append({
                        "Name": name,
                        "Category": category,
                        "Rating": rating
                    })
                except Exception as e:
                    raise Exception(f"Error extracting data: {e}")
            
            return competitor_list
        
        else:
            print(f"Could not find {query} in {location}.")
            return []
                    
    except Exception as e:
        raise Exception(f"Error while scraping: {e}")
    finally:
        browser.close()
        p.stop()
        
def fetch_competitors(company, location) -> List[Dict]:
    category = scrape_business(company, location).get('Category')
    competitors = scrape_multiple_businesses(category, location)
    return competitors
