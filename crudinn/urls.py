from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.decorators import login_required

app_name = "crudinn"

urlpatterns = [
    path("register_inn", login_required(views.RegisterInn.as_view()), name="register_inn"),
    path("delete_inn", login_required(views.deleteInn), name="delete_inn"),
    path("update_inn", login_required(views.UpdateInn.as_view()), name="update_inn"),
    path("delete_image", login_required(views.deleteImage), name="delete_image"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)