import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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

def scrape_github(usernames, output_file='profiles.json'):
    driver = webdriver.Chrome()
    with open(output_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    for username in usernames:
        url = f"https://github.com/{username}?tab=repositories"
        driver.get(url)
        time.sleep(2)

        try:
            contributions = driver.find_element(By.CSS_SELECTOR, 'h2.f4.text-normal').text
        except:
            contributions = '0 contributions'

        for profile in profiles:
            if profile['id'] == username:
                profile['contributions'] = contributions
                break

    driver.quit()

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4)

def scrape_other_source(api_url, output_file='profiles.json'):
    """Scrape data from another open-source API and enrich profiles.json."""
    with open(output_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        for user_data in data.get('users', []):
            for profile in profiles:
                if profile['id'] == user_data.get('id'):
                    profile['other_source_expertise'] = user_data.get('expertise', '')
                    profile['other_source_projects'] = user_data.get('projects', [])
                    break

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
    github_usernames = ['weblate', 'sxyazi', 'jlowin']  # Example GitHub usernames

    scrape_stackoverflow(stackoverflow_ids)
    scrape_github(github_usernames)

    # Example API URL for another open-source platform
    other_source_api_url = 'https://api.example.com/users'
    scrape_other_source(other_source_api_url)

    # Example Kaggle usernames
    kaggle_usernames = ['username1', 'username2']
    scrape_kaggle(kaggle_usernames)