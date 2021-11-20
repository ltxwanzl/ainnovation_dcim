from django.urls import path
from . import views
from .views import StateView, WorkflowView, WorkflowInitView, WorkflowStateView, WorkflowRunScriptView, \
    WorkflowRunScriptDetailView, WorkflowCustomNoticeView, WorkflowCustomNoticeDetailView, WorkflowDetailView, \
    WorkflowTransitionView, WorkflowCustomFieldView, WorkflowCustomFieldDetailView, WorkflowStateDetailView, \
    WorkflowTransitionDetailView, WorkflowUserAdminView

app_name = 'workflow'

urlpatterns = [
    path('', WorkflowView.as_view(),name='workflow'),
    path('user_admin', WorkflowUserAdminView.as_view(),name='user_admin'),
    path('<int:workflow_id>/init_state', WorkflowInitView.as_view(),name='workflow_init_state'),
    path('<int:workflow_id>', WorkflowDetailView.as_view(),name='workflow_detail'),
    path('<int:workflow_id>/states', WorkflowStateView.as_view(),name='workflow_states'),
    path('<int:workflow_id>/states/<int:state_id>', WorkflowStateDetailView.as_view(),name='workflow_states_id'),
    path('<int:workflow_id>/transitions', WorkflowTransitionView.as_view(),name='workflow_transitions'),
    path('<int:workflow_id>/transitions/<int:transition_id>', WorkflowTransitionDetailView.as_view(),name='workflow_transitions_id'),
    path('<int:workflow_id>/custom_fields', WorkflowCustomFieldView.as_view(),name='workflow_custom_fields'),
    path('<int:workflow_id>/custom_fields/<int:custom_field_id>', WorkflowCustomFieldDetailView.as_view(),name='workflow_custom_fields_id'),

    path('states/<int:state_id>', StateView.as_view(),name='workflows_states_id'),
    path('run_scripts', WorkflowRunScriptView.as_view(),name='run_scripts'),
    path('run_scripts/<int:run_script_id>', WorkflowRunScriptDetailView.as_view(),name='run_scripts_id'),
    path('custom_notices', WorkflowCustomNoticeView.as_view(),name='custom_notices'),
    path('custom_notices/<int:notice_id>', WorkflowCustomNoticeDetailView.as_view(),name='custom_notices_id'),

    path('workflow_manage', views.workflow_manage_view,name='workflow_manage'),
    path('workflow_manage/<int:workflow_id>', views.workflow_manage_edit_view,name='workflow_manage_id'),
    path('run_script_manage', views.run_script_manage_view,name='run_script_manage'),
    path('notice_manage', views.notice_manage_view,name='notice_manage'),
    path('workflow_flow_chart/<int:workflow_id>', views.workflow_flow_chart_view,name='workflow_flow_chart_id'),
]