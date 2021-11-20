from django.db import models

# Create your models here.


# 以下是值班表
class Employee(models.Model):
    name = models.CharField(max_length=10, db_index=True, verbose_name='姓名')
    num = models.DecimalField(max_digits=5, unique=True, decimal_places=0, verbose_name='序号')
    available = models.BooleanField(default=False, verbose_name='是否排班')

    class Meta:
        verbose_name = '值班成员'
        verbose_name_plural = '值班成员'
        ordering = ['num']

    def __str__(self):
        return self.name


class LegalDay(models.Model):
    Legal_Type = (
        (0, '法定休息日'),
        (1, '法定工作日')
    )
    date = models.DateField(unique=True, verbose_name='日期')
    legal_type = models.IntegerField(choices=Legal_Type, default=0, verbose_name='法定选择')

    class Meta:
        verbose_name = '法定日期'
        verbose_name_plural = '法定日期'
        ordering = ['-date']

    def __str__(self):
        return '{}({})'.format(self.date, self.get_legal_type_display())



class Schedule(models.Model):
    Duty_Type = (
        (0, '不用值班'),
        (1, '晚上值班'),
        (2, '周末值班'),
    )

    date = models.DateField(unique=True, verbose_name='日期')
    is_workday = models.BooleanField(default=False, verbose_name='是否工作日')
    duty_type = models.IntegerField(choices=Duty_Type, default=0, verbose_name='值班类型')
    staff = models.CharField(max_length=10, null=True, blank=True,  verbose_name='值班人员')
    real_staff = models.CharField(max_length=10, null=True, blank=True, verbose_name='实际值班人员')

    class Meta:
        verbose_name = '值班安排'
        verbose_name_plural = '值班安排'
        ordering = ['-date']  # 日期倒序，新的在前

    def __str__(self):
        return '{}({})'.format(self.date, self.staff)