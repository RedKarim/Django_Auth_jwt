from django import forms


#このフォームは専門学校のオープンキャンパスの申込フォームです。 エレメントは以下にあります。

class RegistEmailForm(forms.Form):
    regist_user_email = forms.CharField(label='メールアドレス' , required=False , widget =forms.TextInput(attrs={'placeholder':'メールアドレスを入力してください。' , 'size':'30'}))

class RegistPassForm(forms.Form):
    regist_user_passwd = forms.CharField(label='パスワード' , required=False , widget =forms.PasswordInput(attrs={'placeholder':'パスワードを入力してください。' , 'size':'30'}))
    # regist_user_email = forms.CharField(label='パスワード' , required=False , widget =forms.TextInput(attrs={'placeholder':'メールアドレスを入力してください。' , 'size':'30'}))

class RegistSecurityCodeForm(forms.Form):
    regist_security_code = forms.CharField(label='セキュリティコード' , required=False , widget =forms.TextInput(attrs={'placeholder':'セキュリティコードを入力してください。' , 'size':'30'}))