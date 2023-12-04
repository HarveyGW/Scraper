import requests
from bs4 import BeautifulSoup
import csv
from colorama import init, Fore
import random
from datetime import datetime


init(autoreset=True)


def load_user_agents():
    with open("./user-agents.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]


def fetch_webpage(url, user_agents):
    while user_agents:
        user_agent = random.choice(user_agents)
        print(Fore.CYAN + f"Trying with user agent: {user_agent}")
        headers = {"User-Agent": user_agent}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            else:
                print(
                    Fore.YELLOW
                    + f"Failed with user agent: {user_agent}. Status code: {response.status_code}"
                )
        except requests.RequestException as e:
            print(Fore.RED + f"Request failed with error: {e}")

        user_agents.remove(user_agent)
        with open("./user-agents.txt", "w") as file:
            file.writelines(f"{ua}\n" for ua in user_agents)

    return None


user_agents = load_user_agents()


url = "https://corporation.org.uk/live-gigs/"
response = fetch_webpage(url, user_agents)

if not response:
    print(Fore.RED + "Failed to fetch webpage after several attempts. Exiting.")
    exit()


print(Fore.CYAN + "Parsing webpage content...")
soup = BeautifulSoup(response.content, "html.parser")


print(Fore.CYAN + "Extracting and manipulating gig data...")
gig_containers = soup.find_all("div", class_="decm-events-details")


def format_date(date_str):
    date_parts = date_str.split()
    if len(date_parts) >= 3:
        date_str = " ".join(date_parts[-3:])
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
            return parsed_date.strftime("%b %d %Y")
        except ValueError:
            return date_str
    else:
        return date_str


def format_time(time_str):
    return " - ".join(
        t.replace(":00 ", " ").upper().replace(" PM", "PM").replace(" AM", "AM")
        for t in time_str.split(" - ")
    ).replace("TIME", "")


gig_data = []
for gig in gig_containers:
    name = gig.find("h2").get_text(strip=True) if gig.find("h2") else None
    date_span = gig.find("span", class_="decm_date")
    date = format_date(date_span.get_text(strip=True)) if date_span else None
    time_span = gig.find("span", class_="ecs-eventTime")
    time = format_time(time_span.get_text(strip=True)) if time_span else None
    price_span = gig.find("span", class_="decm_price")
    price = price_span.get_text(strip=True).replace(".00", "") if price_span else None
    gig_data.append([name, date, time, price])

print(Fore.CYAN + "Writing data to CSV file...")
with open("gigs_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Date", "Time", "Price"])
    writer.writerows(gig_data)

print(Fore.GREEN + "Data extraction and CSV creation completed successfully.")
