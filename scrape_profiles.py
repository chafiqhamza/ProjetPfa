import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

def scrape_stackoverflow(user_ids, output_file='profiles.json'):
    """Scrape Stack Overflow user data and enrich profiles.json."""
    with open(output_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    for user_id in user_ids:
        url = f"https://api.stackexchange.com/2.3/users/{user_id}?site=stackoverflow"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                user_data = data['items'][0]
                for profile in profiles:
                    if profile['id'] == user_id:
                        profile['stackoverflow_reputation'] = user_data.get('reputation', 0)
                        profile['stackoverflow_tags'] = [tag['name'] for tag in user_data.get('top_tags', [])]
                        profile['stackoverflow_badges'] = user_data.get('badge_counts', {})
                        break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4)

def scrape_github_profiles(usernames, output_file='profiles.json'):
    """Scrape GitHub developer profiles and save to a JSON file."""
    profiles = []

    for username in usernames:
        url = f"https://github.com/{username}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract name
            name = soup.find('span', class_='p-name').text.strip() if soup.find('span', class_='p-name') else username

            # Extract bio
            bio = soup.find('div', class_='p-note').text.strip() if soup.find('div', class_='p-note') else ""

            # Extract repositories
            repositories = []
            repo_section = soup.find_all('a', itemprop='name codeRepository')
            for repo in repo_section:
                repo_name = repo.text.strip()
                repo_url = f"https://github.com{repo['href']}"
                repositories.append({"name": repo_name, "url": repo_url})

            # Extract contributions
            contributions = "0 contributions"
            contribution_section = soup.find('h2', class_='f4 text-normal mb-2')
            if contribution_section:
                contributions = contribution_section.text.strip()

            profile_data = {
                "id": username,
                "name": name,
                "bio": bio,
                "profile_url": url,
                "repositories": repositories,
                "contributions": contributions
            }
            profiles.append(profile_data)

            # Delay to avoid rate limits
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {username}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4)

def scrape_kaggle(usernames, output_file='profiles.json'):
    """Scrape Kaggle developer profiles and enrich profiles.json."""
    with open(output_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    for username in usernames:
        url = f"https://www.kaggle.com/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            # Simulate scraping Kaggle developer profile data
            kaggle_data = {
                "competitions": ["Competition 1", "Competition 2"],
                "notebooks": ["Notebook 1", "Notebook 2"],
                "datasets": ["Dataset 1", "Dataset 2"],
                "expertise": "Data Science, Machine Learning"
            }
            for profile in profiles:
                if profile['id'] == username:
                    profile['kaggle_competitions'] = kaggle_data.get('competitions', [])
                    profile['kaggle_notebooks'] = kaggle_data.get('notebooks', [])
                    profile['kaggle_datasets'] = kaggle_data.get('datasets', [])
                    profile['kaggle_expertise'] = kaggle_data.get('expertise', '')
                    break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4)

if __name__ == '__main__':
    stackoverflow_ids = ['22656', '23354']  # Example Stack Overflow user IDs
    github_usernames = [
        "weblate", "sxyazi", "jlowin", "amir1376", "zeux", "geelen", "brandur", "idosal",
        "sb2nov", "miurla", "RobinMalfait", "earlephilhower", "holtskinner", "steveluscher",
        "ezyang", "mxsm", "JarbasAl", "offa", "bdraco", "comfyanonymous", "dgtlmoon",
        "manusa", "sethvargo", "yetone", "jxom"
    ]

    scrape_stackoverflow(stackoverflow_ids)
    scrape_github_profiles(github_usernames)

    # Example Kaggle usernames
    kaggle_usernames = ['username1', 'username2']
    scrape_kaggle(kaggle_usernames)