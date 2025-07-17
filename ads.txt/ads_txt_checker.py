import streamlit as st
import pandas as pd
import requests

# ----------- 🖼️ Add VDO.AI Logo -----------
LOGO_URL = "https://assets-global.website-files.com/5fa2f89762e5c64fd23c34f4/5fa2f89762e5c63e7a3c34f8_VDOAI%20Logo.svg"

st.set_page_config(page_title="Ads.txt Validator", layout="wide")

# ----------- 🎨 Theme Switch -----------
theme = st.selectbox("🎨 Choose Theme", ["Light", "Dark"], index=0)
if theme == "Dark":
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #0e1117;
            color: #FAFAFA;
        }
        </style>
    """, unsafe_allow_html=True)

# ----------- 📊 Page Layout -----------
st.image(LOGO_URL, width=150)
st.title("🧾 ads.txt Validator")
st.markdown("Validate ads.txt lines across multiple domains. Paste domains and ads.txt lines below and get instant results.")

# ----------- 📝 Input Section -----------
st.subheader("🔹 Input")
col1, col2 = st.columns(2)

with col1:
    domains_input = st.text_area("Enter domains (one per line)", height=200)

with col2:
    ads_lines_input = st.text_area("Enter ads.txt lines to check", height=200)

# ----------- 🧠 Logic -----------
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

# ----------- 🟢 Validate Button -----------
if st.button("✅ Validate"):
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
st.markdown("Built by VDO.AI • Validate smart, validate fast 💡")
