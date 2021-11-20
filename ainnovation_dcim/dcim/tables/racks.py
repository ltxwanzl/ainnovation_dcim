import django_tables2 as tables
from django_tables2.utils import Accessor

from dcim.models import Rack, RackReservation, RackRole
from tenancy.tables import TenantColumn
from utilities.tables import (
    BaseTable, ButtonsColumn, ChoiceFieldColumn, ColorColumn, ColoredLabelColumn, LinkedCountColumn, MarkdownColumn,
    TagColumn, ToggleColumn, UtilizationColumn,
)

__all__ = (
    'RackTable',
    'RackReservationTable',
    'RackRoleTable',
)


#
# Rack roles
#

class RackRoleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    rack_count = tables.Column(verbose_name='Racks')
    color = ColorColumn()
    actions = ButtonsColumn(RackRole)

    class Meta(BaseTable.Meta):
        model = RackRole
        fields = ('pk', 'name', 'rack_count', 'color', 'description', 'slug', 'actions')
        default_columns = ('pk', 'name', 'rack_count', 'color', 'description', 'actions')


#
# Racks
#

class RackTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(
        order_by=('_name',),
        linkify=True
    )
    location = tables.Column(
        linkify=True
    )
    site = tables.Column(
        linkify=True
    )
    tenant = TenantColumn()
    status = ChoiceFieldColumn()
    role = ColoredLabelColumn()
    u_height = tables.TemplateColumn(
        template_code="{{ record.u_height }}U",
        verbose_name='高度'
    )
    comments = MarkdownColumn()
    device_count = LinkedCountColumn(
        viewname='dcim:device_list',
        url_params={'rack_id': 'pk'},
        verbose_name='设备数'
    )
    get_utilization = UtilizationColumn(
        orderable=False,
        verbose_name='空间'
    )
    get_power_utilization = UtilizationColumn(
        orderable=False,
        verbose_name='Power'
    )
    tags = TagColumn(
        url_name='dcim:rack_list'
    )

    class Meta(BaseTable.Meta):
        model = Rack
        fields = (
            'pk', 'name', 'site', 'location', 'status', 'facility_id', 'tenant', 'role', 'serial', 'asset_tag', 'type',
            'width', 'u_height', 'comments', 'device_count', 'get_utilization', 'get_power_utilization', 'tags',
        )
        default_columns = (
            'pk', 'name', 'site', 'location', 'status', 'facility_id', 'tenant', 'role', 'u_height', 'device_count',
            'get_utilization', 'get_power_utilization',
        )


#
# Rack reservations
#

class RackReservationTable(BaseTable):
    pk = ToggleColumn()
    reservation = tables.Column(
        accessor='pk',
        verbose_name='预占',
        linkify=True
    )
    site = tables.Column(
        accessor=Accessor('rack__site'),
        verbose_name='站点',
        linkify=True
    )
    tenant = TenantColumn(
        verbose_name='租户'
    )
    rack = tables.Column(
        verbose_name='机架',
        linkify=True
    )
    unit_list = tables.Column(
        orderable=False,
        verbose_name='单位'
    )
    tags = TagColumn(
        url_name='dcim:rackreservation_list'
    )
    actions = ButtonsColumn(RackReservation)

    class Meta(BaseTable.Meta):
        model = RackReservation
        fields = (
            'pk', 'reservation', 'site', 'rack', 'unit_list', '', 'created', 'tenant', 'description', 'tags',
            'actions',
        )
        default_columns = (
            'pk', 'reservation', 'site', 'rack', 'unit_list', 'user', 'description', 'actions',
        )
