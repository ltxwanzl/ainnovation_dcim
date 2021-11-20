from django.urls import path

from . import views
from .views import TicketListView, TicketView, TicketTransition, TicketFlowlog, TicketFlowStep, TicketState, \
    TicketsStates, TicketAccept, TicketDeliver, TicketAddNode, \
    TicketAddNodeEnd, TicketField, TicketScriptRetry, TicketComment, TicketHookCallBack, TicketParticipantInfo, \
    TicketClose, TicketsNumStatistics, TicketRetreat

app_name = 'ticket'

urlpatterns = [
    path('', TicketListView.as_view(),name='ticket'),
    path('<int:ticket_id>', TicketView.as_view(),name='ticket_detail'),
    path('<int:ticket_id>/transitions', TicketTransition.as_view(),name='ticket_transitions'),
    path('<int:ticket_id>/flowlogs', TicketFlowlog.as_view(),name='ticket_flowlogs'),
    path('<int:ticket_id>/flowsteps', TicketFlowStep.as_view(),name='ticket_flowsteps'),
    path('<int:ticket_id>/state', TicketState.as_view(),name='ticket_state'),
    path('<int:ticket_id>/fields', TicketField.as_view(),name='ticket_fields'),
    path('<int:ticket_id>/accept', TicketAccept.as_view(),name='ticket_accept'),
    path('<int:ticket_id>/deliver', TicketDeliver.as_view(),name='ticket_deliver'),
    path('<int:ticket_id>/add_node', TicketAddNode.as_view(),name='ticket_add_node'),
    path('<int:ticket_id>/add_node_end', TicketAddNodeEnd.as_view(),name='ticket_add_node_end'),
    path('<int:ticket_id>/retry_script', TicketScriptRetry.as_view(),name='ticket_retry_script'),
    path('<int:ticket_id>/comments', TicketComment.as_view(),name='ticket_comments'),
    path('<int:ticket_id>/hook_call_back', TicketHookCallBack.as_view(),name='ticket_hook_call_back'),
    path('<int:ticket_id>/participant_info', TicketParticipantInfo.as_view(),name='ticket_participant_info'),
    path('<int:ticket_id>/close', TicketClose.as_view(),name='ticket_close'),
    path('<int:ticket_id>/retreat', TicketRetreat.as_view(),name='ticket_retreat'),
    path('states', TicketsStates.as_view(),name='ticket_states'),  # 批量获取工单状态
    path('num_statistics', TicketsNumStatistics.as_view(),name='ticket_num_statistics'),  # 批量获取工单状态
    path('ticket_manage', views.ticket_manage_view,name='ticket_manage'),
    path('ticket_manage/<int:ticket_id>', views.ticket_manage_detail_view,name='ticket_manage'),
]
