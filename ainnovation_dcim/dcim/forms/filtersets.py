from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from dcim.choices import *
from dcim.constants import *
from dcim.models import *
from extras.forms import CustomFieldModelFilterForm, LocalConfigContextFilterForm
from tenancy.forms import TenancyFilterForm
from tenancy.models import Tenant
from utilities.forms import (
    APISelectMultiple, add_blank_choice, BootstrapMixin, ColorField, DynamicModelMultipleChoiceField, StaticSelect,
    StaticSelectMultiple, TagFilterField, BOOLEAN_WITH_BLANK_CHOICES,
)

__all__ = (
    'CableFilterForm',
    'ConsoleConnectionFilterForm',
    'ConsolePortFilterForm',
    'ConsoleServerPortFilterForm',
    'DeviceBayFilterForm',
    'DeviceFilterForm',
    'DeviceRoleFilterForm',
    'DeviceTypeFilterForm',
    'FrontPortFilterForm',
    'InterfaceConnectionFilterForm',
    'InterfaceFilterForm',
    'InventoryItemFilterForm',
    'LocationFilterForm',
    'ManufacturerFilterForm',
    'PlatformFilterForm',
    'PowerConnectionFilterForm',
    'PowerFeedFilterForm',
    'PowerOutletFilterForm',
    'PowerPanelFilterForm',
    'PowerPortFilterForm',
    'RackFilterForm',
    'RackElevationFilterForm',
    'RackReservationFilterForm',
    'RackRoleFilterForm',
    'RearPortFilterForm',
    'RegionFilterForm',
    'SiteFilterForm',
    'SiteGroupFilterForm',
    'VirtualChassisFilterForm',
)


class DeviceComponentFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    field_order = [
        'q', 'name', 'label', 'region_id', 'site_group_id', 'site_id',
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    name = forms.CharField(
        label='设备名',
        required=False
    )
    label = forms.CharField(
        required=False
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
        },
        label=_('区位'),
        fetch_trigger='open'
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        label=_('设备id'),
        fetch_trigger='open'
    )


class RegionFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Region
    field_groups = [
        ['q'],
        ['parent_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('搜索')
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Parent region'),
        fetch_trigger='open'
    )


class SiteGroupFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = SiteGroup
    field_groups = [
        ['q'],
        ['parent_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('搜索')
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Parent group'),
        fetch_trigger='open'
    )


class SiteFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    model = Site
    field_order = ['q', 'status', 'region_id', 'tenant_group_id', 'tenant_id']
    field_groups = [
        ['q', 'tag'],
        ['status', 'region_id', 'group_id'],
        ['tenant_group_id', 'tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All')}),
        label=_('搜索')
    )
    status = forms.MultipleChoiceField(
        choices=SiteStatusChoices,
        required=False,
        label='状态',
        widget=StaticSelectMultiple(),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class LocationFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Location
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All')}),
        label=_('搜索')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'site_id': '$site_id',
        },
        label=_('Parent'),
        fetch_trigger='open'
    )


class RackRoleFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = RackRole
    field_groups = [
        ['q'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All')}),
        label=_('搜索')
    )


class RackFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    model = Rack
    field_order = ['q', 'region_id', 'site_id', 'location_id', 'status', 'role_id', 'tenant_group_id', 'tenant_id']
    field_groups = [
        ['q', 'tag'],
        ['region_id', 'site_id', 'location_id'],
        ['status', 'role_id'],
        ['type', 'width', 'serial', 'asset_tag'],
        ['tenant_group_id', 'tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('位置'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        choices=RackStatusChoices,
        label='状态',
        required=False,
        widget=StaticSelectMultiple()
    )
    type = forms.MultipleChoiceField(
        choices=RackTypeChoices,
        label=_('类型'),
        required=False,
        widget=StaticSelectMultiple()
    )
    width = forms.MultipleChoiceField(
        choices=RackWidthChoices,
        label=_('宽度'),
        required=False,
        widget=StaticSelectMultiple()
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        null_option='None',
        label=_('角色'),
        fetch_trigger='open'
    )
    serial = forms.CharField(
        label=_('序列号'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('资产标签'),
        required=False
    )
    tag = TagFilterField(model)


class RackElevationFilterForm(RackFilterForm):
    field_order = [
        'q', 'region_id', 'site_id', 'location_id', 'id', 'status', 'role_id', 'tenant_group_id',
        'tenant_id',
    ]
    id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        label=_('机架'),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        fetch_trigger='open'
    )


class RackReservationFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    model = RackReservation
    field_order = ['q', 'region_id', 'site_id', 'location_id', 'user_id', 'tenant_group_id', 'tenant_id']
    field_groups = [
        ['q', 'tag'],
        ['user_id'],
        ['region_id', 'site_id', 'location_id'],
        ['tenant_group_id', 'tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.prefetch_related('site'),
        required=False,
        label=_('位置'),
        null_option='None',
        fetch_trigger='open'
    )
    user_id = DynamicModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('用户'),
        widget=APISelectMultiple(
            api_url='/api/users/users/',
        ),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class ManufacturerFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Manufacturer
    field_groups = [
        ['q'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All')}),
        label=_('Search')
    )


class DeviceTypeFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = DeviceType
    field_groups = [
        ['q', 'tag'],
        ['manufacturer_id', 'subdevice_role'],
        ['console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces', 'pass_through_ports'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('制造商'),
        fetch_trigger='open'
    )
    subdevice_role = forms.MultipleChoiceField(
        choices=add_blank_choice(SubdeviceRoleChoices),
        required=False,
        label=_('子设备角色'),
        widget=StaticSelectMultiple()
    )
    console_ports = forms.NullBooleanField(
        required=False,
        label='有控制台端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_server_ports = forms.NullBooleanField(
        required=False,
        label='有控制台服务端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_ports = forms.NullBooleanField(
        required=False,
        label='有电源端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_outlets = forms.NullBooleanField(
        required=False,
        label='有电源插座',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    interfaces = forms.NullBooleanField(
        required=False,
        label='有接口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    pass_through_ports = forms.NullBooleanField(
        required=False,
        label='有直通端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)


class DeviceRoleFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = DeviceRole
    field_groups = [
        ['q'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )


class PlatformFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Platform
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('制造商'),
        fetch_trigger='open'
    )


class DeviceFilterForm(BootstrapMixin, LocalConfigContextFilterForm, TenancyFilterForm, CustomFieldModelFilterForm):
    model = Device
    field_order = [
        'q', 'region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id', 'status', 'role_id', 'tenant_group_id',
        'tenant_id', 'manufacturer_id', 'device_type_id', 'asset_tag', 'mac_address', 'has_primary_ip',
    ]
    field_groups = [
        ['q', 'tag'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id'],
        ['status', 'role_id', 'serial', 'asset_tag', 'mac_address'],
        ['manufacturer_id', 'device_type_id', 'platform_id'],
        ['tenant_group_id', 'tenant_id'],
        [
            'has_primary_ip', 'virtual_chassis_member', 'console_ports', 'console_server_ports', 'power_ports',
            'power_outlets', 'interfaces',
        ],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('位置'),
        fetch_trigger='open'
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        label=_('机架'),
        fetch_trigger='open'
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        label=_('角色'),
        fetch_trigger='open'
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('制造商'),
        fetch_trigger='open'
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('设备类型'),
        fetch_trigger='open'
    )
    platform_id = DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        null_option='None',
        label=_('平台'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        choices=DeviceStatusChoices,
        required=False,
        label=_('状态'),
        widget=StaticSelectMultiple()
    )
    serial = forms.CharField(
        label=_('序列号'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('资产编号'),
        required=False
    )
    mac_address = forms.CharField(
        required=False,
        label='MAC 地址'
    )
    has_primary_ip = forms.NullBooleanField(
        required=False,
        label='主IP',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    virtual_chassis_member = forms.NullBooleanField(
        required=False,
        label='Virtual chassis member',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_ports = forms.NullBooleanField(
        required=False,
        label='有控制台端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_server_ports = forms.NullBooleanField(
        required=False,
        label='有控制台服务端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_ports = forms.NullBooleanField(
        required=False,
        label='有电源端口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_outlets = forms.NullBooleanField(
        required=False,
        label='有电源插座',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    interfaces = forms.NullBooleanField(
        required=False,
        label='有接口',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
#     pass_through_ports = forms.NullBooleanField(
#         required=False,
#         label='Has pass-through ports',
#         widget=StaticSelect(
#             choices=BOOLEAN_WITH_BLANK_CHOICES
#         )
#     )
    tag = TagFilterField(model)


class VirtualChassisFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    model = VirtualChassis
    field_order = ['q', 'region_id', 'site_group_id', 'site_id', 'tenant_group_id', 'tenant_id']
    field_groups = [
        ['q', 'tag'],
        ['region_id', 'site_group_id', 'site_id'],
        ['tenant_group_id', 'tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class CableFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Cable
    field_groups = [
        ['q', 'tag'],
        ['site_id', 'rack_id', 'device_id'],
        ['type', 'status', 'color'],
        ['tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('租户'),
        fetch_trigger='open'
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_('机架'),
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        fetch_trigger='open'
    )
    type = forms.MultipleChoiceField(
        choices=add_blank_choice(CableTypeChoices),
        required=False,
        label=_('类型'),
        widget=StaticSelect()
    )
    status = forms.ChoiceField(
        required=False,
        label=_('状态'),
        choices=add_blank_choice(CableStatusChoices),
        widget=StaticSelect()
    )
    color = ColorField(
        label=_('颜色'),
        required=False
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'tenant_id': '$tenant_id',
            'rack_id': '$rack_id',
        },
        label=_('设备'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class PowerPanelFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = PowerPanel
    field_groups = (
        ('q', 'tag'),
        ('region_id', 'site_group_id', 'site_id', 'location_id')
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('位置'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class PowerFeedFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = PowerFeed
    field_groups = [
        ['q', 'tag'],
        ['region_id', 'site_group_id', 'site_id'],
        ['power_panel_id', 'rack_id'],
        ['status', 'type', 'supply', 'phase', 'voltage', 'amperage', 'max_utilization'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('站点组'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    power_panel_id = DynamicModelMultipleChoiceField(
        queryset=PowerPanel.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('电源板'),
        fetch_trigger='open'
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('机架'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        choices=PowerFeedStatusChoices,
        label=_('状态'),
        required=False,
        widget=StaticSelectMultiple()
    )
    type = forms.ChoiceField(
        choices=add_blank_choice(PowerFeedTypeChoices),
        label=_('类型'),
        required=False,
        widget=StaticSelect()
    )
    supply = forms.ChoiceField(
        choices=add_blank_choice(PowerFeedSupplyChoices),
        required=False,
        label=_('电流类型'),
        widget=StaticSelect()
    )
    phase = forms.ChoiceField(
        choices=add_blank_choice(PowerFeedPhaseChoices),
        required=False,
        label=_('相'),
        widget=StaticSelect()
    )
    voltage = forms.IntegerField(
        label=_('电压'),
        required=False
    )
    amperage = forms.IntegerField(
        label=_('电流'),
        required=False
    )
    max_utilization = forms.IntegerField(
        label=_('最大利用率'),
        required=False
    )
    tag = TagFilterField(model)


#
# Device components
#

class ConsolePortFilterForm(DeviceComponentFilterForm):
    model = ConsolePort
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type', 'speed'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=ConsolePortTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    speed = forms.MultipleChoiceField(
        choices=ConsolePortSpeedChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    tag = TagFilterField(model)


class ConsoleServerPortFilterForm(DeviceComponentFilterForm):
    model = ConsoleServerPort
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type', 'speed'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=ConsolePortTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    speed = forms.MultipleChoiceField(
        choices=ConsolePortSpeedChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    tag = TagFilterField(model)


class PowerPortFilterForm(DeviceComponentFilterForm):
    model = PowerPort
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=PowerPortTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    tag = TagFilterField(model)


class PowerOutletFilterForm(DeviceComponentFilterForm):
    model = PowerOutlet
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=PowerOutletTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    tag = TagFilterField(model)


class InterfaceFilterForm(DeviceComponentFilterForm):
    model = Interface
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type', 'enabled', 'mgmt_only', 'mac_address'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=InterfaceTypeChoices,
        required=False,
        label=_('类型'),
        widget=StaticSelectMultiple()
    )
    enabled = forms.NullBooleanField(
        required=False,
        label=_('是否可用'),
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    mgmt_only = forms.NullBooleanField(
        required=False,
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    mac_address = forms.CharField(
        required=False,
        label='MAC地址'
    )
    tag = TagFilterField(model)


class FrontPortFilterForm(DeviceComponentFilterForm):
    field_groups = [
        ['q', 'tag'],
        ['name', 'type', 'color'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    model = FrontPort
    type = forms.MultipleChoiceField(
        choices=PortTypeChoices,
        label=_('类型'),
        required=False,
        widget=StaticSelectMultiple()
    )
    color = ColorField(
        label=_('颜色'),
        required=False
    )
    tag = TagFilterField(model)


class RearPortFilterForm(DeviceComponentFilterForm):
    model = RearPort
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'type', 'color'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    type = forms.MultipleChoiceField(
        choices=PortTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    color = ColorField(
        required=False
    )
    tag = TagFilterField(model)


class DeviceBayFilterForm(DeviceComponentFilterForm):
    model = DeviceBay
    field_groups = [
        ['q', 'tag'],
        ['name', 'label'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    tag = TagFilterField(model)


class InventoryItemFilterForm(DeviceComponentFilterForm):
    model = InventoryItem
    field_groups = [
        ['q', 'tag'],
        ['name', 'label', 'manufacturer_id', 'serial', 'asset_tag', 'discovered'],
        ['region_id', 'site_group_id', 'site_id', 'location_id', 'device_id'],
    ]
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer'),
        fetch_trigger='open'
    )
    serial = forms.CharField(
        required=False
    )
    asset_tag = forms.CharField(
        required=False
    )
    discovered = forms.NullBooleanField(
        required=False,
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)


#
# Connections
#

class ConsoleConnectionFilterForm(BootstrapMixin, forms.Form):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('设备'),
        fetch_trigger='open'
    )


class PowerConnectionFilterForm(BootstrapMixin, forms.Form):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('设备'),
        fetch_trigger='open'
    )


class InterfaceConnectionFilterForm(BootstrapMixin, forms.Form):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('地区'),
        fetch_trigger='open'
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('设备'),
        fetch_trigger='open'
    )
