import binascii
import os

from django.contrib.auth.models import Group, User
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from netbox.models import BigIDModel
from utilities.querysets import RestrictedQuerySet
from utilities.utils import flatten_dict
from .constants import *

from loon_base_model import BaseModel


__all__ = (
    'ObjectPermission',
    'Token',
    'UserConfig',
)


#
# Proxy models for admin
#

class AdminGroup(Group):
    """
    Proxy contrib.auth.models.Group for the admin UI
    """
    class Meta:
        verbose_name = 'Group'
        proxy = True


# class AdminUser(User):
#     """
#     用户
#     """
#     alias = models.CharField('姓名', max_length=50, default='')
#     phone = models.CharField('电话', max_length=13, default='')
#     dept_id = models.IntegerField('部门id', default=0)
#     is_admin = models.BooleanField('超级管理员', default=False)
#     is_workflow_admin = models.BooleanField('工作流管理员', default=False)  # 只可以操作自己有权限的工作流、工单
#
#     creator = models.CharField('创建人', max_length=50)
#     gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
#     gmt_modified = models.DateTimeField('更新时间', auto_now=True)
#     is_deleted = models.BooleanField('已删除', default=False)
#
#     @property
#     def is_staff(self):
#         return self.is_active
#
#     def get_short_name(self):
#         return self.username
#
#     def get_alias_name(self):
#         return self.alias
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_perms(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def dept_name(self):
#         dept_id = self.dept_id
#         dept_object = LoonDept.objects.filter(id=dept_id)
#         if dept_object:
#             return dept_object[0].name
#         else:
#             return '部门id不存在'
#     class Meta:
#         verbose_name = 'User'
#         proxy = True

class LoonUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, dep=0):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser):
    """
    用户
    """
    username = models.CharField('用户名', max_length=50, unique=True)
    alias = models.CharField('姓名', max_length=50, default='')
    email = models.EmailField('邮箱', max_length=255)
    phone = models.CharField('电话', max_length=13, default='')
    dept_id = models.IntegerField('部门id', default=0)
    is_active = models.BooleanField('已激活', default=True)
    is_admin = models.BooleanField('超级管理员', default=False)
    is_workflow_admin = models.BooleanField('工作流管理员', default=False)  # 只可以操作自己有权限的工作流、工单

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    objects = LoonUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        return self.is_active

    def get_short_name(self):
        return self.username

    def get_alias_name(self):
        return self.alias

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def dept_name(self):
        dept_id = self.dept_id
        dept_object = LoonDept.objects.filter(id=dept_id)
        if dept_object:
            return dept_object[0].name
        else:
            return '部门id不存在'

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif attr == 'dept_id':
                dept_obj = LoonDept.objects.filter(id=getattr(self, attr), is_deleted=0).first()
                dept_name = dept_obj.name if dept_obj else ''
                dict_result['dept_info'] = dict(dept_id=getattr(self, attr), dept_name=dept_name)
            elif attr == 'password':
                pass
            elif attr == 'creator':
                creator_obj = AdminUser.objects.filter(username=getattr(self, attr)).first()
                if creator_obj:
                    dict_result['creator_info'] = dict(creator_id= creator_obj.id, creator_alias=creator_obj.alias, creator_username=creator_obj.username)
                else:
                    dict_result['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, attr))
            else:
                dict_result[attr] = getattr(self, attr)

        return dict_result

    def get_json(self):
        import json
        dict_result = self.get_dict()
        return json.dumps(dict_result)


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
#
# User preferences
#


class UserConfig(models.Model):
    """
    This model stores arbitrary user-specific preferences in a JSON data structure.
    """
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='config'
    )
    data = models.JSONField(
        default=dict
    )

    class Meta:
        ordering = ['user']
        verbose_name = verbose_name_plural = 'User Preferences'

    def get(self, path, default=None):
        """
        Retrieve a configuration parameter specified by its dotted path. Example:

            userconfig.get('foo.bar.baz')

        :param path: Dotted path to the configuration key. For example, 'foo.bar' returns self.data['foo']['bar'].
        :param default: Default value to return for a nonexistent key (default: None).
        """
        d = self.data
        keys = path.split('.')

        # Iterate down the hierarchy, returning the default value if any invalid key is encountered
        for key in keys:
            if type(d) is dict and key in d:
                d = d.get(key)
            else:
                return default

        return d

    def all(self):
        """
        Return a dictionary of all defined keys and their values.
        """
        return flatten_dict(self.data)

    def set(self, path, value, commit=False):
        """
        Define or overwrite a configuration parameter. Example:

            userconfig.set('foo.bar.baz', 123)

        Leaf nodes (those which are not dictionaries of other nodes) cannot be overwritten as dictionaries. Similarly,
        branch nodes (dictionaries) cannot be overwritten as single values. (A TypeError exception will be raised.) In
        both cases, the existing key must first be cleared. This safeguard is in place to help avoid inadvertently
        overwriting the wrong key.

        :param path: Dotted path to the configuration key. For example, 'foo.bar' sets self.data['foo']['bar'].
        :param value: The value to be written. This can be any type supported by JSON.
        :param commit: If true, the UserConfig instance will be saved once the new value has been applied.
        """
        d = self.data
        keys = path.split('.')

        # Iterate through the hierarchy to find the key we're setting. Raise TypeError if we encounter any
        # interim leaf nodes (keys which do not contain dictionaries).
        for i, key in enumerate(keys[:-1]):
            if key in d and type(d[key]) is dict:
                d = d[key]
            elif key in d:
                err_path = '.'.join(path.split('.')[:i + 1])
                raise TypeError(f"Key '{err_path}' is a leaf node; cannot assign new keys")
            else:
                d = d.setdefault(key, {})

        # Set a key based on the last item in the path. Raise TypeError if attempting to overwrite a non-leaf node.
        key = keys[-1]
        if key in d and type(d[key]) is dict:
            raise TypeError(f"Key '{path}' has child keys; cannot assign a value")
        else:
            d[key] = value

        if commit:
            self.save()

    def clear(self, path, commit=False):
        """
        Delete a configuration parameter specified by its dotted path. The key and any child keys will be deleted.
        Example:

            userconfig.clear('foo.bar.baz')

        Invalid keys will be ignored silently.

        :param path: Dotted path to the configuration key. For example, 'foo.bar' deletes self.data['foo']['bar'].
        :param commit: If true, the UserConfig instance will be saved once the new value has been applied.
        """
        d = self.data
        keys = path.split('.')

        for key in keys[:-1]:
            if key not in d:
                break
            if type(d[key]) is dict:
                d = d[key]

        key = keys[-1]
        d.pop(key, None)  # Avoid a KeyError on invalid keys

        if commit:
            self.save()


