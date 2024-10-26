from django.urls import path
from . import login_views , mysql_to_html_views , logout_views
from . import regist_views
from .login_views import LoginAPIView, VerifySecurityCodeAPIView

urlpatterns = [
    # path('URLのパスを指定' , '各views内のクラスを指定して実行させる' , name='「templates」内のHTMLのファイル名(拡張子は、不要)')
    # ページごとに指定が必要　
    path('', login_views.TopView.as_view(), name='index'),
    path('login_email' , login_views.LoginEmailView.as_view(), name='login_email'),
    path('login_passwd' , login_views.LoginPassView.as_view(), name='login_passwd'),
    path('login_security_code' , login_views.LoginSecurityCodeView.as_view(), name='login_security_code'),
    path('mysql_to_html' , mysql_to_html_views.MysqlToHtmlView.as_view(), name='mysql_to_html'),
    path('logout' , logout_views.MysqlToHtmlView.as_view(), name='logout'),
    path('regist_email' , regist_views.RegistEmailView.as_view(), name='regist_email'),
    path('regist_passwd' , regist_views.RegistPassView.as_view(), name='regist_passwd'),
    path('regist_security_code' , regist_views.RegistSecurityCodeView.as_view(), name='regist_security_code'),
    path('regist_end_page' , regist_views.RegistSecurityCodeView.as_view(), name='regist_end_page'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/verify/', VerifySecurityCodeAPIView.as_view(), name='api_verify'),
]