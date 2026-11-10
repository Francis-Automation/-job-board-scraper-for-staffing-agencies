import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("Launching browser...")

options = webdriver.FirefoxOptions()
options.page_load_strategy = "eager"
driver = webdriver.Firefox(options=options)

search_phrases = [
    "Newly qualified nurse",
    "Pre-registered nurse",
    "New Graduate Nurse",
    "Band 5 nurse"
]

csv_filename = "nhs_nurse_jobs.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Search Phrase", "Job Title", "Trust", "Salary", "Closing Date", "Application Link"])

print("Starting NHS filter pipeline...")

try:
    driver.get("https://beta.jobs.nhs.uk/candidate/search/results")
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
        ).click()
    except:
        pass

    for phrase in search_phrases:
        print(f"\nTarget: {phrase}")
        formatted = "+AND+".join(phrase.lower().split())
        base_url = f"https://beta.jobs.nhs.uk/candidate/search/results?keyword={formatted}&sort=publicationDateDesc"

        for page in range(1, 51):  # 50 pages enough, 500 burns data
            url = f"{base_url}&page={page}"
            try:
                driver.get(url)
                time.sleep(2)
            except TimeoutException:
                continue

            if "Page not found" in driver.page_source:
                break

            job_cards = driver.find_elements(By.CSS_SELECTOR, "li[data-testid='search-result'], div.nhsuk-card")
            if not job_cards:
                job_cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/job-advert/')]/ancestor::li")

            if not job_cards:
                break

            with open(csv_filename, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for card in job_cards:
                    try:
                        link_el = card.find_element(By.CSS_SELECTOR, "a[href*='/job-advert/']")
                        job_title = link_el.text.strip()
                        if not job_title:
                            continue
                        
                        title_lower = job_title.lower()
                        card_text_lower = card.text.lower()

                        # BLOCK senior roles only
                        blacklist = ["senior", "sister", "charge", "matron", "manager", "lead", "head", "consultant", "advanced", "specialist", "deputy", "educator"]
                        if any(b in title_lower for b in blacklist):
                            continue

                        # ALLOW - must be entry level
                        if not ("band 5" in card_text_lower or "newly qualified" in title_lower or "pre-reg" in title_lower or "graduate" in title_lower or "newly qualified" in card_text_lower or "registered nurse" in title_lower or "staff nurse" in title_lower):
                            continue

                        job_url = link_el.get_attribute("href")
                        lines = [l.strip() for l in card.text.split("\n") if l.strip()]
                        
                        trust = lines[1] if len(lines) > 1 else "N/A"
                        salary = next((l for l in lines if "£" in l), "N/A")
                        closing = next((l for l in lines if "Closing" in l or "Closes" in l), "N/A")

                        writer.writerow([phrase, job_title, trust, salary, closing, job_url])
                        print(f"  Saved: {job_title[:45]}")

                    except:
                        continue

except Exception as e:
    print(f"Error: {e}")

finally:
    print(f"\nCompleted. Saved to {csv_filename}")
    driver.quit()
