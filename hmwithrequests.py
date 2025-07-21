import requests
import random
import json
import os
import threading
import time, random

lock = threading.Lock()

def load_proxies(filename="proxy.txt"):
    proxies = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) != 4:
                continue
            ip, port, user, passwd = parts
            proxy_url = f"http://{user}:{passwd}@{ip}:{port}"
            proxies.append(proxy_url)
    return proxies

proxies_list = load_proxies()

def generate_random_email():
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10)) + "@gmail.com"

def generate_random_dob():
    y = random.randint(1980, 2003)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f"{y:04d}-{m:02d}-{d:02d}"

def save_account(email, password):
    with lock:
        filename = "hm_accounts.json"
        data = []
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                data = []
        data.append({"email": email, "password": password})
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def register(proxy_url=None):
    try:
        r = requests.Session()


        email = generate_random_email()
        password = "Rode" + str(random.randint(100000, 999999))
        birth = generate_random_dob()


        payload = {
            "email": email,
            "pwd": password,
            "day": birth[8:10],
            "month": birth[5:7],
            "year": birth[:4],
            "birthDate": birth,
            "recruiterBPID": "",
            "firstName": "mehmet",
            "lastName": "kayakci",
            "gender": "MALE",
            "postalCode": "27100",
            "prefix": "+90",
            "cellPhone": "5425552142",
            "hmClubJoin": "true"
        }

        headers = {
  "content-type": "application/json; charset=UTF-8",
  "cookie": "AKA_A2=A; HMCORP_locale=tr_TR; HMCOUNTRY_name=Turkey; akainst=EU2; hmid=5A537844-ED36-4466-89A5-7EB1AB4A737F; agCookie=d10491e1-86a6-4b1c-b64a-f2bb9817068c; INGRESSCOOKIE=1752958575.401.420.239542|074a41e4bac870997ed51f2ee5b39b32; utag_main__sn=1; utag_main_ses_id=1752958573914%3Bexp-session; dep_sid=s_9525446854132581.1752958573921; utag_main_segment=normal%3Bexp-session; utag_main__ss=0%3Bexp-session; HMCORP_locale_autoassigned=false; hmgroup_consent=datestamp=2025-07-19T20:56:59.875Z&url=https://www2.hm.com/tr_tr/index.html&consentId=97d9f83f-c976-46c3-a2aa-7afe6ca1d762&groups=C0001:1,C0002:1,C0003:1,C0004:1; OptanonConsent=datestamp=2025-07-19T20:56:59.875Z&url=https://www2.hm.com/tr_tr/index.html&consentId=c1b48e43-0b84-4fd3-974d-52ad916f94c9&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; _scid=8E2GcgEO1AXFxS7F-WrRWh1SQvIytfnt; _cs_ex=1741855907; _cs_c=0; _fbp=fb.1.1752958620595.70723496718252168; _ga=GA1.2.937285660.1752958621; _ScCbts=%5B%5D; _pin_unauth=dWlkPU9HSTVaV0k1WkRJdFl6UTRNUzAwTVdSa0xUbGlaall0WlRNeU16UmpZelk1WW1NeQ; _tt_enable_cookie=1; _ttp=01K0J7KNADY8K06N5F5JZPKA2D_.tt.1; _sctr=1%7C1752872400000; bm_ss=ab8e18ef4e; bm_mi=BCF75C863022A0BDE4FECEF840B8848A~YAAQtVPdWJBUDAmYAQAA/yV6JBxXdeVXFP2I0QVnBG2M9HekbLOWcQbhgcvzlikMv5HhaTMWA1xcN9d6aGhZWDheFF2cBYpxb4tyyz4u5f2YxUapSjyTDCWoAWckcPZtZEtxZ8dsY/dmnw1D4LsCXjSrBgXr6/dkp8VvMtbQk1QxB/co3KDrWP2vJ50sDXZpP/6v3KQ/PKmtv2WOisP5QXS29CSiLKcyuM+3BdKHglV8I6BmyL6yJcEJG/Ot04k026aI3BiKnHrnsBls2CWLUlEoV3DnOpdpU0nf0a1J90DGhoI1jSA4NGhydJSorzjNl06XqnxM+r8pPA==~1; ak_bmsc=1FB61D876F5683D232D0156416F6A9F9~000000000000000000000000000000~YAAQtVPdWOBUDAmYAQAAcS56JBxuHkVz9jsF2++UjawenyswIiBKsqdsAT/8dH8YLq/R5mVmB5rJ4CfUP0vaFqaGwbTtdVrxhmCIyQtHUSlbAphN+r//mARnoryqPoeqjCkkThneDcxhnJEmGqg/YLaz6QyQ9OgcJhK/Bionu4du/nX35YU3xVUQX5+Iijk827KY1S1d8A3fLrmRPUmWUUBtgncwfpaL+0uWkM23AZ0g937zrHse0jXRpso5ZN76ULpF8zRK1bI0alVB3t0Y7OGuCUTdIOXRjvuPn+DwohMHe/CSewiYEAO67JrSLbIags6+LhgIz0AhoO9hpxjld0Xjptd3AhexlceNG2x7/JJh03qTCk06Tu4oMF5oOxMCW0pL6E7XzowAs45HUMnkeVM+KTGLcYkOkJMj7YippYzpdFlKC9mLtdn6ggBzMASz3oIZ7Ex7pzu+52wxHGr246eRrT5Nq7bh31aga455ZG9+aNUr2q0s4cDSg9g=; uuidCookie=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..gJ0uIQ6-mprbgKehf1CRnA.hXF69QVoQwz7g0_Bnrz0_MOG6DT-0USahWqL3uNzt6_7ZbEZKgufYXA-Kf9vjH0KtCmtvSxUNNaHYE3GElSvts1sd6ry-Y0MteOKwANDe8pQC7U_gKh7sM2LKLPX-vRW9XJsZyQPPgRp-8tZXcCKAcS8zuqCsLRM97T8yyM-t2wWWm_DgO1cOaiegzjF7bAht9Yyhssuaf0dBWSOcSUHE6_tCRYPl0ZIouMZxcJ659p9CnPjClWhfbDtUpJuG5eTUDivIhAs_WSApIAfOcgJM6e24K_OuSTkL5GPGLtuF_r0p9XpClWC5sH88Q9eBPJS-sE2X8B3nyUrjsUuWX6K2w.OnxPzFWdp6HjGTolqdE8mA; clubFullJoinCookie=##eyJkZWxheSI6NywiZGF0ZSI6MTc1MzU2MzU3MzUxMiwidXNlciI6IjVvcHJ0MGJiZzNAZ21haWwuY29tIiwic3RhdHVzIjoiLTEiLCJjb3VudGVyIjowLCJtYXhDb3VudGVyIjoyfQ##; hm-turkey-cart=c7bb6669-3cc4-4da1-810d-9521ae991ef7; hm-turkey-favourites=\"\"; _scid_r=Ds2GcgEO1AXFxS7F-WrRWh1SQvIytfnttFLung; JSESSIONID=5DA3F20B8D78DE7C664F2E9A2D401813F2A13ACC5F220D12624C8F9AA62989D6EB9919AC774A6EABDE201DA5023562FB20E99CDEB00491A9F559423255C530E3.hybris-ecm-web-545d4f5885-n6pgl; _abck=212F8E14CC330BC3C05C0724BBFA1C98~0~YAAQO5hkXxEWExSYAQAAQK6gJA6cunL4cR0hWXEI4wu/HQKmXATt4G/Fcb7Odw/M8x95kc75hsUj6p8GQzFy+I1Ouf1AEfcgQnck1xoEqCV7ZFJgk/2mdcpL+mdsmYy/mS6v03T8Ee+sSOSzVBGUU/qxtVDnnGoN0ho9TzkWXhOo92R4HV3CBmYkHJvPNAYc1LFlc5wfrC+HhZFAFFAEf0eZW0A9qf6sUHiaMsoaTZREprmZ7EUffJyLpYjGpoSiIJVmjUOwA2F2nrPIL++46GGYz4ybd7O54FFm+T6+nPKvsMNbJxyw7XEprW/tleasZP6ostsIMRWvA1B2S2IXOO9zqnKPJkRprkCyvPAXSr6v+CO7APhmKNd18eAJFf8tFLgWUMCprJ6MbvWEg6qCIMTMAftFEB8b5sjN/SHH89vbFyoLDo7wCeaxppvaqORWP+7zqqcwZJbDs1VcDYCFAByVwA3ZHpIijilNUrzGl3vGtLCKH6j77tQMFTj6WRUxPSfmqzsBFbVrtbYo6WGlSR9KKesBSByKgdzxYPvJjn1/CLc50QALZ79jmagNHNey2t1MQKZzDjtrDYHd4J9hHUM4nfqa79by4uzMKDsu5b0V3IsCr1Pv/P2i1y3ebzamP6aIOEUROyeewQouW7c3iFbUmPzueeoSn55KIzhEr//lp6kTUgdzzzv8tPFHsDXZZf7p/n+qHmrPRXZ8UdezMUMAZfgn1aa2zCoxjez5xGgTtOJxvHcVgrhqCPCMbZvCLAWBs8gSNEv9Sl7ZEFLY~-1~-1~1752962174; userCookie=##eyJjYXJ0Q291bnQiOjB9##; bm_so=F11CB2A484373AA9006E38FE945B52ADEE636E58561F95764BD87547E075E951~YAAQO5hkXyAWExSYAQAAx7KgJATTW7Cq2WI5AdhJpqowaLEUkzMN9I5h1lJGwsIy35eNh3P18kmNBHfQL38ZUXu9SX7xqYCetm1RZsUxg/nQz8Fmu6GvIAsZefwBGA+nfEicrxYC4674pgeQU/XpeYz+AIC9r2O3M61Ap3m2+gfR8zOXTk0KeNyyBPwlHWk6LYzzgKwa2L+p47TdFYbWGBR/FLZt1BoESHGJIDdg+Hzd2KC09bd+TUFgeuGQc9DQEv0HGmAvPrvMBjOu0O8lrhXBVE5LOFRZINd0gz8R3TVsUwuAbp9dXKGU3bvmhEQxKFZ2W5u4BuCJIi6zw/2IEzIzroFG3H+RBKtcNYDzTvWB+YvTn89kXPdpGz3Cwj1CnBtWBEjnc8bn1qHIu9p+08Smj0OsQfiVgJ7XzwpjMICrZegZyAa3I46MXIVu2oCLMPGqLOeTe0rEdq4b",
  "origin": "https://www2.hm.com",
  "priority": "u=1, i",
  "referer": "https://www2.hm.com/tr_tr/register/newcustomer",
  "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
  "x-requested-with": "XMLHttpRequest"
}
        get = r.get("https://www2.hm.com/tr_tr/register/newcustomer", headers=headers, timeout=15)
        res = r.post("https://www2.hm.com/tr_tr/register/newcustomer", json=payload, headers=headers, timeout=15)
        print(res.text)
        if "/account?joinedClub=true" in res.text:
            print(f"✅ Başarılı: {email}:{password} - Proxy: {proxy_url}")
            save_account(email, password)
        else:
            print(f"❌ Kayıt başarısız: {email} - Proxy: {proxy_url} - Response snippet: {res.text[:200]}")
    except Exception as e:
        print(f"⚠️ Hata: {e} - Proxy: {proxy_url}")

def start_threads(thread_count=2):
    threads = []
    for i in range(thread_count):
        proxy = None
        if proxies_list:
            proxy = random.choice(proxies_list)
        t = threading.Thread(target=register, args=(proxy,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def loop_start_threads():
    while True:
        start_threads(2)
        time.sleep(random.uniform(1500, 2000))

loop_start_threads()
