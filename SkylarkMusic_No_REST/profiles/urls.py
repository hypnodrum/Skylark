from django.urls import path
from SkylarkMusic_No_REST.profiles.views import CreateProfileView, LoginUserView, LogoutUserView, EditProfileView, \
    ProfileDetailView, DeleteProfileView

urlpatterns = [
    path("create/", CreateProfileView.as_view(), name="create_profile"),
    path("login/", LoginUserView.as_view(template_name="profiles/login.html"), name="login"),
    path("details/", ProfileDetailView.as_view(), name="details_profile"),
    path("edit/", EditProfileView.as_view(), name="edit_profile"),
    path("delete/", DeleteProfileView.as_view(), name="delete_profile"),
    path("logout/", LogoutUserView.as_view(), name="logout"),

]