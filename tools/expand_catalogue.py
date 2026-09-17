"""Maintain explicit model-series recognition, not generated imaginary model numbers.

These product strings are recognition examples, not device-output captures or
claims of hardware certification. Series share an OS collector only after live
identity confirms that OS. Re-running preserves broad fallback rules.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# vendor, role, official reference, explicit advertised product-series strings.
FAMILIES = [
    ('Cisco', 'switch', 'https://www.cisco.com/c/en/us/products/switches/index.html',
     'Catalyst 2960|Catalyst 2960-X|Catalyst 2960-XR|Catalyst 3560|Catalyst 3560-X|Catalyst 3650|Catalyst 3750|Catalyst 3750-X|Catalyst 3850|Catalyst 4500|Catalyst 4500-X|Catalyst 6500|Catalyst 6800|Catalyst 9200|Catalyst 9200L|Catalyst 9300|Catalyst 9300L|Catalyst 9300X|Catalyst 9400|Catalyst 9500|Catalyst 9500X|Catalyst 9600|Nexus 3000|Nexus 3100|Nexus 3500|Nexus 5000|Nexus 5500|Nexus 5600|Nexus 6000|Nexus 7000|Nexus 7700|Nexus 9000|Nexus 9200|Nexus 9300|Nexus 9500|CBS250|CBS350|SG300|SG350|SG500|IE 2000|IE 3000|IE 4000|IE 5000'),
    ('Aruba', 'switch', 'https://www.arubanetworks.com/products/switches/',
     '2530|2540|2610|2620|2810|2910al|2920|2930F|2930M|3500yl|3800|3810M|5400R|CX 6000|CX 6100|CX 6200|CX 6300|CX 6400|CX 8100|CX 8320|CX 8325|CX 8360|CX 8400|CX 10000|Instant On 1930|Instant On 1960'),
    ('Juniper', 'switch', 'https://www.juniper.net/us/en/products/switches.html',
     'EX2200|EX2300|EX3200|EX3300|EX3400|EX4100|EX4200|EX4300|EX4400|EX4500|EX4550|EX4600|EX4650|EX8200|EX9200|QFX3500|QFX3600|QFX5100|QFX5110|QFX5120|QFX5130|QFX5200|QFX5210|QFX5220|QFX5230|QFX5700|QFX10002|QFX10008|QFX10016'),
    ('Alcatel-Lucent Enterprise', 'switch', 'https://www.al-enterprise.com/en/products/switches',
     'OmniSwitch 6250|OmniSwitch 6350|OmniSwitch 6360|OmniSwitch 6450|OmniSwitch 6465|OmniSwitch 6560|OmniSwitch 6570M|OmniSwitch 6850|OmniSwitch 6855|OmniSwitch 6860|OmniSwitch 6865|OmniSwitch 6870|OmniSwitch 6900|OmniSwitch 9900'),
    ('Extreme', 'switch', 'https://www.extremenetworks.com/products/switches',
     'Summit X250|Summit X440|Summit X450|Summit X460|Summit X465|Summit X480|Summit X620|Summit X670|Summit X690|Summit X695|Switching 5320|Switching 5420|Switching 5520|Switching 5720|Switching 7520|Switching 7720|VSP 4450|VSP 4850|VSP 7200|VSP 7400|VSP 8200|VSP 8400|VSP 8600'),
    ('Ruckus', 'switch', 'https://www.ruckusnetworks.com/products/ethernet-switches/',
     'ICX 6430|ICX 6450|ICX 6610|ICX 6650|ICX 7150|ICX 7250|ICX 7450|ICX 7550|ICX 7650|ICX 7750|ICX 7850|ICX 8200'),
    ('Dell', 'switch', 'https://www.dell.com/en-us/dt/networking/index.htm',
     'PowerConnect 5500|PowerConnect 6200|PowerConnect 7000|PowerConnect 8100|Networking N1500|Networking N2000|Networking N3000|Networking N4000|PowerSwitch N2200|PowerSwitch N3200|PowerSwitch S3048|PowerSwitch S4048|PowerSwitch S4128|PowerSwitch S4148|PowerSwitch S5212|PowerSwitch S5224|PowerSwitch S5232|PowerSwitch S5248|PowerSwitch S5296|PowerSwitch S6000|PowerSwitch S6100|PowerSwitch Z9100|PowerSwitch Z9264|PowerSwitch Z9432'),
    ('HPE', 'switch', 'https://www.hpe.com/us/en/networking.html',
     'FlexNetwork 5130|FlexNetwork 5140|FlexNetwork 5510|FlexNetwork 5520|FlexNetwork 7500|FlexFabric 5700|FlexFabric 5710|FlexFabric 5900|FlexFabric 5930|FlexFabric 5940|FlexFabric 5945|FlexFabric 5950|FlexFabric 12900'),
    ('H3C', 'switch', 'https://www.h3c.com/en/Products_and_Solutions/InterConnect/Switches/',
     'S3100|S3600|S5120|S5130|S5500|S5510|S5560|S5800|S5820|S5850|S6520|S6800|S6850|S7500|S9500|S10500|S12500'),
    ('Huawei', 'switch', 'https://e.huawei.com/en/products/switches',
     'S2700|S3700|S5300|S5700|S5730|S5731|S5732|S5735|S5736|S6700|S6730|S7700|S9700|S12700|CloudEngine 5800|CloudEngine 6800|CloudEngine 8800|CloudEngine 9800|CloudEngine 12800'),
    ('Arista', 'switch', 'https://www.arista.com/en/products',
     'DCS-7010|DCS-7020|DCS-7050|DCS-7060|DCS-7130|DCS-7150|DCS-7160|DCS-7170|DCS-7280|DCS-7300|DCS-7368|DCS-7500|DCS-7800|CCS-710|CCS-720|CCS-722|CCS-750'),
    ('Fortinet', 'switch', 'https://www.fortinet.com/products/ethernet-switches',
     'FortiSwitch 108|FortiSwitch 124|FortiSwitch 148|FortiSwitch 224|FortiSwitch 248|FortiSwitch 424|FortiSwitch 448|FortiSwitch 524|FortiSwitch 548|FortiSwitch 1024|FortiSwitch 1048|FortiSwitch 3032'),
    ('NETGEAR', 'switch', 'https://www.netgear.com/business/wired/switches/',
     'M4100|M4200|M4250|M4300|M4350|M4500'),
    ('MikroTik', 'switch', 'https://mikrotik.com/products/group/switches',
     'CRS125|CRS212|CRS305|CRS309|CRS310|CRS312|CRS317|CRS326|CRS328|CRS354|CRS504|CRS518'),
    ('Allied Telesis', 'switch', 'https://www.alliedtelesis.com/us/en/products/switches',
     'x230|x330|x510|x530|x550|x600|x610|x930|x950|SwitchBlade x908|SwitchBlade x8100'),
    ('Palo Alto Networks', 'firewall', 'https://www.paloaltonetworks.com/network-security/next-generation-firewall',
     'PA-220|PA-410|PA-415|PA-440|PA-445|PA-450|PA-460|PA-820|PA-850|PA-1410|PA-1420|PA-3220|PA-3250|PA-3260|PA-3410|PA-3420|PA-3430|PA-3440|PA-5220|PA-5250|PA-5260|PA-5280|PA-5410|PA-5420|PA-5430|PA-5440|PA-5450|PA-7050|PA-7080|VM-Series'),
    ('Cisco', 'management', 'https://www.cisco.com/c/en/us/products/wireless/wireless-lan-controller/index.html',
     'Catalyst 9800-L|Catalyst 9800-CL|Catalyst 9800-40|Catalyst 9800-80|Wireless Controller 2504|Wireless Controller 3504|Wireless Controller 5508|Wireless Controller 5520|Wireless Controller 8540'),
    ('Ruckus', 'management', 'https://www.ruckusnetworks.com/products/network-control-and-management/',
     'SmartZone 100|SmartZone 144|SmartZone 300|Virtual SmartZone|ZoneDirector 1200|ZoneDirector 3000'),
    ('HPE', 'server', 'https://www.hpe.com/us/en/servers/proliant-dl-servers.html',
     'ProLiant DL20|ProLiant DL60|ProLiant DL80|ProLiant DL160|ProLiant DL180|ProLiant DL325|ProLiant DL345|ProLiant DL360|ProLiant DL380|ProLiant DL385|ProLiant DL560|ProLiant DL580|Synergy 480'),
    ('Dell', 'server', 'https://www.dell.com/en-us/shop/servers-storage-and-networking/sf/poweredge',
     'PowerEdge R240|PowerEdge R250|PowerEdge R350|PowerEdge R440|PowerEdge R450|PowerEdge R540|PowerEdge R550|PowerEdge R630|PowerEdge R640|PowerEdge R650|PowerEdge R660|PowerEdge R730|PowerEdge R740|PowerEdge R750|PowerEdge R760|PowerEdge R940|PowerEdge R950'),
    ('Lenovo', 'server', 'https://www.lenovo.com/us/en/servers-storage/servers/',
     'ThinkSystem SR250|ThinkSystem SR530|ThinkSystem SR550|ThinkSystem SR630|ThinkSystem SR650|ThinkSystem SR665|ThinkSystem SR670|ThinkSystem SR850|ThinkSystem SR950'),
    ('Cisco', 'server', 'https://www.cisco.com/c/en/us/products/servers-unified-computing/index.html',
     'UCS C220|UCS C240|UCS C480|UCS B200|UCS B480|UCS X210c|UCS X410c'),
    ('HPE', 'storage', 'https://www.hpe.com/us/en/storage.html',
     'MSA 1040|MSA 2040|MSA 2050|MSA 2052|MSA 2060|MSA 2062|Nimble Storage|Alletra 5000|Alletra 6000|Alletra 9000|3PAR StoreServ'),
    ('Dell', 'storage', 'https://www.dell.com/en-us/dt/storage.htm',
     'PowerVault ME4|PowerVault ME5|PowerVault MD3|PowerStore 500|PowerStore 1000|PowerStore 1200|PowerStore 3000|PowerStore 3200|Unity XT|PowerScale|EqualLogic PS'),
    ('NetApp', 'storage', 'https://www.netapp.com/data-storage/',
     'AFF A150|AFF A250|AFF A400|AFF A800|AFF A900|AFF C250|AFF C400|AFF C800|FAS2750|FAS2820|FAS8300|FAS8700|FAS9500|E2800|E5700'),
    ('QNAP', 'storage', 'https://www.qnap.com/en/product/',
     'TS-453|TS-464|TS-873|TS-1273|TS-1673|TS-2483|TS-h973|TS-h1277|TS-h1886|TS-h2490|TVS-h1288|TVS-h1688|QuTS hero|QTS'),
    ('Synology', 'storage', 'https://www.synology.com/en-us/products',
     'DiskStation|RackStation|FlashStation|SA3200|SA3400|SA3600|SA6400|HD6500'),
    ('APC', 'management', 'https://www.se.com/us/en/work/products/product-launch/local/apc/',
     'Smart-UPS|Symmetra|NetShelter Rack PDU|Network Management Card'),
    ('Eaton', 'management', 'https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution.html',
     '5PX|9PX|9SX|9PXM|93PM|Intelligent Rack PDU'),
    ('Vertiv', 'management', 'https://www.vertiv.com/en-us/products-catalog/',
     'Liebert GXT5|Liebert EXS|Liebert EXM|Liebert EXL|Geist Rack PDU'),
]


def model_rows():
    result = []
    for vendor, role, source, models in FAMILIES:
        for model in models.split('|'):
            # Specific models precede broader series. Require the manufacturer
            # and literal product together; arbitrary DNS labels are not input.
            product = re.escape(model).replace(r'\-', '-').replace(r'\ ', r'[ -]?')
            brand = {'Alcatel-Lucent Enterprise': r'(?:Alcatel[- ]Lucent(?: Enterprise)?|ALE)',
                     'HPE': r'(?:HPE|HP|Hewlett[- ]Packard)',
                     'Ruckus': r'(?:Ruckus|Brocade|Foundry)',
                     'Palo Alto Networks': r'Palo Alto(?: Networks)?'}.get(vendor, re.escape(vendor).replace(r'\-', '-').replace(r'\ ', '[ -]'))
            pattern = rf'\b{brand}\b[^\r\n]{{0,100}}\b{product}(?=$|[^a-z0-9]|[a-z][0-9a-z-]*\b)'
            result.append(dict(name=f'{vendor} {model}', kind=role.title(), deviceType='server' if role in {'storage', 'management'} else role,
                               pattern=pattern, examples=[f'{vendor} {model}'], source=source))
    return sorted(result, key=lambda row: -len(row['name']))


if __name__ == '__main__':
    path = ROOT / 'catalogues/infrastructureProducts.json'
    new = model_rows()
    names = {r['name'] for r in new}
    old = [r for r in json.loads(path.read_text()) if r['name'] not in names]
    path.write_text(json.dumps(new + old, indent=2) + '\n')
    print(f'{len(new)} explicit series; {len(new) + len(old)} total infrastructure rules.')
    # Service-specific roles supersede the original generic management labels.
    from expand_services import update
    update()
