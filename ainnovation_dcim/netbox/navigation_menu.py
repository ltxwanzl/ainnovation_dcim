from dataclasses import dataclass
from typing import Sequence, Optional

from extras.registry import registry
from utilities.choices import ButtonColorChoices


#
# Nav menu data classes
#

@dataclass
class MenuItemButton:

    link: str
    title: str
    icon_class: str
    permissions: Optional[Sequence[str]] = ()
    color: Optional[str] = None


@dataclass
class MenuItem:

    link: str
    link_text: str
    permissions: Optional[Sequence[str]] = ()
    buttons: Optional[Sequence[MenuItemButton]] = ()


@dataclass
class MenuGroup:

    label: str
    items: Sequence[MenuItem]


@dataclass
class Menu:

    label: str
    icon_class: str
    groups: Sequence[MenuGroup]


#
# Utility functions
#

def get_model_item(app_label, model_name, label, actions=('add', 'import')):
    return MenuItem(
        link=f'{app_label}:{model_name}_list',
        link_text=label,
        permissions=[f'{app_label}.view_{model_name}'],
        buttons=get_model_buttons(app_label, model_name, actions)
    )


def get_model_buttons(app_label, model_name, actions=('add', 'import')):
    buttons = []

    if 'add' in actions:
        buttons.append(
            MenuItemButton(
                link=f'{app_label}:{model_name}_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=[f'{app_label}.add_{model_name}'],
                color=ButtonColorChoices.GREEN
            )
        )
    if 'import' in actions:
        buttons.append(
            MenuItemButton(
                link=f'{app_label}:{model_name}_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=[f'{app_label}.add_{model_name}'],
                color=ButtonColorChoices.CYAN
            )
        )

    return buttons


#
# Nav menus
#

ORGANIZATION_MENU = Menu(
    label='组织',
    icon_class='mdi mdi-domain',
    groups=(
        MenuGroup(
            label='站点',
            items=(
                get_model_item('dcim', 'site', '站点'),
                get_model_item('dcim', 'region', '地区'),
                get_model_item('dcim', 'sitegroup', '站点组'),
                get_model_item('dcim', 'location', '区位'),
            ),
        ),
        MenuGroup(
            label='机架',
            items=(
                get_model_item('dcim', 'rack', '机架'),
                get_model_item('dcim', 'rackrole', '机架角色'),
                get_model_item('dcim', 'rackreservation', '预占'),
                MenuItem(
                    link='dcim:rack_elevation_list',
                    link_text='立视图',
                    permissions=['dcim.view_rack']
                ),
            ),
        ),
        MenuGroup(
            label='租户',
            items=(
                get_model_item('tenancy', 'tenant', '租户'),
                get_model_item('tenancy', 'tenantgroup', '租户组'),
            ),
        ),
    ),
)

DEVICES_MENU = Menu(
    label='设备',
    icon_class='mdi mdi-server',
    groups=(
        MenuGroup(
            label='设备',
            items=(
                get_model_item('dcim', 'device', '设备'),
                get_model_item('dcim', 'devicerole', '设备角色'),
                get_model_item('dcim', 'platform', '平台'),
                """ get_model_item('dcim', 'virtualchassis', 'Virtual Chassis'), """
            ),
        ),
        MenuGroup(
            label='设备类型',
            items=(
                get_model_item('dcim', 'devicetype', '设备类型'),
                get_model_item('dcim', 'manufacturer', '制造商'),
            ),
        ),
        MenuGroup(
            label='设备组件',
            items=(
                get_model_item('dcim', 'interface', '接口', actions=['import']),
                get_model_item('dcim', 'frontport', '前端口', actions=['import']),
                get_model_item('dcim', 'rearport', '后端口', actions=['import']),
                get_model_item('dcim', 'consoleport', '控制台端口', actions=['import']),
                get_model_item('dcim', 'consoleserverport', '控制台服务端口', actions=['import']),
                get_model_item('dcim', 'powerport', '电源端口', actions=['import']),
                get_model_item('dcim', 'poweroutlet', '电源插座', actions=['import']),
                get_model_item('dcim', 'devicebay', '设备托台', actions=['import']),
                get_model_item('dcim', 'inventoryitem', '库存项', actions=['import']),
            ),
        ),
    ),
)

CONNECTIONS_MENU = Menu(
    label='连接',
    icon_class='mdi mdi-ethernet',
    groups=(
        MenuGroup(
            label='连接',
            items=(
                get_model_item('dcim', 'cable', '电缆', actions=['import']),
                MenuItem(
                    link='dcim:interface_connections_list',
                    link_text='接口连接',
                    permissions=['dcim.view_interface']
                ),
                MenuItem(
                    link='dcim:console_connections_list',
                    link_text='控制台连接',
                    permissions=['dcim.view_consoleport']
                ),
                MenuItem(
                    link='dcim:power_connections_list',
                    link_text='电源连接',
                    permissions=['dcim.view_powerport']
                ),
            ),
        ),
    ),
)

