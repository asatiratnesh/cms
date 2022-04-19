from django.urls import path
from .views import *


urlpatterns = [
    path('test/', APIView1.as_view(), name="test"),
    path('register/', UserList.as_view(), name='auth_register'), 
    path('content/', ContentItemList.as_view(), name='content_item'),
    path('content/<int:pk>', ContentItemList.as_view(), name='single_content_item'),
    path('content-search', ContentListView.as_view(), name='single_content_item')

]
