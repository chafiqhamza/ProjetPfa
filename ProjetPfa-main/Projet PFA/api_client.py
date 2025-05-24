import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_match():
    payload = {
        'title': 'Python Developer',
        'description': 'Experience with Flask and APIs'
    }
    response = requests.post(f'{BASE_URL}/match', json=payload)
    print('Match Response:', response.json())

def test_add_profile():
    payload = {
        'id': 'new_dev',
        'name': 'New Developer',
        'bio': 'Expert in Python and Flask',
        'profile_url': 'https://github.com/new_dev',
        'featured_repo': 'https://github.com/new_dev/cool_project'
    }
    response = requests.post(f'{BASE_URL}/profiles', json=payload)
    print('Add Profile Response:', response.json())

def test_delete_profile():
    payload = {'id': 'new_dev'}
    response = requests.delete(f'{BASE_URL}/profiles', json=payload)
    print('Delete Profile Response:', response.json())

def test_chat():
    payload = {'message': 'What is Python?'}
    response = requests.post(f'{BASE_URL}/chat', json=payload)
    print('Chat Response:', response.json())

if __name__ == '__main__':
    test_match()
    test_add_profile()
    test_delete_profile()
    test_chat()