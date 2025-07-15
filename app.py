import streamlit as st
import pandas as pd
import requests

def get_ads_txt(domain):
    try:
        url = f"http://{domain}/ads.txt"
        response = requests.get(url, timeout=10)
        return response.text
    except:
        return None

def clean_line(line):
    return line.split('#')[0].strip()

st.title("ads.txt Validator")

domains = st.text_area("Enter domains (one per line)")
lines = st.text_area("Enter ads.txt lines to check (one per line)")

if st.button("Validate"):
    domains_list = [d.strip() for d in domains.splitlines() if d.strip()]
    lines_list = [clean_line(l) for l in lines.splitlines() if clean_line(l)]

    results = []
    for domain in domains_list:
        content = get_ads_txt(domain)
        if not content:
            results.append({"Domain": domain, "Status": "No ads.txt found", "Missing Lines": "All"})
            continue
        existing = [clean_line(l) for l in content.splitlines() if clean_line(l)]
        missing = [l for l in lines_list if l not in existing]
        results.append({
            "Domain": domain,
            "Status": "All present" if not missing else f"Missing {len(missing)} lines",
            "Missing Lines": "\n".join(missing) if missing else "None"
        })

    df = pd.DataFrame(results)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "ads_txt_validation.csv", "text/csv")
