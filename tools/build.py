"""Validate or sign the public data bundle. Never requires customer/application access."""
from __future__ import annotations
import argparse
import base64
import json
import os
import time
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from support_pack_schema import validate

ROOT = Path(__file__).resolve().parents[1]


def assemble() -> dict:
    data = json.loads((ROOT / 'manifest.json').read_text())
    data.update(issuedAt=int(time.time()), expiresAt=int(time.time()) + 180 * 86400, profiles={})
    for path in sorted((ROOT / 'vendors').glob('*.json')):
        row = json.loads(path.read_text())
        key = row.pop('id')
        if key in data['profiles'] or path.stem != key:
            raise ValueError('Vendor filenames and IDs must be unique and match.')
        data['profiles'][key] = row
    for key in ('identity', 'infrastructureProducts', 'fixedEquipmentProducts'):
        data[key] = json.loads((ROOT / 'catalogues' / (key + '.json')).read_text())
    return validate(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sign', action='store_true')
    args = parser.parse_args()
    data = assemble()
    if args.sign:
        previous = json.loads(base64.b64decode(json.loads((ROOT / 'channel/stable.json').read_text())['payload']))
        if data['sequence'] <= previous['sequence'] or tuple(map(int, data['version'].split('.'))) <= tuple(map(int, previous['version'].split('.'))):
            raise ValueError('A release must increase both sequence and version.')
        key = serialization.load_pem_private_key(os.environ['SUPPORT_PACK_SIGNING_KEY'].encode(), password=None)
        if not isinstance(key, Ed25519PrivateKey):
            raise ValueError('Expected Ed25519 signing key.')
        public = base64.b64encode(key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode()
        if public != json.loads((ROOT / 'trust.json').read_text())['publicKey']:
            raise ValueError('Signing key does not match the desktop trust root.')
        raw = json.dumps(data, sort_keys=True, separators=(',', ':')).encode()
        envelope = {'payload': base64.b64encode(raw).decode(), 'signature': base64.b64encode(key.sign(raw)).decode()}
        (ROOT / 'dist').mkdir(exist_ok=True)
        (ROOT / 'dist/support-pack.json').write_text(json.dumps(envelope, indent=2) + '\n')
    print(f"Validated support {data['version']}: {len(data['profiles'])} collector families; synthetic fixtures passed.")


if __name__ == '__main__':
    main()
