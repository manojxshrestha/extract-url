# Automate R2 Bucket Hunt

This repository contains scripts to automate the process of hunting for **misconfigured Cloudflare R2 buckets** that have **R2.DEV enabled**. These misconfigured buckets can potentially expose sensitive data to unauthorized access. The goal of this repository is to provide a streamlined way of scanning these buckets and identifying vulnerabilities.

---

## Features

- **extracturl.py**: Extracts a list of Cloudflare R2 bucket URLs from a provided misconfiguration file.
- **automate-r2-hunt.py**: Automates the process of scanning the URLs for potential vulnerabilities, logging the results for each bucket.

---

## Output

- **r2_vulnerabilities.txt**: This file contains the results of the R2 bucket scan. It will show the status of each URL:
  - **EXPOSED**: The R2 bucket contains sensitive data.
  - **SAFE**: The R2 bucket appears to be secure.
  - **ERROR**: There was an issue accessing the URL.
