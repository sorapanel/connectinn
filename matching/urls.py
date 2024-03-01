from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.decorators import login_required

app_name = "matching"

urlpatterns = [
    path("search_inn", login_required(views.SearchInn.as_view()), name="search_inn"),
    path("apply_inn", login_required(views.ApplyInn.as_view()), name="apply_inn"),
    path("permit_apply", login_required(views.permitApply), name="permit_apply"),
    path("applied_inn", login_required(views.AppliedInn.as_view()), name="applied_inn"),
    path("cancel_apply", login_required(views.cancelApply), name="cancel_apply"),
    path("auth_apply", login_required(views.AuthenticatedApply.as_view()), name="auth_apply"),
    path("chat_home", login_required(views.Chat.as_view()), name="chat_home"),
    path("chat", login_required(views.ChatDetail.as_view()), name="chat"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)