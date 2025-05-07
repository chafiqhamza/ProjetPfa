import json

def load_profiles(file_path='profiles.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_profiles(profiles, file_path='profiles.json'):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=4)

def match_profiles(query, profiles):
    query_lower = query.lower()
    results = []
    for profile in profiles:
        # Combine all searchable fields into one string
        searchable_text = f"{profile.get('name', '')} {profile.get('bio', '')} {profile.get('profile_url', '')} {profile.get('featured_repo', '')}".lower()
        # Calculate a simple match score based on the presence of query words
        score = sum(1 for word in query_lower.split() if word in searchable_text)
        if score > 0:
            results.append({
                'id': profile.get('id', ''),
                'name': profile.get('name', ''),
                'score': score,
                'profile_url': profile.get('profile_url', ''),
                'featured_repo': profile.get('featured_repo', '')
            })
    # Sort results by score in descending order
    return sorted(results, key=lambda x: x['score'], reverse=True)

def add_profile(profile, file_path='profiles.json'):
    profiles = load_profiles(file_path)
    profiles.append(profile)
    save_profiles(profiles, file_path)

def delete_profile(profile_id, file_path='profiles.json'):
    profiles = load_profiles(file_path)
    profiles = [p for p in profiles if p.get('id') != profile_id]
    save_profiles(profiles, file_path)