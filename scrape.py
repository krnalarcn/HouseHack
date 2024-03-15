import re
import requests
from bs4 import BeautifulSoup

def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

def extract_org_name(url):
    # Remove "https://" or "http://"
    url = url.replace("https://", "").replace("http://", "")
    # Split the URL by "/"
    parts = url.split("/")
    # Get the first part, which is usually the domain name
    org_name = parts[0]
    # Remove any leading "www." if present
    org_name = org_name.replace("www.", "")
    return org_name

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = extract_emails(soup.get_text())
        org_name = extract_org_name(url)
        return org_name, emails
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, []

def write_to_file(org_emails_list, filename):
    with open(filename, 'w') as f:
        for org_name, emails in org_emails_list:
            f.write(f"Organization: {org_name}\n")
            f.write("Emails:\n")
            for email in emails:
                f.write(f"{email}\n")
            f.write("\n")

def main():
    websites = [
        "https://pcs.studentorg.berkeley.edu/",
        "https://advocate.studentorg.berkeley.edu/financial-aid/",
        "https://housingcomm.studentorg.berkeley.edu/",
        "https://calblueprint.org/",
        "https://defendthepark.org/connect",
        "https://berkeleyrealestateclub.com/",
        "https://www.ocf.berkeley.edu/~upsa/"
    ]

    org_emails_list = []

    for website in websites:
        org_name, emails = scrape_website(website)
        if org_name:
            org_emails_list.append((org_name, emails))

    output_file = "org_emails.txt"
    write_to_file(org_emails_list, output_file)
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
