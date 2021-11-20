from django.urls import path

from . import views
from .views import ScheduleIndex, LegalDayList, LegalDayCreate, LegalDayUpdate, LegalDayDelete
from .views import EmployeeList, EmployeeCreate, EmployeeDelete, EmployeeUpdate
from .views import GenerateDateInfo
from .views import GenerateDutyInfo

from django.contrib.auth.decorators import permission_required
app_name = 'schedule'

urlpatterns = [
    path('schedule/',ScheduleIndex.as_view(), name='schedule_list'),  # 值班表首页
    path('schedule/renew_staff/', views.renew_staff, name='renew_staff'),  # 生成日期数据
    path('schedule/calendar/', views.schedule_calendar, name='schedule_calendar'),  # 日历列表
    path('schedule/schedule_calendar_data/', views.schedule_calendar_data, name='schedule_calendar_data'),  # 日历列表
    path('legalday/list/', LegalDayList.as_view(), name='legal_day_list'),  # 显示法定日期
    path('legalday/create/', LegalDayCreate.as_view(), name='legal_day_create'),  # 增加法定日期
    path('legalday/update/<int:legal_day_id>/', LegalDayUpdate.as_view(), name='legal_day_update'),  # 更新法定日期
    path('legalday/delete/<int:legal_day_id>/', LegalDayDelete.as_view(), name='legal_day_delete'),  # 删除法定日期
    path('employee/list/', EmployeeList.as_view(), name='employee_list'),  # 显示值班成员
    path('employee/create/', EmployeeCreate.as_view(), name='employee_create'),  # 增加值班成员
    path('employee/update/<int:employee_id>/', EmployeeUpdate.as_view(), name='employee_update'),  # 更新值班成员
    path('employee/delete/<int:employee_id>/', EmployeeDelete.as_view(), name='employee_delete'),  # 删除值班成员
    path('generate/date/', GenerateDateInfo.as_view(), name='create_date'),  # 生成日期数据
    path('generate/duty/', GenerateDutyInfo.as_view(), name='create_duty'),  # 生成值班日期

    path('legalday/get_last_duty/', views.get_last_duty, name='get_last_duty'),  # 生成日期数据

]