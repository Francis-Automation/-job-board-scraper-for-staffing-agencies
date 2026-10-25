import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

print("🌐 Launching browser environment via Selenium...")
driver = webdriver.Firefox()

# Targeted phrases for the search parameter strings
search_phrases = [
    "Newly qualified nurse",
    "Pre-registered nurse",
    "New Graduate Nurse",
    "International registered nurse"
]

csv_filename = "nhs_nurse_jobs.csv"

# Establish a single, pristine output CSV file with clean headers
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Search Phrase", "Job Title", "Employer/Trust", "Salary", "Closing Date", "Direct Application Link"])

print("🚀 INITIALIZING ALL-IN-ONE REAL-TIME FILTERING PIPELINE...")

try:
    driver.get("https://Beta.jobs.nhs.uk/candidate/search/results")
    time.sleep(3)
    
    # Handle the cookie acceptance overlay via Selenium click commands
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept analytics cookies')]"))
        )
        cookie_btn.click()
        time.sleep(1.5)
    except TimeoutException:
        pass

    for phrase in search_phrases:
        print(f"\n🎯 AUTOMATED TRACK RUNNING FOR: '{phrase}'")
        
        words = phrase.lower().split()
        formatted_keyword = "+AND+".join(words)
        base_url = f"https://Beta.jobs.nhs.uk/candidate/search/results?keyword={formatted_keyword}&sort=publicationDateDesc"
        
        for page_num in range(1, 501):
            print(f"📊 Selenium scanning page {page_num}...")
            
            target_page_url = f"{base_url}&page={page_num}"
            driver.get(target_page_url)
            time.sleep(3.5)
            
            if "Page not found" in driver.page_source:
                break
            
            # Smooth scrolling down to render dynamic page layouts completely
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.0)
            
            # Extract target list items using specific CSS element mappings
            job_cards = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='search-results-list'] > li, .nhsuk-card, li[class*='result']")
            if not job_cards:
                job_cards = driver.find_elements(By.XPATH, "//h2/ancestor::li | //a[contains(@href, '/job-advert/')]/ancestor::li")
            
            if not job_cards:
                break
                
            # Open the CSV with buffering=1 so valid rows lock onto your hard drive instantly
            with open(csv_filename, mode="a", newline="", encoding="utf-8", buffering=1) as file:
                writer = csv.writer(file)
                
                for card in job_cards:
                    try:
                        # Extract the inner title header element link anchor
                        try:
                            link_element = card.find_element(By.CSS_SELECTOR, "h2 a, h3 a, a[href*='/job-advert/']")
                        except NoSuchElementException:
                            continue
                            
                        job_title = link_element.text.strip()
                        job_title_lower = job_title.lower().strip()
                        
                        # ==========================================================
                        # 🛑 LIVE FILTER 1: THE CRITICAL BAN LIST (Skips Senior/Doctors)
                        # ==========================================================
                        blacklist = [
                            "senior", "sister", "charge", "manager", "lead", "advanced", "specialist", 
                            "practitioner", "consultant", "deputy", "head", "trainer", "educator", 
                            "receptionist", "clerk", "payroll", "gp", "doctor", "administrator",
                            "registered nurse", "rn", "anp", "enp", "clinical specialist"
                        ]
                        
                        # If title is exactly "registered nurse" or matches anything on the blacklist, ignore it!
                        if job_title_lower == "registered nurse" or any(bad_word in job_title_lower for bad_word in blacklist):
                            continue 
                            
                        # ==========================================================
                        # ✅ LIVE FILTER 2: THE core SELECTION ALLOW LIST
                        # ==========================================================
                        whitelist = ["nurse", "nursing", "band 5", "pre-registered", "graduate", "junior", "staff nurse", "assistant"]
                        if not any(good_word in job_title_lower for good_word in whitelist):
                            continue # Ignore if it doesn't match an entry level designation
                        
                        # If it passes both filters, Selenium grabs the direct application URL address
                        job_url = link_element.get_attribute("href")
                        
                        card_text = card.text or ""
                        lines = [line.strip() for line in card_text.split("\n") if line.strip()]
                        
                        trust_name = "N/A"
                        salary = "N/A"
                        closing_date = "N/A"
                        
                        if len(lines) > 1:
                            trust_name = lines[1]
                            
                        for text_line in lines:
                            if "£" in text_line or "Salary:" in text_line:
                                salary = text_line
                            elif "Closing date:" in text_line or "Closes:" in text_line:
                                closing_date = text_line
                        
                        # Write the clean match down to the CSV right away
                        writer.writerow([phrase, job_title, trust_name, salary, closing_date, job_url])
                        print(f"🌟 LIVE MATCH SAVED: {job_title}")
                        
                    except Exception:
                        continue
                        
            print(f"✅ Clean page processing completed for Page {page_num}")

except Exception as global_err:
    print(f"\n❌ Pipeline Halt: {global_err}")

finally:
    print("\n🧹 Selenium extraction sequence complete. Data file is locked and saved.")
    input("⏸ Press Enter directly inside this terminal window to close the browser... ")
    driver.quit()
