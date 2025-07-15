import requests
import pandas as pd

def get_ads_txt(domain):
    try:
        url = f"http://{domain}/ads.txt"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return None

def clean_line(line):
    return line.split('#')[0].strip()

def validate_ads_txt(domains, target_lines):
    target_lines = [clean_line(line) for line in target_lines if clean_line(line)]
    results = []

    for domain in domains:
        print(f"Checking {domain}...")
        ads_content = get_ads_txt(domain)

        if not ads_content:
            results.append({
                "Domain": domain,
                "Status": "No ads.txt found",
                "Missing Lines": "All"
            })
            continue

        existing_lines = [clean_line(line) for line in ads_content.splitlines() if clean_line(line)]
        missing = [line for line in target_lines if line not in existing_lines]

        status = "All present" if not missing else f"Missing {len(missing)} lines"
        results.append({
            "Domain": domain,
            "Status": status,
            "Missing Lines": "\n".join(missing) if missing else "None"
        })

    return pd.DataFrame(results)

def read_multiline_input(prompt):
    print(prompt + " (Press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line.strip())
    return lines

def main():
    print("=== ads.txt Validator (Manual Input Mode) ===\n")

    domains = read_multiline_input("Enter domains one per line")
    target_lines = read_multiline_input("Enter ads.txt lines to check")

    df = validate_ads_txt(domains, target_lines)

    # Display result in terminal
    print("\n📊 Validation Results:\n")
    print(df.to_string(index=False))  # Pretty print

    # Save to CSV
    output_file = input("\nEnter name for the output CSV file (e.g. report.csv): ").strip()
    df.to_csv(output_file, index=False)
    print(f"\n✅ CSV saved as: {output_file}")

if __name__ == "__main__":
    main()
