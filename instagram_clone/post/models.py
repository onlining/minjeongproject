from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

from notifications.models import Notification
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title=models.CharField(max_length=75, verbose_name='Tag')
    #verbose_name? - admin 페이지에서 조회할때 필드명 대신 알아보기 쉬운 단어로 지정하는 것
    slug=models.SlugField(null=False, unique=True)
    #slugfield - 일반적으로 이미 얻은 데이터를 사용하여 유효한 url을 생성하는 방법 예를 들어 slug는 기사 제목을 사용하여 url을 생성한다. 수동으로 설정하는 대신 제목이 주어지면 함수를 통해서 슬러그를 생성하는게 좋다. 

    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'

    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])

    ''' 어드민 패널을 만지다 보면 내가 등록한 모델 이름을 장고 어드민이 알아서 복수로 만들어주는 것을 알 수 있다. 그럴떄 가끔 -y로 끝나는 단어의 끝에도 그냥 s를 붙이는 경우가 있는데 이때 메타 클래스의 verbose_name을 이용해서 바꿔줄 수 있다.'''

   # def get_absolute_url(self):
    #    return reverse('tags',args=[self.slug])
    #viewname과 args 및 kwargs를 인자로 받아 url string을 반환한다. 

    #get_absolute_url는 reverse함수를 통해 모델의 개별 데이터 url을 문자열로 반환합니다
    '''
    urls.py에 정의한 namespace(app_name)=blog,, name=blog_detail입니다.
    blog_detail(blog//)은 인수가 있는 url이기 때문에 kwargs로 pk 값을 넘겨주는건
    - def get_absolute_url(self):
        return reverse('blog:blog_detail',kwargs={'pk':self.id})
    수 많은 페이지에 url이 하드코딩 되어 있고, url을 변경해야 한다면 하나씩 url을 찾고 수정해야 하는 번거로움이 발생합니다
    '''

    def __str__(self):
        return self.title

    
    '''
    이미 확보된 데이터로부터 유효한 url 만드는 방법
    from django.utils.text import slugify
    
    class Article(models.Model):
        title=models.charfield(max_length=100)
        slug=models.slugfield(unique=true)

        def save(self, *args, **kwargs):
            self.slug=slugify(self.title)
            super(Article,self).save(*Args, **kwargs)
    >>> test=Article.objects.create(title='django model field list")
    >>> test.save()
    >>> test.slug -> "django-model-field-list"        
    '''
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
    file = models.FileField(upload_to=user_directory_path)
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.ManyToManyField(PostFileContent, related_name='contents')
    caption=models.TextField(max_length=1500,verbose_name='Caption')
    posted=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag, related_name='tags')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails',args=[str(self.id)])


class Follow(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='follower')
    following=models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='following')
#cascade - foreignkeyfield를 포함하는 모델 인스턴스(row)도 같이 삭제한다
    def user_follow(sender, instance, *args, **kwargs):
        follow=instance
        sender = follow.follower
        following = follow.following
        
        notify = Notification(sender = sender, user=following, notification_type=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow=instance
        sender= follow.follower
        following = follow.following

        notify=Notification.objects.filter(sender=sender,user=following, notification_type=3)
        notify.delete()

class Stream(models.Model):
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date=models.DateTimeField()
    
    def add_post(sender, instance, *args, **kwargs):
        post=instance
        user=post.user
        followers=Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()
class Likes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    
    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify= Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like=instance
        post=like.post
        sender=like.user
        notify = Notification.objects.filter(post=post,sender=sender, notification_type=1)
        notify.delete()

post_save.connect(Stream.add_post, sender=Post)

#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)

#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)