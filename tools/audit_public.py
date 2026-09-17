"""Fail closed on accidental private files/content. Not a substitute for human review."""
import base64
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
allowed_roots = {'catalogues', 'vendors', 'tools', 'tests', 'docs', '.github', 'channel'}
allowed_files = {'README.md', 'SECURITY.md', 'CONTRIBUTING.md', 'CHANGELOG.md', 'manifest.json', 'trust.json', 'requirements.txt', '.gitignore'}
checks = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'\bgh[pousr]_[A-Za-z0-9]{25,}', r'\bops_[A-Za-z0-9_-]{20,}', r'\bNTK1-(?:[A-Z0-9]{4}-){6}[A-Z0-9]{4}', r'/Users/[^/]+/', r'(?i)(?:khipu-networks\.com|172\.20\.0\.|172\.21\.14\.|192\.168\.50\.)']
failures = []
for file in ROOT.rglob('*'):
    relative = file.relative_to(ROOT)
    if relative.parts[0] in {'.git', '.venv', 'dist'} or '__pycache__' in relative.parts or not file.is_file():
        continue
    if relative.parts[0] not in allowed_roots and str(relative) not in allowed_files:
        failures.append(str(relative)); continue
    if file.suffix in {'.pem', '.key', '.sqlite', '.db', '.log', '.png'}:
        failures.append(str(relative)); continue
    content = file.read_text()
    if relative.parts[0] == "channel":
        content += base64.b64decode(json.loads(content)["payload"], validate=True).decode()
    if file.name == 'audit_public.py':
        continue
    if any(re.search(pattern, content) for pattern in checks):
        failures.append(str(relative))
if failures:
    raise SystemExit('Public content review failed for: ' + ', '.join(failures))
print('Public-file allowlist and sensitive-content checks passed.')