@receiver(post_save, sender=User)
def create_userconfig(instance, created, **kwargs):
    """
    Automatically create a new UserConfig when a new User is created.
    """
    if created:
        UserConfig(user=instance).save()


#
# REST API
#

class Token(BigIDModel):
    """
    An API token used for user authentication. This extends the stock model to allow each user to have multiple tokens.
    It also supports setting an expiration time and toggling write ability.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tokens'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    expires = models.DateTimeField(
        blank=True,
        null=True
    )
    key = models.CharField(
        max_length=40,
        unique=True,
        validators=[MinLengthValidator(40)]
    )
    write_enabled = models.BooleanField(
        default=True,
        help_text='Permit create/update/delete operations using this key'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        pass

    def __str__(self):
        # Only display the last 24 bits of the token to avoid accidental exposure.
        return f"{self.key[-6:]} ({self.user})"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        # Generate a random 160-bit key expressed in hexadecimal.
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def is_expired(self):
        if self.expires is None or timezone.now() < self.expires:
            return False
        return True


#
# Permissions
#

class ObjectPermission(BigIDModel):
    """
    A mapping of view, add, change, and/or delete permission for users and/or groups to an arbitrary set of objects
    identified by ORM query parameters.
    """
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    enabled = models.BooleanField(
        default=True
    )
    object_types = models.ManyToManyField(
        to=ContentType,
        limit_choices_to=OBJECTPERMISSION_OBJECT_TYPES,
        related_name='object_permissions'
    )
    groups = models.ManyToManyField(
        to=Group,
        blank=True,
        related_name='object_permissions'
    )
    users = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='object_permissions'
    )
    actions = ArrayField(
        base_field=models.CharField(max_length=30),
        help_text="The list of actions granted by this permission"
    )
    constraints = models.JSONField(
        blank=True,
        null=True,
        help_text="Queryset filter matching the applicable objects of the selected type(s)"
    )

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        verbose_name = "permission"

    def __str__(self):
        return self.name

    def list_constraints(self):
        """
        Return all constraint sets as a list (even if only a single set is defined).
        """
        if type(self.constraints) is not list:
            return [self.constraints]
        return self.constraints


class LoonDept(BaseModel):
    """
    部门
    """
    name = models.CharField('名称', max_length=50, help_text='部门名称')
    parent_dept_id = models.IntegerField('上级部门id', blank=True, default=0)
    leader = models.CharField('部门leader', max_length=50, blank=True, default='', help_text='部门的leader, loonuser表中的用户名')
    approver = models.CharField('审批人', max_length=100, blank=True, default='', help_text='user表中的用户名, 逗号隔开多个user。当工作流设置为leader审批时， 优先以审批人为准，如果审批人为空，则取leader')
    label = models.CharField('标签', max_length=50, blank=True, default='', help_text='因为部门信息一般是从别处同步过来， 为保证对应关系，同步时可以在此字段设置其他系统中相应的唯一标识')

    creator = models.CharField('创建人', max_length=50, help_text='user表中的用户名')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def get_dict(self):
        dept_dict_info = super().get_dict()
        creator_obj = AdminUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            dept_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias)
        else:
            dept_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        if self.parent_dept_id:
            parent_dept_obj = LoonDept.objects.filter(id=self.parent_dept_id, is_deleted=0).first()
            if parent_dept_obj:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name=parent_dept_obj.name)
            else:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='未知')
        else:
            parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='')
        dept_dict_info['parent_dept_info'] = parent_dept_info

        if self.leader:
            leader_obj = AdminUser.objects.filter(username=self.leader).first()
            if leader_obj:
                dept_dict_info['leader_info'] = {
                    'leader_username': leader_obj.username,
                    'leader_alias': leader_obj.alias,
                    'leader_id': leader_obj.id,
                }
            else:
                dept_dict_info['leader_info'] = {
                    'leader_username': self.leader,
                    'leader_alias': self.leader,
                    'leader_id': 0,
                }
        else:
            dept_dict_info['leader_info'] = {
                'leader_username': '',
                'leader_alias': '',
                'leader_id': 0,
            }

        if self.approver:
            approver_list = self.approver.split(',')
            approver_info_list = []
            for approver in approver_list:
                approver_obj = AdminUser.objects.filter(username=approver).first()
                if approver_obj:
                    approver_info_list.append({
                        'approver_name': approver_obj.username,
                        'approver_alias': approver_obj.alias,
                        'approver_id': approver_obj.id,
                    })
                else:
                    approver_info_list.append({
                        'approver_name': approver,
                        'approver_alias': approver,
                        'approver_id': 0,
                    })
            dept_dict_info['approver_info'] = approver_info_list
        else:
            dept_dict_info['approver_info'] = []

        return dept_dict_info


class LoonRole(BaseModel):
    """
    角色
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=50, default='')

    label = models.CharField('标签', max_length=50, blank=True, default='{}', help_text='因为角色信息也可能是从别处同步过来， 为保证对应关系，同步时可以在此字段设置其他系统中相应的唯一标识,字典的json格式')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = AdminUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        return role_dict_info


class LoonUserRole(BaseModel):
    """
    用户角色
    """
    user_id = models.IntegerField('用户id')
    role_id = models.IntegerField('角色id')

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'