from django.urls import path, include

from user_app import views

urlpatterns = [
    path('login/', include(([
        path('page/', views.login_page, name='page'),
        path('logic/', views.login_logic, name='logic'),
        path('jump/', views.login_jump, name='jump'),
    ], 'login'))),
    path('regist/', include(([
        path('page/', views.regist_page, name='page'),
        path('mailCheck/', views.mail_check, name='mailCheck'),
        path('pwdCheck/', views.pwd_check, name='pwdCheck'),
        path('logic/', views.regist_logic, name='logic'),
        path('captcha/', views.getCaptcha, name='captcha'),
        path('checkCaptcha/', views.checkCaptcha, name='checkCaptcha'),
        path('confirm/', views.confirm, name='comfirm'),
    ], 'regist'))),
    path('exit/', views.exit, name='exit'),
]
