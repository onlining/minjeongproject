from django.urls import path
from stories.views import NewStory

urlpatterns = [
    path('newstory/', NewStory, name='newstory')
]