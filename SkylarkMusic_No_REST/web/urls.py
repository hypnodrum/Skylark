from django.urls import path
from SkylarkMusic_No_REST.web.views import index, DashboardView, about, contact, custom_403_view, custom_404_view

urlpatterns = (
    path("", index, name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),

)

handler404 = custom_403_view
handler403 = custom_404_view
