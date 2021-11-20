from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DeleteView, ListView, CreateView
from django.conf import settings
from django.db.models import Q
import calendar
import datetime
import os
import json
from .forms import LegalDayForm,EmployeeForm

from .models import Employee, Schedule, LegalDay


# 导出路径


class ScheduleIndex(View):
    """
    查询排班表数据，显示今天+前10天+后19天，总共30天的排班信息
    """
    def get(self, request):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(10)  # 时间往前10天
        end_date = today + datetime.timedelta(19)
        show_schedule = Schedule.objects.filter(date__range=(start_date, end_date)).order_by('date')  # 需要显示的值班

        # 导出功能，显示月份
        mouth1 = today.month
        year1 = today.year
        date1 = str(year1) + '-' + str(mouth1)
        date1v = '导出%s年%s月数据' % (str(year1), str(mouth1))

        mouth0 = mouth1 - 1
        if mouth0 < 1:
            year0 = year1 - 1
            mouth0 = mouth0 + 12
        else:
            year0 = year1
        date0 = str(year0) + '-' + str(mouth0)
        date0v = '导出%s年%s月数据' % (str(year0), str(mouth0))

        mouth2 = mouth1 + 1
        if mouth2 > 12:
            year2 = year1 + 1
            mouth2 = mouth2 - 12
        else:
            year2 = year1
        date2 = str(year2) + '-' + str(mouth2)
        date2v = '导出%s年%s月数据' % (str(year2), str(mouth2))

        mouth3 = mouth1 + 2
        if mouth3 > 12:
            year3 = year1 + 1
            mouth3 = mouth3 - 12
        else:
            year3 = year1
        date3 = str(year3) + '-' + str(mouth3)
        date3v = '导出%s年%s月数据' % (str(year3), str(mouth3))

        return render(request, 'schedule/schedule_list.html', locals())


class LegalDayList(ListView):
    model = LegalDay
    context_object_name = 'legal_day_list'
    template_name = 'schedule/legal_day_list.html'


class LegalDayCreate(CreateView):
    model = LegalDay
    form_class = LegalDayForm
    template_name = 'schedule/legal_day_edit.html'

    success_url = reverse_lazy('schedule:legal_day_create')


class LegalDayUpdate(UpdateView):
    model = LegalDay
    form_class = LegalDayForm
    pk_url_kwarg = 'legal_day_id'
    template_name = 'schedule/legal_day_edit.html'
    success_url = reverse_lazy('schedule:legal_day_list')


class LegalDayDelete(DeleteView):
    model = LegalDay
    pk_url_kwarg = 'legal_day_id'
    template_name = 'schedule/legal_day_del.html'
    success_url = reverse_lazy('schedule:legal_day_list')



class EmployeeList(ListView):
    model = Employee
    context_object_name = 'employee_list'
    template_name = 'schedule/employee_list.html'


