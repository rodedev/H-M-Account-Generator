import random
import string
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# This script automates the registration process on the H&M website using Playwright.
# It uses proxies from a file, generates random email and password, and saves the account details.
# If you have a problem, join my discord server: https://discord.gg/apiland


def load_proxies():
    proxies = []
    with open("proxy.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ip, port, user, pwd = line.split(":")
            proxies.append({
                "server": f"http://{ip}:{port}",
                "username": user,
                "password": pwd
            })
    return proxies

def load_accounts():
    path = Path("hmacc.json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []

def save_account(account):
    accounts = load_accounts()
    accounts.append(account)
    Path("hmacc.json").write_text(json.dumps(accounts, indent=4), encoding="utf-8")

def generate_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gmail.com"

def generate_password():
    while True:
        pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 25)))
        if any(c.islower() for c in pwd) and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd) and ' ' not in pwd:
            return pwd

def generate_birth_date():
    return (str(random.randint(1, 28)).zfill(2),
            str(random.randint(1, 12)).zfill(2),
            str(random.randint(1980, 2005)))

def main():
    proxies = load_proxies()
    if not proxies:
        print("proxy.txt dosyasında proxy bulunamadı!")
        return

    proxy = random.choice(proxies)

    email = generate_email()
    password = generate_password()
    day, month, year = generate_birth_date()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
            proxy=proxy,
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(locale="en-GB", viewport={"width":1280, "height":720})
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-GB', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        page = context.new_page()
        page.goto("https://www2.hm.com/en_gb/register")
        time.sleep(5)

        page.locator('xpath=/html/body/div[1]/main/div/form/section/div/div[1]/input').fill(email)
        page.locator('xpath=/html/body/div[1]/main/div/form/div[1]/div[1]/input').fill(password)
        page.locator('xpath=//*[@id="dateOfBirth-D"]').fill(day)
        page.locator('xpath=//*[@id="dateOfBirth-M"]').fill(month)
        page.locator('xpath=//*[@id="dateOfBirth-Y"]').fill(year)

        page.wait_for_selector('xpath=/html/body/div[1]/main/div/form/button[1]')
        time.sleep(3)
        page.locator('xpath=/html/body/div[1]/main/div/form/button[1]').click()

        print(f"[✓] Form gönderildi: {email} - {password} - {day}/{month}/{year}")
        print(f"[✓] Proxy kullanıldı: {proxy['server']} (kullanıcı: {proxy['username']})")

        save_account({
            "email": email,
            "password": password,
            "birth_date": f"{day}.{month}.{year}",
            "proxy": proxy
        })

        print("[*] Hesap hmacc.json dosyasına kaydedildi.")
        time.sleep(300)
        browser.close()

if __name__ == "__main__":
    main()
