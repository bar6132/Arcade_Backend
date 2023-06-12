from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import paginators
from django.contrib.auth.models import User  


urlpatterns = [
    path('signup', views.signup),
    path('obtain-token', obtain_auth_token),
    path('users/<int:pk>/inbox/', views.user_inbox, name='inbox'),
    path('get-user-data', views.get_user_data),
    path('getuser/<int:pk>', views.get_user),
    path('get-all-users', views.manage_users),
    path('manage-users/', views.manage_users),
    path('my_profile/<int:pk>', views.get_profile),
    path('uploader/<int:pk>', views.uploader_data),
    path('games/', views.games),
    path('games/<int:pk>', views.games),
    path('game/', views.game),
    path('game/<int:pk>', views.game),
    path('inbox/', views.inbox),
    path('inbox/<int:pk>', views.inbox),
    path('page', paginators.GamePagination.as_view()),
    path('serve_game_pagination', paginators.serve_game_pagination)
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
