from django.contrib import admin
from authy.models import Profile
# Register your models here.

admin.site.register(Profile)


'''
특정 모델클래스를 admin에 등록하면, 해당 모델을 GUI 환경에서 관리 가능
admin.py 파일 내에 원하는 모델을 import, register, unregister진행
admin.site.unregister 기능은 기본 유저 모델의 등록을 해제하는 등의 용도로 사용
admin.Modeladmin 상속을 통해 커스터마이징이 가능하다
class postadmin(admin.modeladmin):list_display=['id','title','created_At','updated_At']
admin.site.register(post,postadmin)으로 가능
장식자 형태로 등록이 가능하다

장식자 등록법
-장식자 형태로 등록이 가능하다
from django.contrib import admin
from blog.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','content']
    list_display_links=['id','title']
    
modeladmin옵션
1. list_display: admin 목록에 보여질 필드목록
2. list_display_links: 목록 내에서 링크로 지정할 필드 목록(이를 지정하지 않으면 첫번째 필드에만 링크만 적용)
3. list_editable : 목록 상에서 수정할 필드 목록
4. list_per_page: 페이지 별로 보여질 최대 갯수(디폴트:100)
5. list_filter 필터 옵션을 제공할 필드 목록
6. actions: 목록에서 수행할 action 목록
7. fields: add/change폼에 노출할 필드 목록
8. fieldset:add/change 폼에 노출할 필드 목록(fieldset)
9. formfield_overrides: 특정 form field에 대한 속성 재정의 
10. form : 디폴트로 모델 클래스에 대한 form class 지정


1.list_display 옵션
-모델 인스턴스 필드명/속성명/함수명 뿐만 아니라 modeladmin 내 멤버 함수도 지정 가능
-외래키를 지정한다면 관련 objectd의 __str__()값이 노출
-manytomanyfield 미지원

from django.contrib import admin
from django.utils.safestring import mark_safe
form .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','content_size]
    
    def content_size(self,post):
        return mark_safe('<u>{}<u>글자',format(len(post.content)))
    content_size.short_description='글자수'

2.list_display_links 옵션
admin 사이트에서 세부 항목으로 들어가는 link를 어디에 걸어줄 지 선택할 수 있습니다. 기본적으로는 가장 앞에 오는 field에 링크를 걸게 되는데 예시의 경우, id에 있는 것보다는 title에 있는게 더 자연스러울 거 같아서 title에 걸어주었습니다

@admin.register(Post)
class MyAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'short_content', 'is_published' ]
  list_display_links = ['title']

3. list_editable 옵션
    '''

