import requests
import re

# Function to handle the URL scanning
def hunt_safe_buckets(urls):
    exposed_results = []
    for url in urls:
        try:
            print(f"[+] Hunting for exposed data on: {url}")
            response = requests.get(url, timeout=10)

            # Handle common status codes and log results accordingly
            status_code = response.status_code
            response_text = response.text[:300]  # Limit the content size logged
            
            # Check for misconfigurations and sensitive info in the page source
            if status_code == 200:
                # Check if we find sensitive files or exposed API keys in the HTML
                if re.search(r"(?:\.git|\.env|\.backup|API_KEY|SECRET_KEY)", response_text, re.IGNORECASE):
                    exposed_results.append(f"[+] EXPOSED: {url} - Status Code: {status_code}\n{response_text}\n")
                else:
                    exposed_results.append(f"[+] SAFE (No sensitive data found): {url} - Status Code: {status_code}\n")
            elif status_code == 301 or status_code == 302:
                exposed_results.append(f"[+] REDIRECT: {url} - Status Code: {status_code} -> {response.headers.get('Location')}")
            elif status_code == 403:
                exposed_results.append(f"[+] Forbidden Access: {url} - Status Code: {status_code}")
            elif status_code == 404:
                exposed_results.append(f"[+] Not Found: {url} - Status Code: {status_code}")
            elif status_code == 500:
                exposed_results.append(f"[+] Server Error: {url} - Status Code: {status_code}")
            else:
                exposed_results.append(f"[+] Unexpected Status: {url} - Status Code: {status_code}")
            
            # You can also look for additional subdomains or internal endpoints in the response text
            # Example regex to find URLs in the page
            found_urls = re.findall(r'https?://[^\s]+', response_text)
            if found_urls:
                exposed_results.append(f"[+] Found URLs within the response: {url} -> {', '.join(found_urls)}\n")

        except requests.exceptions.RequestException as e:
            exposed_results.append(f"[!] Error accessing {url}: {e}\n")

    return exposed_results

# Function to read URLs from the provided file
def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        # Clean up URLs (strip extra spaces, newlines)
        return [url.strip() for url in urls]
    except Exception as e:
        print(f"[!] Error reading URL file: {e}")
        return []

# Prompt user to select the file containing URLs
url_file_path = input("Enter the path to the URL file (e.g., urls.txt): ")

# Read URLs from the file
urls_to_check = read_urls_from_file(url_file_path)

# Ensure the URL list is not empty
if not urls_to_check:
    print("[!] No URLs to check. Exiting.")
else:
    # Run the function to hunt for safe buckets
    safe_buckets = hunt_safe_buckets(urls_to_check)

    # Output results to a file
    with open("safe_bucket_exposure_refined.txt", "w") as file:
        file.write("Hunting exposed data on Safe R2 Buckets\n" + "="*50 + "\n")
        for result in safe_buckets:
            file.write(result + "\n")

    print("[*] Safe Buckets hunting completed. Results are saved in 'safe_bucket_exposure_refined.txt'.")
