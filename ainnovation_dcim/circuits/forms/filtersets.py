from django import forms
from django.utils.translation import gettext as _

from circuits.choices import CircuitStatusChoices
from circuits.models import *
from dcim.models import Region, Site, SiteGroup
from extras.forms import CustomFieldModelFilterForm
from tenancy.forms import TenancyFilterForm
from utilities.forms import BootstrapMixin, DynamicModelMultipleChoiceField, StaticSelectMultiple, TagFilterField

__all__ = (
    'CircuitFilterForm',
    'CircuitTypeFilterForm',
    'ProviderFilterForm',
    'ProviderNetworkFilterForm',
)


class ProviderFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = Provider
    field_groups = [
        ['q', 'tag'],
        ['region_id', 'site_group_id', 'site_id'],
        ['asn'],
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
            'site_group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    asn = forms.IntegerField(
        required=False,
        label=_('ASN')
    )
    tag = TagFilterField(model)


class ProviderNetworkFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = ProviderNetwork
    field_groups = (
        ('q', 'tag'),
        ('provider_id',),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    provider_id = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label=_('电路提供商'),
        fetch_trigger='open'
    )
    tag = TagFilterField(model)


class CircuitTypeFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    model = CircuitType
    field_groups = [
        ['q'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )


class CircuitFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    model = Circuit
    field_groups = [
        ['q', 'tag'],
        ['provider_id', 'provider_network_id'],
        ['type_id', 'status', 'commit_rate'],
        ['region_id', 'site_group_id', 'site_id'],
        ['tenant_group_id', 'tenant_id'],
    ]
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('All Fields')}),
        label=_('Search')
    )
    type_id = DynamicModelMultipleChoiceField(
        queryset=CircuitType.objects.all(),
        required=False,
        label=_('类型'),
        fetch_trigger='open'
    )
    provider_id = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label=_('电路提供商'),
        fetch_trigger='open'
    )
    provider_network_id = DynamicModelMultipleChoiceField(
        queryset=ProviderNetwork.objects.all(),
        required=False,
        query_params={
            'provider_id': '$provider_id'
        },
        label=_('提供商网络'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        choices=CircuitStatusChoices,
        required=False,
        label=_('状态'),
        widget=StaticSelectMultiple()
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
            'site_group_id': '$site_group_id',
        },
        label=_('站点'),
        fetch_trigger='open'
    )
    commit_rate = forms.IntegerField(
        required=False,
        min_value=0,
        label=_('传输速率(Kbps)')
    )
    tag = TagFilterField(model)
