from django import forms

from circuits.choices import CircuitStatusChoices
from circuits.models import *
from extras.forms import AddRemoveTagsForm, CustomFieldModelBulkEditForm
from tenancy.models import Tenant
from utilities.forms import (
    add_blank_choice, BootstrapMixin, CommentField, DynamicModelChoiceField, SmallTextarea, StaticSelect,
)

__all__ = (
    'CircuitBulkEditForm',
    'CircuitTypeBulkEditForm',
    'ProviderBulkEditForm',
    'ProviderNetworkBulkEditForm',
)


class ProviderBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    asn = forms.IntegerField(
        required=False,
        label='ASN'
    )
    account = forms.CharField(
        max_length=30,
        required=False,
        label='Account number'
    )
    portal_url = forms.URLField(
        required=False,
        label='Portal'
    )
    noc_contact = forms.CharField(
        required=False,
        widget=SmallTextarea,
        label='NOC contact'
    )
    admin_contact = forms.CharField(
        required=False,
        widget=SmallTextarea,
        label='Admin contact'
    )
    comments = CommentField(
        widget=SmallTextarea,
        label='Comments'
    )

    class Meta:
        nullable_fields = [
            'asn', 'account', 'portal_url', 'noc_contact', 'admin_contact', 'comments',
        ]


class ProviderNetworkBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ProviderNetwork.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='网络提供商',
        required=False
    )
    description = forms.CharField(
        max_length=100,
        label='描述',
        required=False
    )
    comments = CommentField(
        widget=SmallTextarea,
        label='评论'
    )

    class Meta:
        nullable_fields = [
            'description', 'comments',
        ]


class CircuitTypeBulkEditForm(BootstrapMixin, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=CircuitType.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        max_length=200,
        label='描述',
        required=False
    )

    class Meta:
        nullable_fields = ['description']


class CircuitBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Circuit.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    type = DynamicModelChoiceField(
        queryset=CircuitType.objects.all(),
        label='电路类型',
        required=False
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        label='提供商',
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(CircuitStatusChoices),
        required=False,
        label='状态',
        initial='',
        widget=StaticSelect()
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        label='租户',
        required=False
    )
    commit_rate = forms.IntegerField(
        required=False,
        label='传输速率(Kbps)'
    )
    description = forms.CharField(
        max_length=100,
        label='描述',
        required=False
    )
    comments = CommentField(
        widget=SmallTextarea,
        label='评论'
    )

    class Meta:
        nullable_fields = [
            'tenant', 'commit_rate', 'description', 'comments',
        ]
