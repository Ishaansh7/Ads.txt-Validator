import streamlit as st
import pandas as pd
import requests

# ----------- 📄 App Config -----------
st.set_page_config(page_title="Ads.txt Validator", layout="wide")

# ----------- 🖼️ Logo -----------
LOGO_URL = "https://raw.githubusercontent.com/Ishaansh7/Ads.txt-Validator/refs/heads/main/vdoai-logo.png"
st.image(LOGO_URL, width=160)

# ----------- 🧾 Title -----------
st.title("ads.txt Validator")
st.markdown("Easily validate your ads.txt lines across multiple domains. Paste your inputs below 👇")

# ----------- 🔢 Input Fields -----------
st.subheader("🔹 Input")
col1, col2 = st.columns(2)

with col1:
    domains_input = st.text_area("Enter domains (one per line)", height=200)

with col2:
    ads_lines_input = st.text_area("Enter ads.txt lines to check", height=200)

# ----------- 🧠 Helper Functions -----------
def clean_line(line):
    return line.split('#')[0].strip()

def get_ads_txt(domain):
    try:
        url = f"http://{domain}/ads.txt"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return None

# ----------- ✅ Validation Logic -----------
if st.button("Validate"):
    domains = [d.strip() for d in domains_input.splitlines() if d.strip()]
    ads_lines = [clean_line(l) for l in ads_lines_input.splitlines() if clean_line(l)]

    results = []
    for domain in domains:
        ads_content = get_ads_txt(domain)
        if not ads_content:
            results.append({"Domain": domain, "Status": "❌ No ads.txt found", "Missing Lines": "All"})
            continue
        existing = [clean_line(l) for l in ads_content.splitlines() if clean_line(l)]
        missing = [l for l in ads_lines if l not in existing]
        results.append({
            "Domain": domain,
            "Status": "✅ All present" if not missing else f"⚠️ Missing {len(missing)} lines",
            "Missing Lines": "\n".join(missing) if missing else "None"
        })

    df = pd.DataFrame(results)
    st.subheader("📋 Validation Results")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "ads_txt_validation.csv", "text/csv")

# ----------- 📎 Footer -----------
st.markdown("---")
st.markdown("Built by **Ishaan Sharma** • Powered by [VDO.AI](https://vdo.ai)", unsafe_allow_html=True)
