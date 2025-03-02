import requests
import re
import os
import time

# Function to send request and check response for exposure
def check_r2_bucket(url):
    try:
        # Send HTTP request to the Cloudflare R2 Bucket URL
        response = requests.get(url)
        
        # Check if the response indicates a vulnerability (200 OK, exposed files)
        if response.status_code == 200:
            print(f"[+] Found accessible R2 Bucket: {url}")
            # Check for exposed data (you can adjust based on expected response)
            if "private" in response.text.lower():  # Adjust based on the expected content you are looking for
                print(f"[!] Private data found in: {url}")
                return f"EXPOSED: {url}\n"
            else:
                print(f"[+] No private data found in: {url}")
                return f"SAFE: {url}\n"
        else:
            print(f"[-] URL {url} returned {response.status_code}")
            return f"NO ACCESS: {url} - Status Code: {response.status_code}\n"
    except requests.exceptions.RequestException as e:
        # Handle any exception (timeout, DNS error, etc.)
        print(f"[!] Error accessing {url}: {e}")
        return f"ERROR: {url} - {e}\n"

# Main function to process URLs and check R2 bucket access
def automate_r2_hunting(input_file, output_file="r2_vulnerabilities.txt"):
    # Open the file containing URLs (already extracted URLs from previous step)
    with open(input_file, "r") as file:
        urls = file.readlines()

    # Open output file to store the results
    with open(output_file, "w") as result_file:
        for url in urls:
            url = url.strip()
            if url:  # Skip empty lines
                print(f"\n[+] Checking URL: {url}")
                result = check_r2_bucket(url)
                result_file.write(result)
                time.sleep(2)  # Sleep to avoid rate limits (adjust as needed)
    
    print(f"\n[+] Automation complete! Results saved to {output_file}")

if __name__ == "__main__":
    # Input the path to the file containing extracted URLs (you can manually set this)
    input_file = input("[+] Enter the path to the misconfiguration URL file: ").strip()
    
    if os.path.exists(input_file):
        automate_r2_hunting(input_file)
    else:
        print(f"[!] File not found: {input_file}. Please make sure the file path is correct.")
