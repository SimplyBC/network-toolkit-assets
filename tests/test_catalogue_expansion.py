"""Public synthetic recognition tests; no live addresses or customer captures."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import assemble
from expand_catalogue import model_rows
from support_pack_schema import matches, validate


class ExpansionTest(unittest.TestCase):
    def test_catalogue_contains_explicit_unique_series_with_sources(self):
        rows = assemble()['infrastructureProducts']
        self.assertGreaterEqual(len(model_rows()), 300)
        self.assertEqual(len({r['name'] for r in rows}), len(rows))
        for row in rows:
            self.assertTrue(row['examples'], row['name'])
            self.assertTrue(row['source'].startswith('https://'))
            for example in row['examples']:
                self.assertTrue(matches(row['pattern'], example), row['name'])

    def test_vendor_mac_generic_cert_and_endpoint_names_are_not_products(self):
        rows = assemble()['infrastructureProducts']
        for text in ['VMware', 'Proxmox', 'Cisco', 'HP', 'Aruba', 'securelogin.arubanetworks.com',
                     '02:00:00:00:00:01', 'example-laptop', 'example-phone', 'nginx',
                     'Microsoft Windows 11', 'Linux 6.8', 'Cisco Catalyst 999999',
                     'Dell PowerEdge R999999', 'NETGEAR M43000']:
            self.assertFalse(any(matches(row['pattern'], text) for row in rows), text)

    def test_specific_models_precede_broad_fallbacks(self):
        rows = assemble()['infrastructureProducts']
        for text, expected in [('Dell PowerEdge R750', 'Dell PowerEdge R750'),
                               ('Arista DCS-7050SX3-48YC8', 'Arista DCS-7050'),
                               ('Ruckus ICX7150-48P', 'Ruckus ICX 7150'),
                               ('Cisco Catalyst 9300L', 'Cisco Catalyst 9300L'),
                               ('Aruba 2930M-40G-8SR-PoE', 'Aruba 2930M')]:
            self.assertEqual(next(row['name'] for row in rows if matches(row['pattern'], text)), expected)

    def test_engine_one_signed_channel_is_still_valid(self):
        import base64
        channel = json.loads((ROOT / 'channel/stable.json').read_text())
        self.assertEqual(validate(json.loads(base64.b64decode(channel['payload'])))['engine'], 1)

    def test_new_families_have_read_plans_and_synthetic_command_outputs(self):
        data = assemble()
        fixtures = json.loads((ROOT / 'tests/fixtures/expanded_switches.json').read_text())
        self.assertEqual(set(fixtures), {'arista_eos', 'ruckus_fastiron', 'hp_comware', 'huawei_vrp'})
        for platform, outputs in fixtures.items():
            self.assertEqual(set(data['profiles'][platform]['sections']), {'identity','interfaces','vlans','lldp','fdb','arp'})
            for section, commands in data['profiles'][platform]['sections'].items():
                self.assertTrue(outputs[section])
                self.assertTrue(all(c.startswith(('show ', 'display ')) for c in commands))


if __name__ == '__main__':
    unittest.main()
