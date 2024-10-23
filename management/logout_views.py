from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

class MysqlToHtmlView(TemplateView):
  def __init__(self):
    self.params = {
      'title':'ログアウト',
      'heading':'ログアウト',
      'paragraph':'ログアウトします。',
    }

  # <form action="" method="POST">以外のページの遷移は、「GET」メソッドになります。
  def get(self, request):
    # セッション変数にセッション名（キー）が存在するかを調べる。
    if 'eMail' in request.session:
      # セッション変数をすべて削除してセッションを破棄する。
      request.session.clear()
      self.params = {
        'title':'ログアウト',
        'heading':'ログアウト',
        'paragraph':'ログアウトしました。',
      }
      return render(request, 'auth/login_pages/logout.html', self.params)
    else:
      self.params = {
        'title':'ログアウト',
        'heading':'ログアウト',
        'paragraph':'セッションが無効です。ログインしてください。',
        'logout':'logout',
      }
      return render(request, 'auth/login_pages/logout.html', self.params)
  
  def post(self, request):
    return render(request, 'auth/login_pages/logout.html' , self.params)