import argparse
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

import argparse
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

def check_open_redirect(url):
    original_url = url
    modified_url = url + '///;@inexistantdomain.com'
    print(f"Original URL: {original_url}, Modified URL: {modified_url}")
    try:
        response = requests.get(modified_url, allow_redirects=False, verify=False)
        if response.status_code == 302:  # Código de estado de redirección
            redirect_location = response.headers.get('Location')
            if redirect_location and 'inexistantdomain.com' in redirect_location:
                print(Fore.GREEN + f"Open redirect found: {original_url}" + Style.RESET_ALL)
            else:
                print(f"No open redirect found: {original_url}")
        else:
            print(f"No open redirect found: {original_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {original_url}, {e}")

def generate_open_redirects(file_path, num_threads):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            
            # Limpiar las URL de caracteres no deseados y verificar que no estén vacías
            urls = [url.strip() for url in urls if url.strip()]
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                executor.map(check_open_redirect, urls)
    except FileNotFoundError:
        print("El archivo especificado no se encontró.")

def main():
    parser = argparse.ArgumentParser(description="Script to generate open redirects from a list of URLs")
    parser.add_argument("-f", "--file", help="Path to the file containing URLs", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads to use (default: 5)", type=int, default=5)
    args = parser.parse_args()
    
    file_path = args.file
    num_threads = args.threads
    generate_open_redirects(file_path, num_threads)

if __name__ == "__main__":
    main()


