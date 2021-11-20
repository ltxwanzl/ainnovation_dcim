from django import forms

from utilities.forms import BootstrapMixin

OBJ_TYPE_CHOICES = (
    ('', 'All'),
    ('Circuits', (
        ('provider', '提供商'),
        ('circuit', '电路'),
    )),
    ('DCIM', (
        ('site', '站点'),
        ('rack', '机架'),
        ('rackreservation', '机架预占'),
        ('location', '区位'),
        ('devicetype', '设备类型'),
        ('device', '设备'),
        ('virtualchassis', '虚拟机箱'),
        ('cable', '电缆'),
        ('powerfeed', '供电'),
    )),
#     ('IPAM', (
#         ('vrf', 'VRFs'),
#         ('aggregate', 'Aggregates'),
#         ('prefix', 'Prefixes'),
#         ('ipaddress', 'IP Addresses'),
#         ('vlan', 'VLANs'),
#     )),
    ('Tenancy', (
        ('tenant', '租户'),
    )),
    ('Virtualization', (
        ('cluster', '集群'),
        ('virtualmachine', '虚拟机'),
    )),
)


def build_options():
    options = [{"label": OBJ_TYPE_CHOICES[0][1], "items": []}]

    for label, choices in OBJ_TYPE_CHOICES[1:]:
        items = []

        for value, choice_label in choices:
            items.append({"label": choice_label, "value": value})

        options.append({"label": label, "items": items})
    return options


class SearchForm(BootstrapMixin, forms.Form):
    q = forms.CharField(
        label='Search'
    )
    obj_type = forms.ChoiceField(
        choices=OBJ_TYPE_CHOICES, required=False, label='Type'
    )
    options = build_options()
