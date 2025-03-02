import re
import os

# Regular expression to match URLs containing "domain name"
url_pattern = r"https?://[^\s]*verily[^\s]*"

def extract_urls(input_file, output_file="misconfurl.txt"):
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"[!] Error: '{input_file}' not found. Please check the file path.")
        return

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Find all matching URLs
        urls = re.findall(url_pattern, content)

        # Remove duplicates and sort
        unique_urls = sorted(set(urls))

        # Save the extracted URLs to the output file
        with open(output_file, "w", encoding="utf-8") as out_file:
            for url in unique_urls:
                out_file.write(url + "\n")

        print(f"[+] Extracted {len(unique_urls)} URLs containing 'verily'. Saved to '{output_file}'.")

    except Exception as e:
        print(f"[!] Error reading the file: {e}")

# Run the extraction with user input
if __name__ == "__main__":
    input_file = input("[+] Enter the path of the misconfigurations file: ").strip()
    extract_urls(input_file)
