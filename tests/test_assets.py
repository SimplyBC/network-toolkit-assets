"""Synthetic authoring contract tests; no real device captures or credentials."""
import base64
import copy
import json
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import assemble
from support_pack_schema import command, normalize, profile_for, validate


class AssetsTest(unittest.TestCase):
    def test_all_vendor_definitions_and_recognition_examples(self):
        data = assemble()
        self.assertEqual(len(data['profiles']), 11)
        for name, row in data['profiles'].items():
            if name != 'paloalto_panos':
                self.assertEqual(row['sectionOrder'][0], 'identity')

    def test_channel_signature(self):
        signed = json.loads((ROOT / 'channel/stable.json').read_text())
        raw = base64.b64decode(signed['payload'], validate=True)
        public = base64.b64decode(json.loads((ROOT / 'trust.json').read_text())['publicKey'], validate=True)
        Ed25519PublicKey.from_public_bytes(public).verify(base64.b64decode(signed['signature'], validate=True), raw)
        validate(json.loads(raw))

    def test_rejects_unsafe_commands(self):
        for value in ('reload', 'configure terminal', 'show version; reboot', 'show version | save x', 'show $(id)'):
            with self.assertRaises(ValueError):
                command(value)

    def test_synthetic_output_adapter_and_variant(self):
        data = copy.deepcopy(assemble())
        data['profiles']['cisco_ios']['transforms'] = [{
            'section': 'identity', 'containsAll': ['ExampleOS'],
            'pattern': r'(?m)^System name = (?P<name>[a-z0-9-]+)$',
            'replacement': r'hostname: \g<name>', 'maxMatches': 1,
            'fixtures': [{'input': 'System name = example-switch', 'expected': 'hostname: example-switch'}],
        }]
        validate(data)
        profile = profile_for(data, 'cisco_ios', 'ExampleOS')
        self.assertEqual(normalize(profile, 'identity', 'ExampleOS', 'System name = example-switch'), 'hostname: example-switch')


if __name__ == '__main__':
    unittest.main()
