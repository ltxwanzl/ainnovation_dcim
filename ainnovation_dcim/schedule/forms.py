from django import forms
from .models import LegalDay, Employee


class LegalDayForm(forms.ModelForm):
    class Meta:
        model = LegalDay
        fields = '__all__'

    # django是通过“__new__”方法，找到ModelForm里面的每个字段的，然后循环出每个字段添加自定义样式
    def __new__(cls, *args, **kwargs):
        # cls.base_fields是一个元祖，里面是 所有的  【(字段名，字段的对象),(),()】
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            # 添加属性
            filed_obj.widget.attrs.update({'class': 'form-control'})

        return forms.ModelForm.__new__(cls)



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    # django是通过“__new__”方法，找到ModelForm里面的每个字段的，然后循环出每个字段添加自定义样式
    def __new__(cls, *args, **kwargs):
        # cls.base_fields是一个元祖，里面是 所有的  【(字段名，字段的对象),(),()】
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            if field_name != 'available':
                # 添加属性，复选框不添加样式
                filed_obj.widget.attrs.update({'class': 'form-control'})

        return forms.ModelForm.__new__(cls)