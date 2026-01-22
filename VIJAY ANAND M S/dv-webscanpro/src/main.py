"""Simple runner that ties crawler + basic tests into a demo flow."""
import json, pathlib
from crawler import crawl
from sql_tester import test_get_param
from xss_tester import test_reflected
from report_generator import generate_report

def run_demo(target):
    print('Crawling', target)
    t = crawl(target, max_depth=1)
    findings = []
    for page in t:
        for form in page.get('forms',[]):
            # naive: test first input for sql/xss if present
            if form.get('inputs'):
                param = form['inputs'][0]
                url = form['action'] or page['url']
                # SQL tests
                s = test_get_param(url, param)
                if s:
                    findings.append({'type':'SQL Injection','endpoint':url,'severity':'High','details':s})
                # XSS tests
                x = test_reflected(url, param)
                if x:
                    findings.append({'type':'XSS','endpoint':url,'severity':'Medium','details':x})
    report = generate_report(findings)
    print('Report generated:', report)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python main.py <target_url>')
    else:
        run_demo(sys.argv[1])
