import argparse
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
import os
import random
import re

def search_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            matches = re.findall(r'(AIza[0-9A-Za-z-_]{35})', content)
            return matches
            for match in list(set(matches)):
                print(match)
    except Exception as e:
        return []

def browse_files(folder):
    matches = []
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            matches.extend(search_in_file(file_path))
    return list(set(matches))

def test_api_key(key):
    try:
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        geolocator = GoogleV3(api_key=key)
        locations = geolocator.reverse(f"{latitude}, {longitude}")
        return True
    except GeocoderQueryError as e:
        return False 
    except Exception as e:
        return False 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='APK file to decompile')
    args = parser.parse_args()
    path = args.file
    file = path.replace('..', '').replace('/', '')
    if os.path.isfile(path) and path.lower().endswith('.apk'):
        print(f'Decompiling {file}...')
        os.system(f'apktool d {path} -o ./tmp > /dev/null')
        
        print('Looking for API KEYS...')
        api_keys = browse_files('./tmp')
        
        print('Cleaning space...')
        os.system('rm -rf ./tmp')

        print(f'\nAPI KEYS found: {len(api_keys)}\n')
        
        if len(api_keys) > 0:
            print('Testing API KEYS...\n')
            api_keys = [(key, test_api_key(key)) for key in api_keys]
            valid_api_keys = [key for key in api_keys if key[1]]
            invalid_api_keys = [key for key in api_keys if not key[1]]

            if len(valid_api_keys) > 0:
                print(f'Valid API KEYS ({len(valid_api_keys)}):')
                for key, _ in valid_api_keys:
                    print(f'- {key}')
        
            if len(invalid_api_keys) > 0:
                print(f'\nInvalid API KEYS ({len(invalid_api_keys)}):')
                for key, _ in invalid_api_keys:
                    print(f'- {key}')
            print()
    else:
        print(f'{file} is not an .apk file')
