from django.urls import path

from manage_app import views

urlpatterns = [
    path('index/', views.index_page, name='index'),
    path('addPage/', views.add_page, name='addPage'),
    path('addLogic/', views.add_logic, name='addLogic'),
    path('dzlistPage/', views.dzlist_page, name='dzlistPage'),
    path('listPage/', views.list_page, name='listPage'),
    path('splbPage/', views.splb_page, name='splbPage'),
    path('testPage/', views.test_page, name='testPage'),
    path('zjspPage/', views.zjsp_page, name='zjspPage'),
    path('zjspLogic/', views.zisp_logic, name='zjspLogic'),
    path('zjzlbPage/', views.zjzlb_page, name='zjzlbPage'),
    path('zjzlbLogic/', views.zjzlb_logic, name='zjzlbLogic'),
    path('delOne/', views.del_one, name='delOne'),
    path('delMany/', views.del_many, name='delMany'),
]