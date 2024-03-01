from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.decorators import login_required

app_name = "registration"

urlpatterns = [
    path("", views.InitView.as_view(), name="init"),
    path("main", login_required(views.IndexView.as_view()), name="index"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', login_required(views.LogoutView), name="logout"),
    path('<int:pk>/update/', login_required(views.UserUpdateView.as_view()), name='update'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)