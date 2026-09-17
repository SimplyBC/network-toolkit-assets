"""Synthetic product evidence, not customer captures or device certification."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build import assemble
from expand_services import service_rows
from support_pack_schema import matches


class WirelessServicesTest(unittest.TestCase):
    def test_all_service_examples_are_recognized_without_command_drivers(self):
        rows = assemble()['infrastructureProducts']
        for service in service_rows():
            row = next(r for r in rows if r['name'] == service['name'])
            self.assertEqual(row['deviceType'], 'server')
            self.assertNotIn('commands', row)
            for example in service['examples']:
                self.assertTrue(matches(row['pattern'], example), example)

    def test_roles_are_specific_and_common_university_products_are_present(self):
        rows = assemble()['infrastructureProducts']
        for example, role in [
            ('Cisco Identity Services Engine 3.3', 'Network access control'),
            ('Cisco Catalyst 9800-CL', 'Wireless controller'),
            ('Ruckus Virtual SmartZone', 'Wireless controller'),
            ('ExtremeCloud IQ Controller', 'Wireless controller'),
            ('Huawei AC6508', 'Wireless controller'),
            ('H3C WX5560H', 'Wireless controller'),
            ('FortiWLC-200D', 'Wireless controller'),
            ('TP-Link Omada Controller', 'Wireless controller'),
            ('EfficientIP SOLIDserver', 'DNS / DHCP / IPAM'),
            ('Forescout CounterACT', 'Network access control'),
            ('Kemp LoadMaster', 'Load balancer'),
            ('Opengear Lighthouse', 'Console server'),
        ]:
            found = next((r for r in rows if matches(r['pattern'], example)), None)
            self.assertIsNotNone(found, example)
            self.assertEqual(found['kind'], role, example)

    def test_no_service_product_from_vendor_names_acronyms_or_ap_models(self):
        for text in ['Cisco', 'ISE', 'ACS', 'MM', 'AC', 'Ruckus', 'Fortinet', 'BlueCat',
                     'VMware', 'Login', 'RADIUS server', 'DHCP server', 'nginx',
                     'Cisco Aironet 3802', 'Cisco Catalyst 9120AX', 'TP-Link Omada EAP650',
                     'Ruckus R750', 'FortiAP 231F', 'Huawei AirEngine 5761',
                     'Cisco SNS-37950', 'Huawei AC65080', 'H3C WX5560H9']:
            self.assertFalse(any(matches(r['pattern'], text) for r in service_rows()), text)


if __name__ == '__main__':
    unittest.main()
