from django import forms
from post.models import Post
from django.forms import ClearableFileInput
class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multile':True}), required=True)
    # content = forms.FileField(widget=forms.required=True)
    caption=forms.CharField(widget=forms.Textarea(attrs={'class':'input is-mdedium'}),required=True)
    tags=forms.CharField(widget=forms.Textarea(attrs={'class':'input is-medium'}),required=True)

    class Meta:
        model=Post
        fields=('content','caption','tags')

'''
위젯은 html 입력 요소를 장고의 표현입니다. 위젯은 html 렌더링 및 get/post 사전에서 위젯에 해당하는 데이터 추출을 처리합니다. 내장 위젯에서 생성된 html은 html5구문을 사용하여 <!를 대상으로 합니다. doctype html을 참조하십시오. 예를 들어 checked='checked'의 xhtml 스타일 대신 checked와 같은 부올 속성을 사용합니다/
위젯은 양식 필드와 혼동되지 않아야 합니다. 양식 필드는 입력 유효성 검사 논리를 다루며 템플릿에서 직접 사용됩니다. 위젯은 웹페이지에서 html 양식 입력 요소의 렌더링과 원시 제출 데이터의 추출을 다룬다. 그러나 양식 필드에 위젯을 할당해야합니다

form fields
1.class field(**kwargs)
-양식 클래스를 만들때 가장 중요한 부분은 양식의 필드를 정의하는 것입니다. 각 필드에는 몇가지 다른 후크와 함께 사용자 지정 검증 논리가 있습니다.
2. field.clean(값)
-필드 클래스를 주로 사용하는 방법은 양식 클래스에 있지만 필드 클래스를 인스턴스화하고 직접 사용하여 작업 방식을 더 잘 파악할 수도 있습니다. 각 필드 인스턴스에는 단일 인수를 사용하고 django.core.exceptions를 생성하는 clean()메서드가 있습니다. validationError 예외 또는 클린 값을 반환합니다

form django import forms
f=formsEmailField()
f.clean('foo@example.com')-> food@example.com
f.clean('invalide email address')

core field arguments
각 필드 클래스 생성자는 적어도 이러한 인수를 사용합니다. 일부 필드 클래스는 필드별 인수를 추가로 사용하지만 항상 다음 인수를 수락해야 합니다

required
field.required
-기본적으로 각 필드 클래스는 값이 필요한 것으로 간주하므로 빈 값(없음 또는 빈 문자열("")을 전달하면 clean()에서 validationError예외가 발생합니다.)

from django import forms
f=forms.CharField()
f.clean('foo')-> 'foo'
f.clean('') -> validationError this field is required
f.clean(None)-> validationError - ' this field is required']

장고 폼을 이용하여 모든 입력 데이터에 대한 유효성 검사하기
-장고 폼은 파이션 딕셔너리의 유효성을 검사하는 데 최상의 도구다. 대부분의 경우 POST가 포함된 HTTP요청을 받아 유효성을 검사하는데 이용하지만 이런 경우 외에는 절대로 쓰지 말라는 제약은 없다.
-다른 프로젝트로부터 csv파일을 받아 모델에 업데이트하는 장고 앱을 가지고 있다고하자
import csv
import io
from .models import Purchase
def add_csv_pruchases(rows):
    rows=StringIO.StringIO(rows)
    records_added=0

    for row in csv.DictReader(rows,delimiter=','):
        purchase.objects.create(**row)
        records_added+=1
    return records_added

    #stringIO는 파일처럼 흉내내는 객체라고 이해하면 됩니다. 문자열 데이터를 파일로 저장한 다음 여러가지 처리를 하게 되는데 그 파일이 다시 쓰이지 않을때 유용하게 사용된다고 한다.
import io
str='text csv binary'
f=io.StringIO(str)
f.close() 

csv 파일이란 -csv데이터는 쉼표를 기준으로 항목을 구분하여 저장하는 데이터를 말하며 콤마로 규칙적으로 구분되어 있기 때문에 엑셀과 같은 프로그램으로도 읽을 수 있고 또 생성할 수도 있다. 주로 테이블 형태로 구성된 자료나 텍스트 자료를 저장할 때 사용된다.
python은 어떻게 csv 파일을 읽을 수 있을까
대부분의 프로그래밍 언어가 텍스트 파일을 읽을 수 있는 특히 파이썬에는 csv 파일을 다루기 위한 모듈이 있으며 그 중 csv.reader()또는 csv.DictReader()라는 메소드를 이용하면 매우 쉽게.csv 파일을 다룰 수 있다 
import csv #csv파일을 다루기 위한 라이브러리를 import합니다.
with open('wecode.csv') as csv_file:
    rows=csv.reader(csv_file,delimiter=',')
        for row in rows:
            print(row)
models.py 생성
class Menu.CSV(models.Model):
    menu_name=models.CharField(max_length=45)

    class Meta:
        db_tlle='menus_csv'
class Category_CSV(models.Model):
    menu.csv_models.ForeginKey('Menu', on_delete=models.CASCADE)
    

[foreginkey를 알아보기 위해서 다시
django code 구성
models.py
form django.db import models
class Post(models.Model):
    id=models.BIgAutoFIeld(help_tex=)]
'''
