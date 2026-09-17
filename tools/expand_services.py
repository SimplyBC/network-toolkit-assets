"""Explicit campus wireless and network-service recognition data.

This is an authoring helper, never downloaded or executed by the application.
These are product signatures, not new CLI/API drivers or firmware certifications.
Only endpoint product evidence is matched, not DNS guesses or RADIUS references.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Brand, meaningful inventory role, manufacturer documentation, known products.
FAMILIES = [
    ('Cisco', 'Wireless controller', 'https://www.cisco.com/c/en/us/support/wireless/catalyst-9800-series-wireless-controllers/series.html',
     'Catalyst 9800-L|Catalyst 9800-CL|Catalyst 9800-40|Catalyst 9800-80|Catalyst CW9800L|Catalyst CW9800M|Catalyst CW9800H1|Catalyst CW9800H2|Wireless Controller 2504|Wireless Controller 3504|Wireless Controller 5508|Wireless Controller 5520|Wireless Controller 5760|Wireless Controller 7510|Wireless Controller 8510|Wireless Controller 8540|Virtual Wireless Controller'),
    ('Ruckus', 'Wireless controller', 'https://www.ruckusnetworks.com/products/network-control-and-management/network-controllers/',
     'SmartZone 100|SmartZone 144|SmartZone 300|Virtual SmartZone|ZoneDirector 1100|ZoneDirector 1200|ZoneDirector 3000|ZoneDirector 5000'),
    ('Extreme', 'Wireless controller', 'https://www.extremenetworks.com/products/wi-fi-management/extremecloud-iq-controller/extremecloud-iq-controller',
     'ExtremeCloud IQ Controller|Campus Controller|IdentiFi Wireless|VX9000|NX5500|NX7500|NX9500'),
    ('Fortinet', 'Wireless controller', 'https://docs.fortinet.com/document/wireless-controller/8.5.4/fortiwlc-release-notes/252571/supported-hardware-and-software',
     'FortiWLC-50D|FortiWLC-200D|FortiWLC-500D|FortiWLC-1000D|FortiWLC-3000D|FWC-VM-50|FWC-VM-200|FWC-VM-500|FWC-VM-1000|FWC-VM-3000'),
    ('Huawei', 'Wireless controller', 'https://e.huawei.com/au/products/wlan',
     'AC6507S|AC6508|AC6800V|AC6805|AirEngine 9700-M|AirEngine 9700-M1|AirEngine 9700S-S|AirEngine 9703-S|AirEngine 9703-H'),
    ('H3C', 'Wireless controller', 'https://www.h3c.com/en/Support/Resource_Center/EN/Home/Wireless/00-Public/Configure___Deploy/Configuration_Guides/H3C_Access_Controllers_CG(R5456)/00/',
     'WX1804H|WX2508H|WX2510H|WX2540H|WX2560H|WX5540H|WX5560H|WX5580H'),
    ('TP-Link', 'Wireless controller', 'https://www.tp-link.com/us/business-networking/omada-controller/',
     'Omada OC200|Omada OC300|Omada Software Controller'),
    ('Cisco', 'Network access control appliance', 'https://www.cisco.com/c/en/us/products/collateral/security/identity-services-engine/secure-network-server-3700-series-ds.html',
     'SNS-3715|SNS-3755|SNS-3795'),
    ('Cisco', 'Network management', 'https://www.cisco.com/site/us/en/products/networking/cloud-networking-management/index.html',
     'Catalyst Center|DNA Center|Prime Infrastructure|Prime Network Registrar|Secure Access Control System'),
    ('Aruba', 'Network management', 'https://arubanetworking.hpe.com/techdocs/',
     'AirWave|Central On-Premises'),
    ('Extreme', 'Network management', 'https://www.extremenetworks.com/products/network-management/extremecloud-iq-site-engine',
     'ExtremeCloud IQ Site Engine|Management Center|ExtremeAnalytics|ExtremeControl'),
    ('Fortinet', 'Network management', 'https://docs.fortinet.com/',
     'FortiManager|FortiAnalyzer|FortiAuthenticator|FortiADC|FortiWeb|FortiDDoS|FortiMail'),
    ('BlueCat', 'DNS / DHCP / IPAM', 'https://bluecatnetworks.com/products/integrity/',
     'Address Manager|DNS/DHCP Server|Integrity|Gateway|Proteus|Adonis'),
    ('EfficientIP', 'DNS / DHCP / IPAM', 'https://efficientip.com/products/solidserver-ddi/',
     'SOLIDserver|DNS Guardian'),
    ('Men&Mice', 'DNS / DHCP / IPAM', 'https://bluecatnetworks.com/products/micetro/', 'Micetro'),
    ('BlueCat', 'DNS / DHCP / IPAM', 'https://bluecatnetworks.com/products/micetro/', 'Micetro'),
    ('Forescout', 'Network access control', 'https://www.forescout.com/products/', 'CounterACT|eyeSight|eyeControl'),
    ('Ivanti', 'Network access control', 'https://www.ivanti.com/products/connect-secure', 'Policy Secure|Connect Secure'),
    ('Pulse Secure', 'Network access control', 'https://www.ivanti.com/products/connect-secure', 'Policy Secure|Connect Secure'),
    ('F5', 'Load balancer', 'https://www.f5.com/products/big-ip', 'BIG-IP|BIG-IQ|VELOS|rSeries'),
    ('A10', 'Load balancer', 'https://www.a10networks.com/products/thunder-adc/', 'Thunder ADC|vThunder|Thunder TPS'),
    ('Citrix', 'Load balancer', 'https://docs.netscaler.com/', 'ADC|NetScaler'),
    ('Progress', 'Load balancer', 'https://kemptechnologies.com/load-balancer', 'Kemp LoadMaster'),
    ('Kemp', 'Load balancer', 'https://kemptechnologies.com/load-balancer', 'LoadMaster'),
    ('Radware', 'Load balancer', 'https://www.radware.com/products/alteon/', 'Alteon|DefensePro'),
    ('VMware', 'Load balancer', 'https://techdocs.broadcom.com/us/en/vmware-security-load-balancing/avi-load-balancer.html', 'NSX Advanced Load Balancer|Avi Load Balancer'),
    ('VMware', 'Network management', 'https://techdocs.broadcom.com/us/en/vmware-cis/nsx.html', 'NSX Manager|NSX Edge'),
    ('Check Point', 'Network management', 'https://sc1.checkpoint.com/documents/latest/', 'Multi-Domain Server|Security Management Server'),
    ('Opengear', 'Console server', 'https://opengear.com/products/', 'Operations Manager|Console Manager|Lighthouse'),
    ('Lantronix', 'Console server', 'https://www.lantronix.com/products-class/console-servers/', 'SLC 8000|LM-Series'),
    ('Vertiv', 'Console server', 'https://www.vertiv.com/en-us/products-catalog/monitoring-control-and-management/serial-consoles-and-gateways/', 'Avocent ACS'),
]

# Distinctive software identities also cover virtual deployments with no model SKU.
# No bare ISE/ACS/MM/AC, generic login title, OUI, hostname or arbitrary page body.
ALIASES = [
    ('Cisco ISE', 'Network access control', r'\bCisco\s+(?:Identity\s+Services\s+Engine|ISE)\b', ['Cisco Identity Services Engine', 'Cisco ISE'], 'https://www.cisco.com/c/en/us/support/security/identity-services-engine/series.html'),
    ('Cisco AireOS / Catalyst wireless controller', 'Wireless controller', r'\bCisco\s+(?:AireOS|Wireless(?:\s+LAN)?\s+Controller|Catalyst\s+(?:CW)?9800[\w-]*|(?:IOS[^\r\n]{0,100})?C9800(?:_IOSXE|-CL|-L|-40|-80)?\b)', ['Cisco AireOS', 'Cisco Wireless Controller', 'Cisco IOS Software C9800 Software'], 'https://www.cisco.com/c/en/us/products/wireless/wireless-lan-controller/index.html'),
    ('Ruckus SmartZone / ZoneDirector', 'Wireless controller', r'\b(?:Ruckus(?:\s+Wireless)?\s+)?(?:SmartZone|ZoneDirector|vSZ)[\w-]*\b', ['Ruckus SmartZone', 'ZoneDirector', 'vSZ'], 'https://www.ruckusnetworks.com/products/network-control-and-management/network-controllers/'),
    ('ExtremeCloud IQ Controller', 'Wireless controller', r'\bExtremeCloud\s+IQ\s+Controller\b', ['ExtremeCloud IQ Controller'], 'https://www.extremenetworks.com/products/wi-fi-management/extremecloud-iq-controller/extremecloud-iq-controller'),
    ('Fortinet FortiWLC', 'Wireless controller', r'\bFortiWLC(?:-[\w-]+)?\b', ['FortiWLC', 'FortiWLC-200D'], 'https://docs.fortinet.com/product/wireless-controller'),
    ('Ubiquiti UniFi Network Application', 'Wireless / network management', r'\b(?:Ubiquiti\s+)?UniFi\s+(?:Network(?:\s+(?:Application|Controller))?|Controller)\b', ['UniFi Network Application', 'UniFi Controller'], 'https://help.ui.com/hc/en-us/categories/6583256751383-UniFi-Network'),
    ('TP-Link Omada Controller', 'Wireless controller', r'\b(?:TP-Link\s+)?Omada\s+(?:(?:Software|Hardware|SDN)\s+)?Controller\b', ['Omada Software Controller', 'TP-Link Omada Controller'], 'https://www.tp-link.com/us/business-networking/omada-controller/'),
    ('Aruba AirWave', 'Network management', r'\b(?:Aruba\s+)?AirWave(?:\s+Management\s+Platform)?\b', ['Aruba AirWave', 'AirWave Management Platform'], 'https://arubanetworking.hpe.com/techdocs/AirWave/'),
    ('EfficientIP SOLIDserver', 'DNS / DHCP / IPAM', r'\b(?:EfficientIP\s+)?SOLIDserver\b', ['EfficientIP SOLIDserver', 'SOLIDserver'], 'https://efficientip.com/products/solidserver-ddi/'),
    ('PacketFence', 'Network access control', r'\bPacketFence\b', ['PacketFence'], 'https://www.packetfence.org/'),
    ('Portnox CORE', 'Network access control', r'\bPortnox\s+CORE\b', ['Portnox CORE'], 'https://docs.portnox.com/'),
    ('Fortinet FortiAuthenticator', 'Authentication service', r'\bFortiAuthenticator\b', ['FortiAuthenticator'], 'https://www.fortinet.com/products/identity-access-management/fortiauthenticator'),
    ('Fortinet FortiManager', 'Network management', r'\bFortiManager\b', ['FortiManager'], 'https://docs.fortinet.com/product/fortimanager'),
    ('Fortinet FortiAnalyzer', 'Network management', r'\bFortiAnalyzer\b', ['FortiAnalyzer'], 'https://docs.fortinet.com/product/fortianalyzer'),
    ('NetScaler ADC', 'Load balancer', r'\bNetScaler\s+(?:ADC|Gateway|VPX|MPX|SDX)\b', ['NetScaler ADC', 'NetScaler VPX'], 'https://docs.netscaler.com/'),
]


def service_rows():
    result = []
    for vendor, role, source, products in FAMILIES:
        # Python escapes '&'; JavaScript's Unicode regex mode rejects '\&'.
        brand = re.escape(vendor).replace(r'\ ', r'\s+').replace(r'\-', '-').replace(r'\&', '&')
        for product in products.split('|'):
            token = re.escape(product).replace(r'\ ', r'[ -]+').replace(r'\-', '-')
            result.append(dict(name=f'{vendor} {product}', kind=role, deviceType='server',
                               pattern=rf'\b{brand}\s+{token}(?![a-z0-9])',
                               examples=[f'{vendor} {product}'], source=source))
    # Exact named products override generic aliases with the same display name.
    names = {r['name'] for r in alias_rows()}
    result = [r for r in result if r['name'] not in names]
    return sorted(result, key=lambda r: -len(r['name'])) + alias_rows()


def alias_rows():
    return [dict(name=n, kind=k, deviceType='server', pattern=p, examples=e, source=s)
            for n, k, p, e, s in ALIASES]


def update():
    path = ROOT / 'catalogues/infrastructureProducts.json'
    rows = service_rows()
    names = {r['name'] for r in rows}
    old = [r for r in json.loads(path.read_text()) if r['name'] not in names]
    for row in old:
        if row['name'] == 'TP-Link Omada switch / router':
            row['pattern'] = row['pattern'].replace('Switch|Router|Controller', 'Switch|Router')
    path.write_text(json.dumps(rows + old, indent=2) + '\n')
    print(f'{len(rows)} wireless/service rules; {len(rows) + len(old)} infrastructure rules total.')


if __name__ == '__main__':
    update()
