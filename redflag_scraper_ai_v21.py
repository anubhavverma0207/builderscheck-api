import os
import json
import time
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

openai_key = input("🔐 OpenAI Key: ").strip()
serpapi_key = input("🔑 SerpAPI Key: ").strip()
query = input("🏗️ Name to search: ").strip()

client = OpenAI(api_key=openai_key)

red_flag_keywords = [
    "permanently closed", "in liquidation", "receivership", "complaint", "scam", "fraud",
    "winding up", "struck off", "abandoned", "director banned", "court case", "banned from trading",
    "asic.gov.au", "debtorinsight.co.nz", "appointment of receiver",
    "petition filed", "statutory demand", "insolvency proceedings"
]

high_risk_keywords = [
    "permanently closed", "in liquidation", "receivership", "winding up", "struck off",
    "appointment of receiver", "court case", "petition filed", "statutory demand", "insolvency proceedings",
    "scam", "fraud", "abandoned", "banned from trading", "director banned"
]

def search_google(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key,
        "num": 30,
        "gl": "nz",
        "hl": "en"
    }
    return GoogleSearch(params).get_dict()

def fetch_page_source(query):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html

def fetch_link_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=" ", strip=True).lower()
    except:
        return ""

def extract_pdf_text(url):
    if not url.endswith(".pdf"):
        return ""
    try:
        import fitz
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        with open("temp.pdf", "wb") as f:
            f.write(r.content)
        doc = fitz.open("temp.pdf")
        text = "\n".join([page.get_text() for page in doc])
        doc.close()
        os.remove("temp.pdf")
        return text.lower()
    except:
        return ""

def detect_red_flags(results):
    text_hits, link_hits, entity_flags = [], [], []
    for r in results:
        combined_text = f"{r['title']} {r['snippet']} {r['content_excerpt']} {r['pdf_text']}".lower()
        flagged_this = []
        for k in red_flag_keywords:
            if k in combined_text:
                text_hits.append(k)
                flagged_this.append(k)
                if r['link'] not in link_hits:
                    link_hits.append(r['link'])
        if flagged_this:
            entity_flags.append({
                "title": r['title'],
                "link": r['link'],
                "matched_keywords": flagged_this
            })
    return list(set(text_hits)), link_hits, entity_flags

def extract_serp_and_expand(serp_data):
    results = []
    for item in serp_data.get("organic_results", []):
        link = item.get("link", "")
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        content = fetch_link_content(link)
        pdf_text = extract_pdf_text(link)
        results.append({
            "title": title,
            "snippet": snippet,
            "link": link,
            "content_excerpt": content[:2000],
            "pdf_text": pdf_text[:3000]
        })
    return results

def summarize_critical_flags(entity_flags):
    summary = []
    for e in entity_flags:
        critical_flags = [k for k in e["matched_keywords"] if k in high_risk_keywords]
        if critical_flags:
            summary.append(f"• **{e['title']}** – {', '.join(sorted(set(critical_flags)))}")
    return summary

def ask_ai_summary(query, bullets):
    bullets_text = "\n".join(bullets) if bullets else "• No serious red flags found."
    explanation_prompt = f"""
You are helping evaluate risk for builder/company/director: {query}

The following red flags were found:

{bullets_text}

Now:
1. Summarize key red flags as bullet points (done).
2. Write a short risk assessment paragraph explaining the risk level (e.g., High, Medium, Low).
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": explanation_prompt}],
            temperature=0.3
        )
        return bullets_text + "\n\n" + response.choices[0].message.content.strip()
    except Exception as e:
        return bullets_text + "\n\n⚠️ AI summary failed: " + str(e)

def save_report(query, results, html_flags, redflags, flagged_links, entity_flags, ai_output):
    filename = f"redflag_report_{query.replace(' ', '_')}_v21.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "query": query,
            "search_results": results,
            "html_redflags": html_flags,
            "detected_redflags": redflags,
            "flagged_links": flagged_links,
            "entity_issues": entity_flags,
            "ai_summary": ai_output
        }, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved: {filename}")

# Main Execution
serp_data = search_google(query)
html = fetch_page_source(query)
html_flags = [k for k in red_flag_keywords if k in html.lower()]
expanded_results = extract_serp_and_expand(serp_data)
detected_flags, flagged_links, entity_flags = detect_red_flags(expanded_results)
bullet_flags = summarize_critical_flags(entity_flags)
ai_summary = ask_ai_summary(query, bullet_flags)
save_report(query, expanded_results, html_flags, detected_flags, flagged_links, entity_flags, ai_summary)
