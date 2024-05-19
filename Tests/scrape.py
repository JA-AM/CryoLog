import requests
import csv
from bs4 import BeautifulSoup

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }

def scrape_substance_by_letter(letter):
    url = f"https://www.webmd.com/vitamins/alpha/{letter}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        aside_container = soup.find("aside", style="display:contents;")

        vitamin_links = aside_container.find_all("a")

        vitamin_info = [(link.get("href"), link.text.strip()) for link in vitamin_links]

        for url, substance_name in vitamin_info:
            print(f"URL: {url}")
            print(f"Name: {substance_name}")
            data = scrape_info(url=url, substance_name=substance_name)
            write_to_csv(data)

    else:
        print("Failed to retrieve data from the website. Status code:", response.status_code)

def scrape_info(url, substance_name):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        overview = soup.find("div", class_="vitamins-monograph-content overview-content")
        side_effects = soup.find("div", class_="vitamins-monograph-content side-effects-content")
        precautions = soup.find("div", class_="vitamins-monograph-content precautions-content")
        dosing = soup.find("div", class_="vitamins-monograph-content dosage-content")

        # Check if any of the sections are None
        overview_text = overview.text.strip() if overview else ""
        side_effects_text = side_effects.text.strip() if side_effects else ""
        precautions_text = precautions.text.strip() if precautions else ""
        dosing_text = dosing.text.strip() if dosing else ""

        return {
            "Substance Name": substance_name,
            "URL": url,
            "Overview": overview_text,
            "Side Effects": side_effects_text,
            "Precautions": precautions_text,
            "Dosing": dosing_text
        }

    else:
        print("Failed to retrieve data from the website. Status code:", response.status_code)
        return None

def write_to_csv(data):
    with open("webmd_vitamins_supplements_data.csv", "a", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Substance Name', 'URL', 'Overview', 'Side Effects', 'Precautions', 'Dosing']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)
 
def main():
    for letter in "abcdefghijklmnopqrstuvwxyz":
        scrape_substance_by_letter(letter)

if __name__ == "__main__":
    main()