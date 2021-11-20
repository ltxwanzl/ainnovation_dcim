from django import forms

from dcim.choices import InterfaceModeChoices
from dcim.constants import INTERFACE_MTU_MAX, INTERFACE_MTU_MIN
from dcim.models import DeviceRole, Platform, Region, Site, SiteGroup
from extras.forms import AddRemoveTagsForm, CustomFieldModelBulkEditForm
from ipam.models import VLAN
from tenancy.models import Tenant
from utilities.forms import (
    add_blank_choice, BootstrapMixin, BulkEditNullBooleanSelect, BulkRenameForm, CommentField, DynamicModelChoiceField,
    DynamicModelMultipleChoiceField, SmallTextarea, StaticSelect
)
from virtualization.choices import *
from virtualization.models import *

__all__ = (
    'ClusterBulkEditForm',
    'ClusterGroupBulkEditForm',
    'ClusterTypeBulkEditForm',
    'VirtualMachineBulkEditForm',
    'VMInterfaceBulkEditForm',
    'VMInterfaceBulkRenameForm',
)


class ClusterTypeBulkEditForm(BootstrapMixin, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ClusterType.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        max_length=200,
        label='描述',
        required=False
    )

    class Meta:
        nullable_fields = ['description']


class ClusterGroupBulkEditForm(BootstrapMixin, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ClusterGroup.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        max_length=200,
        label='描述',
        required=False
    )

    class Meta:
        nullable_fields = ['description']


class ClusterBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        label='类型',
        required=False
    )
    group = DynamicModelChoiceField(
        queryset=ClusterGroup.objects.all(),
        label='集群组',
        required=False
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        label='租户',
        required=False
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        label='地区',
        required=False,
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        label='站点组',
        required=False,
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label='站点',
        required=False,
        query_params={
            'region_id': '$region',
            'group_id': '$site_group',
        }
    )
    comments = CommentField(
        widget=SmallTextarea,
        label='评论'
    )

    class Meta:
        nullable_fields = [
            'group', 'site', 'comments', 'tenant',
        ]


class VirtualMachineBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(VirtualMachineStatusChoices),
        required=False,
        label='状态',
        initial='',
        widget=StaticSelect(),
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        label='集群',
        required=False
    )
    role = DynamicModelChoiceField(
        queryset=DeviceRole.objects.filter(
            vm_role=True
        ),
        label='角色',
        required=False,
        query_params={
            "vm_role": "True"
        }
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        label='租户',
        required=False
    )
    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        label='平台',
        required=False
    )
    vcpus = forms.IntegerField(
        required=False,
        label='CPU核数'
    )
    memory = forms.IntegerField(
        required=False,
        label='内存(MB)'
    )
    disk = forms.IntegerField(
        required=False,
        label='硬盘(GB)'
    )
    comments = CommentField(
        widget=SmallTextarea,
        label='评论'
    )

    class Meta:
        nullable_fields = [
            'role', 'tenant', 'platform', 'vcpus', 'memory', 'disk', 'comments',
        ]


class VMInterfaceBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VMInterface.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    virtual_machine = forms.ModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label='虚拟机',
        disabled=True,
        widget=forms.HiddenInput()
    )
    parent = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        label='父接口',
        required=False
    )
    enabled = forms.NullBooleanField(
        required=False,
        label='是否可用',
        widget=BulkEditNullBooleanSelect()
    )
    mtu = forms.IntegerField(
        required=False,
        min_value=INTERFACE_MTU_MIN,
        max_value=INTERFACE_MTU_MAX,
        label='MTU'
    )
    description = forms.CharField(
        max_length=100,
        label='描述',
        required=False
    )
    mode = forms.ChoiceField(
        choices=add_blank_choice(InterfaceModeChoices),
        required=False,
        widget=StaticSelect()
    )
    untagged_vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.all(),
        label='未标记VLAN',
        required=False
    )
    tagged_vlans = DynamicModelMultipleChoiceField(
        queryset=VLAN.objects.all(),
        label='标记VLAN',
        required=False
    )

    class Meta:
        nullable_fields = [
            'parent', 'mtu', 'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'virtual_machine' in self.initial:
            vm_id = self.initial.get('virtual_machine')

            # Restrict parent interface assignment by VM
            self.fields['parent'].widget.add_query_param('virtual_machine_id', vm_id)

            # Limit VLAN choices by virtual machine
            self.fields['untagged_vlan'].widget.add_query_param('available_on_virtualmachine', vm_id)
            self.fields['tagged_vlans'].widget.add_query_param('available_on_virtualmachine', vm_id)

        else:
            # See 5643
            if 'pk' in self.initial:
                site = None
                interfaces = VMInterface.objects.filter(pk__in=self.initial['pk']).prefetch_related(
                    'virtual_machine__cluster__site'
                )

                # Check interface sites.  First interface should set site, further interfaces will either continue the
                # loop or reset back to no site and break the loop.
                for interface in interfaces:
                    if site is None:
                        site = interface.virtual_machine.cluster.site
                    elif interface.virtual_machine.cluster.site is not site:
                        site = None
                        break

                if site is not None:
                    self.fields['untagged_vlan'].widget.add_query_param('site_id', site.pk)
                    self.fields['tagged_vlans'].widget.add_query_param('site_id', site.pk)


class VMInterfaceBulkRenameForm(BulkRenameForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VMInterface.objects.all(),
        widget=forms.MultipleHiddenInput()
    )