"""Enhanced simple crawler to discover links and forms and save targets.json"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import sys
import os

def crawl(start_url, max_depth=2, same_domain_only=True):
    visited = set()
    to_visit = [(start_url, 0)]
    results = []
    

    base_domain = urlparse(start_url).netloc

    print(f"[+] Starting crawl from: {start_url} (max depth = {max_depth})")

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue

        visited.add(url)
        print(f"[*] Crawling ({depth}): {url}")

        try:
            r = requests.get(url, timeout=6)
            r.raise_for_status()
        except Exception as e:
            print(f"[!] Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(r.text, 'lxml')
        forms = []

        for f in soup.find_all('form'):
            inputs = [i.get('name') for i in f.find_all(['input', 'textarea', 'select']) if i.get('name')]
            forms.append({
                'action': urljoin(url, f.get('action', '')),
                'method': f.get('method', 'get').lower(),
                'inputs': inputs
            })

        results.append({'url': url, 'forms': forms})

        for a in soup.find_all('a', href=True):
            link = urljoin(url, a['href'])
            parsed = urlparse(link)
            if parsed.scheme.startswith('http'):
                if same_domain_only and parsed.netloc != base_domain:
                    continue
                if link not in visited:
                    to_visit.append((link, depth + 1))

    print(f"[+] Crawl finished. {len(results)} pages discovered.")
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[!] No URL provided, using default for testing...')
        sys.argv.append('https://example.com')
        sys.argv.append('2')

    url = sys.argv[1]
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    out = crawl(url, depth)

    os.makedirs('../data', exist_ok=True)
    out_path = '../data/targets.json'

    with open(out_path, 'w') as fh:
        json.dump(out, fh, indent=2)

    print(f"[+] Crawl complete. Targets saved to: {out_path}")
