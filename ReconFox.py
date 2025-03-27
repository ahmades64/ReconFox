from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import random
import time
import undetected_chromedriver as uc

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    driver = uc.Chrome(options=options)
    return driver

def is_internal_url(url, base_url):
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url)
    return parsed_url.netloc == parsed_base.netloc

def has_query_parameters(url):
    return '?' in url or '&' in url


def selenium_crawl(base_url, max_pages=50):
    visited = set()
    to_visit = [base_url]
    found_urls = set()
    found_forms = set()  
    found_comments = set()  
    found_login = set()  
    found_signup = set()  
    found_forgot_password = set()  
    found_profile_edit = set()  
    found_js_files = set()  
    driver = setup_driver()
    print(f"[🌐] Starting crawl on {base_url}\n")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            driver.get(url)
            time.sleep(random.uniform(1, 3))

            elements = driver.find_elements(By.TAG_NAME, "a")
            for elem in elements:
                href = elem.get_attribute("href")
                if href:
                    full_url = urljoin(url, href)

                    if is_internal_url(full_url, base_url):
                        found_urls.add(full_url)
                        if full_url not in visited:
                            to_visit.append(full_url)

            forms = driver.find_elements(By.TAG_NAME, "form")
            for form in forms:
                action = form.get_attribute("action")
                if action:
                    full_action_url = urljoin(url, action)
                    if is_internal_url(full_action_url, base_url):
                        found_forms.add(full_action_url)

            comment_inputs = driver.find_elements(By.CSS_SELECTOR, "textarea, input, button")
            for comment_input in comment_inputs:
                form_action = comment_input.get_attribute("formaction")
                if form_action:
                    full_action_url = urljoin(url, form_action)
                    if is_internal_url(full_action_url, base_url):
                        found_comments.add(full_action_url)

            scripts = driver.find_elements(By.TAG_NAME, "script")
            for script in scripts:
                src = script.get_attribute("src")
                if src:
                    full_src_url = urljoin(url, src)
                    if full_src_url.endswith('.js'):
                        found_js_files.add(full_src_url)

            print(f"[🔗] Crawled: {url} (found {len(elements)} links, {len(forms)} forms, {len(comment_inputs)} comment fields, {len(scripts)} scripts)")

        except Exception as e:
            print(f"[⛔] Error visiting {url}: {e}")
            continue

    driver.quit()
    return found_urls, found_forms, found_comments, found_login, found_signup, found_forgot_password, found_profile_edit, found_js_files

def save_urls_to_file(urls, forms, comments, js_files, login=None, signup=None, forgot=None, profile_edit=None, filename="urls.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        if urls:
            f.write("[🔗] URLs with Parameters:\n")
            for url in urls:
                f.write(url + "\n")
            f.write("\n")

        if forms:
            f.write("[📝] Forms:\n")
            for form in forms:
                f.write(form + "\n")
            f.write("\n")

        if comments:
            f.write("[💬] Comment Fields:\n")
            for comment in comments:
                f.write(comment + "\n")
            f.write("\n")

        if login:
            f.write("[🔐] Login Forms:\n")
            for item in login:
                f.write(item + "\n")
            f.write("\n")

        if signup:
            f.write("[🆕] SignUp Forms:\n")
            for item in signup:
                f.write(item + "\n")
            f.write("\n")

        if forgot:
            f.write("[❓] Forgot Password Forms:\n")
            for item in forgot:
                f.write(item + "\n")
            f.write("\n")

        if profile_edit:
            f.write("[👤] Profile Edit Forms:\n")
            for item in profile_edit:
                f.write(item + "\n")
            f.write("\n")

        if js_files:
            f.write("[💻] JavaScript Files:\n")
            for js in js_files:
                f.write(js + "\n")
            f.write("\n")

    print(f"\n[✅] The output file with categorized items has been saved to {filename}.")


def main():
    domain = input("🌐 Enter domain (e.g., https://example.com): ")
    urls, forms, comments, login, signup, forgot, profile_edit, js_files = selenium_crawl(domain)
    print(f"\n[✅] Crawling complete. Total URLs found: {len(urls)}")
    print(f"[✅] Total Forms found: {len(forms)}")
    print(f"[✅] Total Comment fields found: {len(comments)}")
    print(f"[✅] Total Login forms found: {len(login)}")
    print(f"[✅] Total SignUp forms found: {len(signup)}")
    print(f"[✅] Total Forgot Password forms found: {len(forgot)}")
    print(f"[✅] Total Profile Edit forms found: {len(profile_edit)}")
    print(f"[✅] Total JS files found: {len(js_files)}")

    save_urls_to_file(
        urls,
        forms,
        comments,
        js_files,
        login,
        signup,
        forgot,
        profile_edit
    )
if __name__ == "__main__":
    main()
