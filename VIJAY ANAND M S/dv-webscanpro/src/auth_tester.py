"""Authentication & session checks (cookie flags, simple default-cred check)"""
import requests

COMMON_DEFAULTS = [('admin','admin'),('admin','password'),('root','root')]

def check_cookie_flags(url):
    try:
        r = requests.get(url, timeout=8)
    except Exception:
        return {}
    cookies = r.headers.get('Set-Cookie','')
    flags = {'Secure': 'secure' in cookies.lower(), 'HttpOnly': 'httponly' in cookies.lower(), 'SameSite': 'samesite' in cookies.lower()}
    return flags

def check_default_credentials(login_url, user_field='username', pass_field='password', extra_fields=None):
    results = []
    for u,p in COMMON_DEFAULTS:
        data = {user_field: u, pass_field: p}
        if extra_fields:
            data.update(extra_fields)
        try:
            r = requests.post(login_url, data=data, timeout=8, allow_redirects=False)
        except Exception:
            continue
        # naive heuristic: 302 redirect on successful login
        if r.status_code in (301,302):
            results.append({'username':u,'password':p,'evidence':'redirect status code %s'%r.status_code})
    return results

if __name__ == '__main__':
    print('Auth tester module: cookie checks + default credential checks.')
