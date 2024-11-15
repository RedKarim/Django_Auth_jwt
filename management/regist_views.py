from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .regist_forms import RegistEmailForm, RegistPassForm, RegistSecurityCodeForm
import MySQLdb
import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, SecurityCodeSerializer, TokenSerializer
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        connection = MySQLdb.connect(
            host='db2',
            user='root',
            passwd='team5',
            db='jmandpf_sns_db'
        )
        cursor = connection.cursor()

        # Check if email already exists
        sql = "SELECT email FROM user_tbl WHERE email = %s"
        cursor.execute(sql, (email,))
        if cursor.fetchone():
            connection.close()
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Insert new user
        sql = "INSERT INTO user_tbl (email, passwd) VALUES (%s, %s)"
        cursor.execute(sql, (email, password))
        connection.commit()

        # Generate and save security code
        security_code = ''.join([str(random.randint(0,9)) for _ in range(7)])
        sql = "UPDATE user_tbl SET security_code = %s WHERE email = %s"
        cursor.execute(sql, (security_code, email))
        connection.commit()

        # Send security code via email
        subject = 'Registration Security Code'
        message = f'Your security code is: {security_code}'
        from_email = 'hack2024team5@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        connection.close()
        return Response({"message": "Security code sent"}, status=status.HTTP_200_OK)

