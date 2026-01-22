"""Basic reflected XSS tester (string-reflection based)"""
import requests
XSS_PAYLOADS = ['<script>alert(1)</script>', '\" onmouseover=alert(1) \"']

def test_reflected(url, param, base_params=None, timeout=8):
    base = base_params or {}
    results = []
    for p in XSS_PAYLOADS:
        params = base.copy()
        params[param] = p
        try:
            r = requests.get(url, params=params, timeout=timeout)
        except Exception:
            continue
        if p in r.text:
            results.append({'payload': p, 'evidence': 'payload reflected in response'})
    return results

if __name__ == '__main__':
    print('XSS tester module. Import functions into main runner.')
