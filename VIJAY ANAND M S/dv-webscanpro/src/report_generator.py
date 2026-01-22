"""Generate a simple HTML report from findings (expects a dict/list)."""
import json, os, datetime, pathlib
from jinja2 import Template

TEMPLATE = '''<!doctype html>
<html><head><meta charset="utf-8"><title>DV-WebScanPro Report</title></head><body>
<h1>DV-WebScanPro Scan Report</h1>
<p>Generated: {{ generated }}</p>
<h2>Findings</h2>
{% for f in findings %}
  <div style="border:1px solid #ccc;padding:8px;margin:8px">
    <strong>{{ f.type }}</strong> - {{ f.endpoint }}<br/>
    Severity: {{ f.severity }}<br/>
    Details: <pre>{{ f.details }}</pre>
  </div>
{% else %}
  <p>No findings.</p>
{% endfor %}
</body></html>'''

def generate_report(findings, out_path=None):
    out_path = out_path or ('../reports/scan-%s.html'%datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'))
    tpl = Template(TEMPLATE)
    html = tpl.render(generated=datetime.datetime.utcnow().isoformat()+'Z', findings=findings)
    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')
    return str(p.resolve())

if __name__ == '__main__':
    print('Report generator module. Import generate_report and pass findings list.')
