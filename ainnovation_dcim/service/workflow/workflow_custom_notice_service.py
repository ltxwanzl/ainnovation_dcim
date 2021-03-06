import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from workflow.models import CustomNotice
from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowCustomNoticeService(BaseService):
    """
    工作流通知服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_notice_list(cls, query_value: str, page: int, per_page: int)->tuple:
        """
        获取通知列表
        :param query_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value) | Q(description__contains=query_value)

        custom_notice_querset = CustomNotice.objects.filter(query_params).order_by('id')
        paginator = Paginator(custom_notice_querset, per_page)
        try:
            custom_notice_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            custom_notice_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            custom_notice_result_paginator = paginator.page(paginator.num_pages)
        custom_notice_result_object_list = custom_notice_result_paginator.object_list
        custom_notice_result_restful_list = []
        for custom_notice_result_object in custom_notice_result_object_list:
            custom_notice_result_restful_list.append(custom_notice_result_object.get_dict())
        return custom_notice_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def add_custom_notice(cls, name: str, description: str, hook_url: str, hook_token: str, creator: str)->tuple:
        """
        新增自定义通知记录
        :param name:
        :param description:
        :param hook_url:
        :param hook_token:
        :param creator:
        :return:
        """
        notice_obj = CustomNotice(name=name, description=description, hook_url=hook_url, hook_token=hook_token,
                                  creator=creator)
        notice_obj.save()
        return True, dict(notice_id=notice_obj.id)

    @classmethod
    @auto_log
    def update_custom_notice(cls, custom_notice_id: int, name: str, description: str, hook_url: str, hook_token: str)->tuple:
        """
        更新自定义通知
        :param custom_notice_id:
        :param name:
        :param description:
        :param hook_url:
        :param hook_token:
        :return:
        """
        custom_notice_obj = CustomNotice.objects.filter(id=custom_notice_id, is_deleted=0)
        if custom_notice_obj:
            custom_notice_obj.update(name=name, description=description, hook_url=hook_url, hook_token=hook_token)
        else:
            custom_notice_obj.update(name=name, description=description, hook_url=hook_url, hook_token=hook_token)
        return True, ''

    @classmethod
    @auto_log
    def del_custom_notice(cls, custom_notice_id: int)->tuple:
        """
        删除脚本
        :id: 
        :return:
        """
        custom_notice_obj = CustomNotice.objects.filter(id=custom_notice_id, is_deleted=0)
        if custom_notice_obj:
            custom_notice_obj.update(is_deleted=True)
            return True, ''
        else:
            return False, 'the record is not exist or has been deleted'


workflow_custom_notice_service_ins = WorkflowCustomNoticeService()
