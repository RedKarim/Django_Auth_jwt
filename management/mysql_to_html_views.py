from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import MySQLdb

class MysqlToHtmlView(TemplateView):
  def __init__(self):
    self.params = {
      'title':'データベースの表示',
      'heading':'データベースの表示',
      'paragraph':'データベースの表示をしてみる',
      'mysql_to_html':'mysql_to_html',
      'logout':'logout',
    }

  # <form action="" method="POST">以外のページの遷移は、「GET」メソッドになります。
  def get(self, request):
    if 'eMail' in request.session:
      # MariaDB(MySQL)へ接続パラメータ
      connection = MySQLdb.connect(
        host='db',
        user='web_weavers',
        passwd='c6SrEGYv',
        db='user_manage_dv'
      )
      # MariaDB(MySQL)へ接続
      cursor = connection.cursor()
      sql = "SELECT email , passwd FROM user_tbl"
      cursor.execute(sql)
      rows = cursor.fetchall()
      # バッファのデータをデータベースにコミットする
      self.params['rows'] = rows
      # 接続を閉じる
      connection.close()
      #  self.params['eMail']にセッション変数「request.session['eMail']」お値を保存してreturnします。
      self.params['eMail'] = request.session['eMail']
      return render(request, 'auth/login_pages/mysql_to_html.html', self.params)
    else:
      self.params = {
        'title':'データベースの表示',
        'heading':'データベースの表示',
        'paragraph':'セッションが無効です。ログインしてください。',
        'mysql':'mysql_to_html',
        'logout':'logout',
      }
      return render(request, 'auth/login_pages/mysql_to_html.html', self.params)
  
  def post(self, request):
    return render(request, 'auth/login_pages/mysql_to_html.html' , self.params)