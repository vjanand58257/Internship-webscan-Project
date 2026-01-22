# DV-WebScanPro - Architecture Overview

This document describes the high-level architecture of the DV-WebScanPro starter scaffold.

- **Crawler**: discovers pages and forms and saves metadata
- **Test Modules**: sql_tester, xss_tester, auth_tester, idor_tester
- **Report Generator**: creates a basic HTML report using Jinja2
- **Main Runner**: ties the modules for a demo run against a local test target

Use Docker to run DVWA or Juice Shop locally for safe testing.