class EmployeeCreate(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'schedule/employee_edit.html'

    success_url = reverse_lazy('schedule:employee_create')


class EmployeeUpdate(UpdateView):
    model = Employee
    form_class = EmployeeForm
    pk_url_kwarg = 'employee_id'
    template_name = 'schedule/employee_edit.html'
    success_url = reverse_lazy('schedule:employee_list')


class EmployeeDelete(DeleteView):
    model = Employee
    pk_url_kwarg = 'employee_id'
    template_name = 'schedule/employee_del.html'
    success_url = reverse_lazy('schedule:employee_list')


class GenerateDateInfo(View):
    """
    根据法定工作日·休息日生成数据
    """

    def get(self, request):
        last_date = Schedule.objects.order_by('-date').first()
        today = datetime.date.today()
        return render(request, 'schedule/create_date.html', locals())

    def post(self, request):
        today = datetime.date.today()
        y, m = today.year, today.month
        # 如果没有获得日期，则使用今天日期的年月
        today_date = '{}-{}'.format(y, m)
        to_one_month = request.POST.get('to_one_month', today_date)  # 2018-11
        # print(to_one_month.split('-'))
        try:
            y, m = int(to_one_month.split('-')[0]), int(to_one_month.split('-')[1])
            if y not in range(today.year, int(today.year) + 2) or m not in range(1, 13) or (y == today.year and m in range(1, today.month + 1)):
                # 年不在近2年，或者月不在1-12月，或者在今年，但日期在1-本月，则就使用本月的日期
                y, m = today.year, today.month
        except:
            y, m = today.year, today.month
        print('日期止于 %s 年 %s 月' % (str(y), str(m)))

        first_day, day_nums = calendar.monthrange(int(y), int(m))
        weekday = {1: '星期一', 2: '星期二', 3: '星期三', 4: '星期四', 5: '星期五', 6: '星期六', 7: '星期日'}
        # print('选择月份第一天：', weekday[first_day + 1])
        # print('本月一共 %s 天' % str(day_nums))

        # 根据开始标识生成，勾选后就本月1号创建，默认不勾选，从今天开始创建
        start_flag = request.POST.get('start_flag')
        if start_flag:
            start_date = datetime.date(today.year, today.month, 1)  # 从本月1号开始创建
        else:
            start_date = today
        end_date = datetime.date(int(y), int(m), calendar.monthrange(int(y), int(m))[1])
        days = (end_date - start_date).days + 1
        # print(start_date, end_date)
        print('从{}到结束日期一共{}天'.format(start_date, days))

        # 遍历这个区间的所有日期
        this_date = start_date
        while this_date <= end_date:
            # print(this_date, type(this_date), '周内' if this_date.isoweekday() < 6 else '周末')

            # 判断工作日，和法定工作日（休息日变工作日的）
            if (this_date.isoweekday() <= 5 and not LegalDay.objects.filter(date=this_date, legal_type=0)) or LegalDay.objects.filter(date=this_date, legal_type=1):
                # print('工作日：', this_date)

                if Schedule.objects.filter(date=this_date):
                    # 如果存在当前日期数据，就进行更新
                    schedule = Schedule.objects.get(date=this_date)
                    schedule.is_workday = True
                    schedule.duty_type = 1
                    schedule.staff = ''  # 更新时清空值班人员
                    schedule.real_staff = ''
                    schedule.save()
                else:
                    Schedule.objects.create(
                        date=this_date,
                        is_workday=True,
                        duty_type=1
                    )

            # 判断休息日，和法定休息日（工作日变休息日的）
            elif (this_date.isoweekday() >= 6 and not LegalDay.objects.filter(date=this_date, legal_type=1)) or LegalDay.objects.filter(date=this_date, legal_type=0):
                # print('休息日：', this_date)

                if Schedule.objects.filter(date=this_date):
                    # 存在即更新更新
                    schedule = Schedule.objects.get(date=this_date)
                    schedule.staff = ''  # 更新时清空值班人员
                    schedule.real_staff = ''
                else:
                    # 不存在即创建对象
                    schedule = Schedule()
                    schedule.date = this_date

                schedule.is_workday = False

                if this_date.isoweekday() == 6 and not LegalDay.objects.filter(date=this_date):
                    # 为周六，且不在法定工作日和法定休息日中，就要加班了，调休半天（坑）
                    schedule.duty_type = 2
                else:
                    # 真正休息的时候
                    schedule.duty_type = 0
                schedule.save()

            this_date += datetime.timedelta(days=1)

        return redirect(reverse('schedule:create_date'))



def generate_duty_data(last_duty_name, duty_type, start_date, end_date):
    print('正在生成类型为{}值班信息'.format(duty_type))
    all_employee = Employee.objects.filter(available=True)
    # 生成默认的顺序{name:{'default_order': num}, ...}
    employee_order = dict()
    for employee in all_employee:
        employee_order[employee.name] = {}
        employee_order[employee.name]['default_order'] = employee.num
    # print(employee_order)

    # 将选择的last_duty_name的新顺序变为值班成员的数量，也就是排班排到最后一位，得到新顺序和默认顺序的差值
    employee_order[last_duty_name]['new_order'] = all_employee.count()
    diff_num = all_employee.count() - employee_order[last_duty_name]['default_order']
    print('顺序差值：', diff_num)

    # 在默认的顺序字典中增加新的顺序
    new_employee_order = {}
    for name, item in employee_order.items():
        employee_order[name]['new_order'] = employee_order[name]['default_order'] + diff_num
        if employee_order[name]['new_order'] > all_employee.count():
            employee_order[name]['new_order'] -= all_employee.count()
        # 根据这个新字典顺便生成新顺序：名字的对应关系
        new_employee_order[employee_order[name]['new_order']] = name
    print(employee_order)
    print(new_employee_order)  # {new_order: name, ...}

    # 待排序的值班进行排序
    next_duty = Schedule.objects.filter(duty_type=duty_type, date__gte=start_date, date__lte=end_date).order_by('date')

    # 更新从选定日期到生成的最后日期的值班表
    i = 0
    print(next_duty)
    for duty in next_duty:
        # print(duty, i % all_employee.count() + 1)
        duty.staff = new_employee_order[i % all_employee.count() + 1]
        duty.real_staff = ''
        duty.save()
        i += 1


class GenerateDutyInfo(View):
    """
    生成值班表，填充值班人员
    """

    def get(self, request):
        # 获取上次值班安排到的日期，也就是安排了值班人员的最后一个日期
        last_schedule = Schedule.objects.exclude(Q(staff__isnull=True) | Q(staff='')).order_by('date')

        all_employee = Employee.objects.filter(available=True)
        today = datetime.date.today()  # 可选日期开始
        if Schedule.objects.all():  # 如果存在值班表
            end_date = Schedule.objects.order_by('-date').first().date  # 可选日期结束
        else:
            end_date = today
        last_night_duty = last_schedule.filter(duty_type=1).last()  # 获取上次晚班的数据
        last_weekend_duty = last_schedule.filter(duty_type=2).last()  # 获取上次周末值班数据

        return render(request, 'schedule/create_duty.html', locals())

    def post(self, request):
        choose_date = request.POST.get('choose_date')
        end_date = Schedule.objects.order_by('-date').first().date  # 排班结束日期
        this_date = datetime.date.today()  # 默认为今天的日期
        if choose_date:
            yy, mm, dd = choose_date.split('-')
            this_date = datetime.date(int(yy), int(mm), int(dd))  # 获取选择的日期

        # 获取选择的上次值班人员id
        last_night_duty_id = request.POST.get('last_night_duty')
        last_weekend_duty_id = request.POST.get('last_weekend_duty')

        # 获取值班表中该日期数据信息，以日期从小到大排序
        previous_night_duty = Schedule.objects.filter(duty_type=1, date__lt=this_date).order_by('date')
        previous_weekend_duty = Schedule.objects.filter(duty_type=2, date__lt=this_date).order_by('date')

        # 值班成员中的第一个
        all_employee = Employee.objects.filter(available=True)

        # 如果选择了上次晚班值班人员
        if last_night_duty_id:
            last_night_duty_name, last_night_duty_num = Employee.objects.filter(id=last_night_duty_id).values_list('name', 'num').first()
        else:
            # 默认情况下为值班成员第一个
            last_night_duty_name = all_employee.first().name

            # 如果值班表中已安排过晚班，从中获取上次值班人员，exclude表示得到staff中有值得数据
            all_previous_night_duty = previous_night_duty.exclude(Q(staff__isnull=True) & Q(staff=''))

            if all_previous_night_duty:
                # 得到上次值班人员，要考虑到值班成员列表中消失的名字
                for previous_night_duty in all_previous_night_duty.reverse():  # 倒序，日期最新的在前
                    # print(previous_night_duty)
                    if all_employee.filter(name=previous_night_duty.staff):
                        last_night_duty_name = previous_night_duty.staff  # 获取值班表名字在成员中的一个，获取到后停止
                        break
        print('上次晚上值班人员：', last_night_duty_name)
        generate_duty_data(last_duty_name=last_night_duty_name, duty_type=1, start_date=this_date, end_date=end_date)

        # ---------------------------------------------------------
        # 如果选择了上次周末值班人员
        if last_weekend_duty_id:
            last_weekend_duty_name, last_weekend_duty_num = Employee.objects.filter(id=last_weekend_duty_id).values_list('name', 'num').first()
        else:
            # 默认情况下为值班成员第一个
            last_weekend_duty_name = all_employee.first().name

            # 如果值班表中已安排过周末值班，从中获取上次值班人员，exclude表示得到staff中有值得数据
            all_previous_weekend_duty = previous_weekend_duty.exclude(Q(staff__isnull=True) & Q(staff=''))

            if all_previous_weekend_duty:
                # 得到上次值班人员，要考虑到值班成员列表中消失的名字
                for previous_weekend_duty in all_previous_weekend_duty.reverse():  # 倒序，日期最新的在前
                    # print(previous_weekend_duty)
                    if all_employee.filter(name=previous_weekend_duty.staff):
                        last_weekend_duty_name = previous_weekend_duty.staff  # 获取值班表名字在成员中的一个，获取到后停止
                        break
        print('上次周末值班人员：', last_weekend_duty_name)
        generate_duty_data(last_duty_name=last_weekend_duty_name, duty_type=2, start_date=this_date, end_date=end_date)

        return redirect(reverse('schedule:create_duty'))



def get_last_duty(request):
    """
    根据给定的一个日期，从值班表中得到这个日期之前的值班人员信息
    :param reqeust:
    :return:
    """
    yy, mm, dd = request.GET.get('this_date').split('-')
    this_date = datetime.date(int(yy), int(mm), int(dd))

    # 获取值班表中日期数据信息，以日期从大到小排序
    previous_night_duty = Schedule.objects.filter(duty_type=1, date__lt=this_date).order_by('-date')
    previous_weekend_duty = Schedule.objects.filter(duty_type=2, date__lt=this_date).order_by('-date')

    all_employee = Employee.objects.filter(available=True)

    last_night_duty_name = last_weekend_duty_name = all_employee.last().name  # 未安排过值班的，默认显示值班成员最后一个，然后从第一人开始排

    for night_duty in previous_night_duty:
        if all_employee.filter(name=night_duty.staff):
            last_night_duty_name = night_duty.staff  # 获取值班表名字在成员中的一个，获取到后停止
            break

    for weekend_duty in previous_weekend_duty:
        if all_employee.filter(name=weekend_duty.staff):
            last_weekend_duty_name = weekend_duty.staff  # 获取值班表名字在成员中的一个，获取到后停止
            break

    last_duty = dict()
    last_duty['last_night_duty_name'] = last_night_duty_name
    last_duty['last_weekend_duty_name'] = last_weekend_duty_name
    return HttpResponse(json.dumps(last_duty))



#@simple_permission_required(permission='it_sys_user')
def renew_staff(request):
    new_staff = request.POST.get('new_staff')
    staff_flag = request.POST.get('staff_flag')
    date = request.POST.get('date')

    schedule_data = Schedule.objects.filter(date=date).first()
    if staff_flag == "staff":
        schedule_data.staff = new_staff
    elif staff_flag == "real_staff":
        schedule_data.real_staff = new_staff
    schedule_data.save()
    return HttpResponse(json.dumps({}))



# 日历视图中显示值班表
#@simple_permission_required(permission='it_sys_user')
def schedule_calendar(request):
    all_employee = Employee.objects.filter(available=True)
    return render(request, 'schedule/schedule_calendar.html', {"all_employee": all_employee})


# 提供日历视图数据
#@simple_permission_required(permission='it_sys_user')
def schedule_calendar_data(request):
    data = []
    today = datetime.date.today()
    start_date = today - datetime.timedelta(20)  # 时间往前20天
    end_date = today + datetime.timedelta(39)
    schedules = Schedule.objects.filter(date__range=(start_date, end_date)).order_by('date')  # 需要显示的值班
    for schedule in schedules:
        date_str = str(schedule.date)
        if schedule.real_staff:
            data.append({"title": "更换值班：" + schedule.real_staff,
                         "start": date_str + " 18:00",
                         "end": date_str + " 21:00",
                         "allDay": True})

        if schedule.duty_type == 1:  # 晚上值班
            data.append({"title": "今日值班：" + schedule.staff,
                         "start": date_str + " 18:00",
                         "end": date_str + " 21:00",
                         "allDay": True})
        elif schedule.duty_type == 2:  # 周末值班
            data.append({"title": "周末值班：" + schedule.staff,
                         "backgroundColor": "#23b7e5",
                         "start": date_str})
    return HttpResponse(json.dumps(data))