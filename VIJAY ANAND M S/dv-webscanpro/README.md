# DV-WebScanPro - Starter Scaffold

This repository contains a starter scaffold for the DV-WebScanPro web application security testing project.
It includes basic crawler, SQL/XSS/IDOR/auth tester modules, a simple HTML report generator, and a demo runner.

## Quickstart
1. Create and activate a Python virtualenv (Python 3.10+ recommended).
2. Install dependencies: `pip install -r requirements.txt`
3. Run a vulnerable target locally (DVWA or Juice Shop recommended).
4. Run demo: `python src/main.py http://localhost:80/`

**IMPORTANT**: Only run tests against systems you own or are authorized to test (DVWA/Juice Shop are safe to use).