class VerifyRegistrationAPIView(APIView):
    def post(self, request):
        serializer = SecurityCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        security_code = serializer.validated_data['security_code']

        connection = MySQLdb.connect(
            host='db2',
            user='root',
            passwd='team5',
            db='jmandpf_sns_db'
        )
        cursor = connection.cursor()

        # Check if the security code is correct and get the user_id
        sql = "SELECT user_id FROM user_tbl WHERE email = %s AND security_code = %s"
        cursor.execute(sql, (email, security_code))
        result = cursor.fetchone()

        if not result:
            connection.close()
            return Response({"error": "Invalid security code"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = result[0]

        # Clear the security code and set auth_regist_flag
        sql = "UPDATE user_tbl SET security_code = NULL, auth_regist_flag = 1 WHERE email = %s"
        cursor.execute(sql, (email,))
        connection.commit()

        # Generate JWT token
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=14)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        connection.close()
        return Response({"token": token}, status=status.HTTP_200_OK)

#-------------------メールアドレスを処理するためのクラス-----------------------------------------------

class RegistEmailView(TemplateView):
  def __init__(self):
    self.params = {
      'title':'メールアドレス入力',
      'heading':'メールアドレス入力',
      'paragraph':'ユーザ登録',
      'form':RegistEmailForm(),
      'login_email':'login_email',
      'regist_email':'regist_email',
    }

  # <form action="" method="POST">からのデータ送信のため実行しません。
  def get(self, request):
    self.params['form'] = RegistEmailForm(request.GET)
    return render(request, 'regist/regist_email.html', self.params)

  # <form action="" method="POST">からのデータ送信のためこちらを実行します。
  def post(self, request):
    # MariaDB(MySQL)へ接続パラメータ
    connection = MySQLdb.connect(
        host='db2',
        user='root',
        passwd='team5',
        db='jmandpf_sns_db'
    )

    # MariaDB(MySQL)へ接続
    cursor = connection.cursor()

    # 送信されてきたメールアドレスと同じメールアドレスがDBに存在するかを調べるSQL文
    sql = "SELECT email FROM user_tbl WHERE email = '" + request.POST['regist_user_email'] + "'"
    # 問い合わせの実行
    rows = cursor.execute(sql)

    if rows == 1: # 同じメールアドレスが存在する場合の処理
      self.params = {
        'title':'メールアドレス入力',
        'heading':'メールアドレス入力',
        'paragraph':'ユーザ登録',
        'form':RegistEmailForm(),
        'regist_email':'regist_email'
      }
      self.params['message'] ='上記メールアドレスでは登録できません。'
      self.params['form'] = RegistEmailForm(request.POST)
      return render(request, 'regist/regist_email.html' , self.params)

    else: # 同じメールアドレスが存在しない場合の処理
      if request.POST['regist_user_email'] == '':
        self.params = {
          'title':'メールアドレス入力',
          'heading':'メールアドレス入力',
          'paragraph':'ユーザ登録',
          'form':RegistEmailForm(),
          'regist_email':'regist_email'
        }
        self.params['message'] ='入力がありません。メールアドレスを入力してください。'
        self.params['form'] = RegistEmailForm(request.POST)
        return render(request, 'regist/regist_email.html' , self.params)

      else:
        # request.session['eMail']変数のセッション名(キー)が存在するかを調べて存在しない場合は、セッション変数にメールアドレスを格納しておく
        if not 'eMail' in request.session:
        # この時点でセッションがスタートし、 request.session['eMail']にメールアドレスが格納されます。
          request.session['eMail'] = request.POST['regist_user_email']


        # 新たに行を追加してメールアドレスを保存するSQL文
        sql ="INSERT INTO user_tbl(email) VALUES('" + request.POST['regist_user_email']  + "')"
        cursor.execute(sql)
        # バッファのデータをデータベースにコミットする
        connection.commit()

        self.params = {
          'title':'パスワード入力',
          'heading':'パスワード入力',
          'paragraph':'ユーザ登録',
          'form':RegistPassForm(),
          'regist_passwd':'regist_passwd',
        }

        # 接続を閉じる
        connection.close()
        return render(request, 'regist/regist_passwd.html' , self.params)

#-------------------パスワードを処理するためのクラス-----------------------------------------------

class RegistPassView(TemplateView):
  def __init__(self):
    self.params = {
      'title':'パスワード入力',
      'heading':'パスワード入力',
      'paragraph':'ユーザ登録',
      'form':RegistPassForm(),
      'regist_passwd':'regist_passwd',
    }
  
  def get(self, request):
    self.params['form'] = RegistPassForm(request.GET)
    return render(request, 'regist/regist_passwd.html', self.params)
  
  def post(self, request):
    # MariaDB(MySQL)へ接続パラメータ
    connection = MySQLdb.connect(
        host='db2',
        user='root',
        passwd='team5',
        db='jmandpf_sns_db'
    )

    # MariaDB(MySQL)へ接続
    cursor = connection.cursor()

    if request.POST['regist_user_passwd'] == '':
      self.params = {
        'title':'パスワード入力',
        'heading':'パスワード入力',
        'paragraph':'ユーザ登録',
        'form':RegistPassForm(),
        'regist_passwd':'regist_passwd',
      }
      self.params['message'] ='入力がありません。パスワードを入力してください。'
      self.params['form'] = RegistPassForm(request.POST)
      return render(request, 'regist/regist_passwd.html' , self.params)
    else:
      # 既に登録中のメールアドレスが存在するのでその行にパスワードを保存するSQL文
      sql ="UPDATE user_tbl SET passwd = '" +  request.POST['regist_user_passwd'] + "' WHERE email = '" + request.session['eMail'] + "'"
      cursor.execute(sql)
      # バッファのデータをデータベースにコミットする
      connection.commit()

      #セキュリティコードの生成
      security_code = ''
      for i in range(1,8):
        sc = random.randint(0,9)
        security_code += str(sc)

      # セキュリティコードをsecurity_code列に書き込むSQL文
      # # 既に登録中のメールアドレスが存在するのでその行にセキュリティコードを保存するSQL文
      sql ="UPDATE user_tbl SET security_code = '" +  security_code + "' WHERE email = '" + request.session['eMail'] + "'"
      cursor.execute(sql)
      # バッファのデータをデータベースにコミットする
      connection.commit()
      
      # 登録されているメールアドレスにセキュリティーコードを送信する
      # 「subject」、「message」、「from_email」は、registPassViewクラス先頭あたりでリストまたは、辞書にしておくのがベストです。
      # そうするとプリグラムが見やすくなるし、内容を自由ね編集できます。
      # メールの件名
      subject = 'セキュリティコードの送信'
      # メールの本文
      # 「\n」は、メール文を改行させるためのエスケープシーケンスです。
      message = 'セキュリティコードは、以下になります。\n' + \
                'セキュリティコード：' + security_code
      # メールの送信者(実際は、スパムメール等を防ぐためにGmailアドレスに置き換えて送信されます。)
      from_email = 'hack2024team5@gmail.com'
      # メールの送信先
      to = request.session['eMail']
      # メールの送信
      send_mail(subject,message,from_email,[to],fail_silently=False,)

      self.params = {
        'title':'セキュリティコード入力',
        'heading':'セキュリティコード入力',
        'paragraph':'ユーザ登録',
        'form':RegistSecurityCodeForm(),
        'regist_security_code':'regist_security_code',
      }
      # 接続を閉じる
      connection.close()
      self.params['message'] = 'セキュリティコードは、' + to +'宛に送信しました。'
      return render(request, 'regist/regist_security_code.html' , self.params)

# --------------------------セキュリティコードを処理するためのクラス-----------------------------------------------------------

class RegistSecurityCodeView(TemplateView):
  def __init__(self):
    self.params = {
      'title':'セキュリティコード入力',
      'heading':'セキュリティコード入力',
      'paragraph':'ユーザ登録',
      'form':RegistSecurityCodeForm(),
      'regist_security_code':'regist_security_code',
    }
  
  def get(self, request):
    self.params['form'] = RegistSecurityCodeForm(request.GET)
    return render(request, 'regist/regist_security_code.html', self.params)
  
  def post(self, request):
    # MariaDB(MySQL)へ接続パラメータ
    connection = MySQLdb.connect(
        host='db2',
        user='root',
        passwd='team5',
        db='jmandpf_sns_db'
    )

    # MariaDB(MySQL)へ接続
    cursor = connection.cursor()

    # 送信されてきたセキュリティコードと同じセキュリティコードがDBに存在するかを調べるSQL文
    # セッション変数「request.session['eMail']」に登録されているメールアドレスを使って行(row)を特定するための条件
    sql = "SELECT * FROM user_tbl WHERE security_code = '" +  request.POST['regist_security_code'] + "' AND email = '" + request.session['eMail'] + "'"
    # 問い合わせの実行
    rows = cursor.execute(sql)
    if rows != 1:
      self.params = {
        'title':'パスワード入力',
        'heading':'パスワード入力',
        'paragraph':'ユーザ登録',
        'form':RegistSecurityCodeForm(),
        'regist_security_code':'regist_security_code',
      }
      self.params['message'] ='上記セキュリティコードでは、登録できません。'
      self.params['form'] = RegistSecurityCodeForm(request.POST)
      return render(request, 'regist/regist_security_code.html' , self.params)
    else:
      # SQL文の条件に合ったすべての行を取得する。（この場合は、1行のみになります。）
      # ここでユーザー登録を認めるので、そのユーザの行の「security_code」列を「NULL」にする。
      sql = "UPDATE user_tbl SET security_code = NULL WHERE email = '" + request.session['eMail'] + "'"
      cursor.execute(sql)
      # バッファのデータをデータベースにコミットする
      connection.commit()
      self.params = {
        'title':'ユーザ登録完了ページ',
        'heading':'登録完了ページ',
        'paragraph':'ユーザ登録が完了しました。',
        'index':'index',
        # 'regist_end_page':'regist_end_page',
      }
      # 接続を閉じる
      connection.close()
      # メールの件名
      subject = request.session['eMail'] + '様の登録情報'
      # メールの本文
      # 「\n」は、メール文を改行させるためのエスケープシーケンスです。
      message = '本サイトの会員登録ありがとうございました。\n' + \
                'メールアドレス：' +  request.session['eMail'] + '\n' + \
                'パスワード：登録時のパスワードでご利用ください。\n\n' + \
                '登録された覚えがない場合は、以下までメールをお願いいたします。\n\n' + \
                '-----------------hack2024team5@gmail.com ----------------'
      # メールの送信者(実際は、スパムメール等を防ぐためにGmailアドレスに置き換えて送信されます。)
      from_email = 'hack2024team5@gmail.com'
      # メールの送信先
      to = request.session['eMail']
      # メールの送信
      send_mail(subject,message,from_email,[to],fail_silently=False,)

      self.params['eMail'] =  request.session['eMail']
      # セッションを破棄する。
      # 登録が完了したので、セッション変数をすべて削除してセッションを破棄する。
      request.session.clear()
      return render(request, 'regist/regist_pages/regist_end_page.html' , self.params)