IPAM_MENU = Menu(
    label='IPAM',
    icon_class='mdi mdi-counter',
    groups=(
        MenuGroup(
            label='IP Addresses',
            items=(
                get_model_item('ipam', 'ipaddress', 'IP Addresses'),
                get_model_item('ipam', 'iprange', 'IP Ranges'),
            ),
        ),
        MenuGroup(
            label='Prefixes',
            items=(
                get_model_item('ipam', 'prefix', 'Prefixes'),
                get_model_item('ipam', 'role', 'Prefix & VLAN Roles'),
            ),
        ),
        MenuGroup(
            label='Aggregates',
            items=(
                get_model_item('ipam', 'aggregate', 'Aggregates'),
                get_model_item('ipam', 'rir', 'RIRs'),
            ),
        ),
        MenuGroup(
            label='VRFs',
            items=(
                get_model_item('ipam', 'vrf', 'VRFs'),
                get_model_item('ipam', 'routetarget', 'Route Targets'),
            ),
        ),
        MenuGroup(
            label='VLANs',
            items=(
                get_model_item('ipam', 'vlan', 'VLANs'),
                get_model_item('ipam', 'vlangroup', 'VLAN Groups'),
            ),
        ),
        MenuGroup(
            label='Services',
            items=(
                get_model_item('ipam', 'service', 'Services', actions=['import']),
            ),
        ),
    ),
)

VIRTUALIZATION_MENU = Menu(
    label='虚拟机',
    icon_class='mdi mdi-monitor',
    groups=(
        MenuGroup(
            label='虚拟机',
            items=(
                get_model_item('virtualization', 'virtualmachine', '虚拟机'),
                get_model_item('virtualization', 'vminterface', '接口', actions=['import']),
            ),
        ),
        MenuGroup(
            label='集群',
            items=(
                get_model_item('virtualization', 'cluster', '集群'),
                get_model_item('virtualization', 'clustertype', '集群类型'),
                get_model_item('virtualization', 'clustergroup', '集群组'),
            ),
        ),
    ),
)

CIRCUITS_MENU = Menu(
    label='电路',
    icon_class='mdi mdi-transit-connection-variant',
    groups=(
        MenuGroup(
            label='电路',
            items=(
                get_model_item('circuits', 'circuit', '电路'),
                get_model_item('circuits', 'circuittype', '电路类型'),
            ),
        ),
        MenuGroup(
            label='供电商',
            items=(
                get_model_item('circuits', 'provider', '供电商'),
                get_model_item('circuits', 'providernetwork', '供电网络'),
            ),
        ),
    ),
)

POWER_MENU = Menu(
    label='电源',
    icon_class='mdi mdi-flash',
    groups=(
        MenuGroup(
            label='电源',
            items=(
                get_model_item('dcim', 'powerfeed', '电源'),
                get_model_item('dcim', 'powerpanel', '电源面板'),
            ),
        ),
    ),
)

OTHER_MENU = Menu(
    label='Other',
    icon_class='mdi mdi-notification-clear-all',
    groups=(
        MenuGroup(
            label='Logging',
            items=(
                get_model_item('extras', 'journalentry', 'Journal Entries', actions=[]),
                get_model_item('extras', 'objectchange', 'Change Log', actions=[]),
            ),
        ),
        MenuGroup(
            label='Customization',
            items=(
                get_model_item('extras', 'customfield', 'Custom Fields'),
                get_model_item('extras', 'customlink', 'Custom Links'),
                get_model_item('extras', 'exporttemplate', 'Export Templates'),
            ),
        ),
        MenuGroup(
            label='Integrations',
            items=(
                get_model_item('extras', 'webhook', 'Webhooks'),
                MenuItem(
                    link='extras:report_list',
                    link_text='Reports',
                    permissions=['extras.view_report']
                ),
                MenuItem(
                    link='extras:script_list',
                    link_text='Scripts',
                    permissions=['extras.view_script']
                ),
            ),
        ),
        MenuGroup(
            label='Other',
            items=(
                get_model_item('extras', 'tag', 'Tags'),
                get_model_item('extras', 'configcontext', 'Config Contexts', actions=['add']),
            ),
        ),
    ),
)

SCHEDULE_MENU = Menu(
    label='值班管理',
    icon_class='mdi mdi-domain',
    groups=(
        MenuGroup(
            label='',
            items=(
                MenuItem(
                    link='schedule:schedule_list',
                    link_text='值班表'
                ),
                MenuItem(
                    link='schedule:legal_day_list',
                    link_text='工作日管理'
                ),
                MenuItem(
                    link='schedule:create_date',
                    link_text='生成日期'
                ),
                MenuItem(
                    link='schedule:create_duty',
                    link_text='值班安排'
                ),
                MenuItem(
                    link='schedule:employee_list',
                    link_text='值班成员'
                ),
                MenuItem(
                    link='schedule:schedule_calendar',
                    link_text='日历视图'
                )
            ),
        ),
    ),
)


TICKET_MENU = Menu(
    label='工单',
    icon_class='mdi mdi-domain',
    groups=(
        MenuGroup(
            label='',
            items=(
                MenuItem(
                    link='ticket:ticket_manage',
                    link_text='工单管理'
                ),
                MenuItem(
                    link='workflow:workflow_manage',
                    link_text='工作流管理'
                )
            ),
        ),
    ),
)

MENUS = [
    ORGANIZATION_MENU,
    DEVICES_MENU,
    CONNECTIONS_MENU,
#     IPAM_MENU,
    VIRTUALIZATION_MENU,
    CIRCUITS_MENU,
    POWER_MENU,
    SCHEDULE_MENU,
    TICKET_MENU,
#     OTHER_MENU,
]

#
# Add plugin menus
#

if registry['plugin_menu_items']:
    plugin_menu_groups = []

    for plugin_name, items in registry['plugin_menu_items'].items():
        plugin_menu_groups.append(
            MenuGroup(
                label=plugin_name,
                items=items
            )
        )

    PLUGIN_MENU = Menu(
        label="Plugins",
        icon_class="mdi mdi-puzzle",
        groups=plugin_menu_groups
    )

    MENUS.append(PLUGIN_MENU)
