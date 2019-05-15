from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:movie_pk>/edit/<int:score_pk>/', views.edit_score, name="edit_score"),
    path('<int:user_pk>/',views.profile,name="profile"),
    path('<int:user_pk>/follow/',views.follow,name="follow"),
    path('<int:user_pk>/create_profile/', views.create_profile, name="create_profile"),

    # 관리자 모드 -----------------------------------
    path('test/algorithm_clear/',views.algorithm_clear, name="test_algorithm_clear"),
    path('test/make_bot/',views.make_bot, name="test_make_bot"),
    path('test/make_bot_score/',views.make_bot_score, name="make_bot_score"),
    path('test/search_sns/<int:num>/',views.search_sns, name="search_sns"),
]