from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from SkylarkMusic_No_REST.audio_library.models import Track


def index(request):
    logged_in_user = request.user

    if logged_in_user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, "web/index.html")


def about(request):
    return render(request, "web/about.html")


def contact(request):
    return render(request, "web/contact.html")


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)


class DashboardView(LoginRequiredMixin, ListView):
    model = Track
    template_name = 'web/dashboard.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        tracks = super().get_queryset().filter(private=False).order_by('-id')
        return tracks
