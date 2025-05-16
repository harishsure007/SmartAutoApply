from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_dice_jobs(search_term, num_pages=2, output_file="dice_jobs.csv"):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(), options=options)

    jobs = []

    for page in range(1, num_pages + 1):
        print(f"🌐 Scraping page {page}")
        url = f"https://www.dice.com/jobs?q={search_term.replace(' ', '%20')}&page={page}"
        driver.get(url)

        time.sleep(6)  # Give time for job cards to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        job_cards = driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")

        print(f"📝 Found {len(job_cards)} job cards")

        for job in job_cards:
            try:
                title = job.text
                link = job.get_attribute("href")
                card = job.find_element(By.XPATH, "..").find_element(By.XPATH, "..")  # go up to card div
                company = card.find_element(By.XPATH, ".//span[@data-cy='company-name']").text
                location = card.find_element(By.XPATH, ".//span[@data-cy='search-result-location']").text

                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Link": link
                })
            except Exception as e:
                print(f"⚠️ Skipping a job due to error: {e}")

    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv(output_file, index=False)
        print(f"✅ Scraped {len(jobs)} jobs. Saved to {output_file}")
    else:
        print("⚠️ No jobs scraped. Check XPath or wait time.")

    input("🔒 Press ENTER to close the browser and finish...")
    driver.quit()

if __name__ == "__main__":
    scrape_dice_jobs("data analyst", num_pages=2)
