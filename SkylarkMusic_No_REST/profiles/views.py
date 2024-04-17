from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import views as auth_views, get_user_model, login
from SkylarkMusic_No_REST.profiles.forms import CustomAuthenticationForm, CustomUserCreationForm, EditProfileForm
from SkylarkMusic_No_REST.profiles.models import SkylarkUser


class LoginUserView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('index')


class CreateProfileView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'profiles/create_profile.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a profile instance for the newly created user
        profile = SkylarkUser(user=self.object)
        profile.save()
        login(self.request, form.instance)
        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profiles/details_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "profiles/edit_profile.html"
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "profiles/profile_delete.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return self.request.user


class LogoutUserView(auth_views.LogoutView):
    def get_success_url(self):
        return reverse_lazy('index')
