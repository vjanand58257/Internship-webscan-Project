"""Simple IDOR testing by enumerating numeric IDs in a URL parameter."""
import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import copy

def enumerate_id_param(url, param_name, start=1, end=10):
    findings = []
    for i in range(start, end+1):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs[param_name] = [str(i)]
        new_q = urlencode(qs, doseq=True)
        new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_q, parsed.fragment))
        try:
            r = requests.get(new_url, timeout=6)
        except Exception:
            continue
        if r.status_code == 200:
            findings.append({'id': i, 'url': new_url, 'status': r.status_code})
    return findings

if __name__ == '__main__':
    print('IDOR helper functions. Use responsibly on test targets only.')
