from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls), # 管理システムへのパス
    path('', include('management.urls')), # 「management」アプリケーション内の「urls.py」の読み込み
]
