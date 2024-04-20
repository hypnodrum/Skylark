from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import FileResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from .forms import CreateTrackForm
from .models import Track


class CatalogueView(LoginRequiredMixin, ListView):
    model = Track
    template_name = 'tracks/catalogue.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        tracks = super().get_queryset().filter(user=self.request.user).order_by('id')
        return tracks


class CreateTrackView(LoginRequiredMixin, CreateView):
    model = Track
    form_class = CreateTrackForm
    template_name = 'tracks/upload_track.html'
    success_url = reverse_lazy('catalogue')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        track_id = self.object.id
        return reverse_lazy('catalogue', kwargs={'pk': track_id})


class TrackDetailView(LoginRequiredMixin, DetailView):
    model = Track
    template_name = 'tracks/track_details.html'
    context_object_name = 'track'

    def dispatch(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user != track.user:
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['share_url'] = self.request.build_absolute_uri()
        return context


class TrackEditView(LoginRequiredMixin, UpdateView):
    model = Track
    template_name = 'tracks/edit_track.html'
    fields = ['title', 'file', 'private', 'cover', 'genre', 'album', 'link_of_author', 'license']
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        track = self.get_object()
        if request.user != track.user:
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)


class TrackDeleteView(DeleteView):
    model = Track
    template_name = "tracks/delete_track.html"
    success_url = reverse_lazy("index")


def get_track(request, pk):
    track = get_object_or_404(Track, pk=pk)

    if request.user.is_authenticated and request.user == track.user:
        track.increase_play_count()  # Increase play count when the track is accessed
        return FileResponse(open(track.file.path, 'rb'), content_type='audio/mpeg')
    else:
        return HttpResponseForbidden("You do not have permission to access this track.")


def get_all_track(request, pk):
    track = get_object_or_404(Track, pk=pk)

    if request.user == track.user or not track.private:
        track.increase_play_count()  # Increase play count when the track is accessed
        return FileResponse(open(track.file.path, 'rb'), content_type='audio/mpeg')
    else:
        # If the track is private and the user is not the owner, return a 403 Forbidden response
        return HttpResponseForbidden("You are not authorized to access this track.")


def download_track(request, pk):
    track = get_object_or_404(Track, pk=pk, private=False)
    track.increase_download_count()
    return FileResponse(open(track.file.path, 'rb'), content_type='audio/mpeg')


def increase_likes(request, pk):
    track = get_object_or_404(Track, pk=pk)

    # Check if the user has already liked the track
    if request.user in track.user_of_likes.all():
        messages.warning(request, "You have already liked this track.")
    else:
        track.increase_likes_count(request.user)

    return redirect('dashboard')


def search_view(request):
    if request.user.is_authenticated:
        if 'query' in request.GET:
            query = request.GET['query']
            results = Track.objects.filter(title__icontains=query, private=False).order_by('-id')
            return render(request, 'web/search_results.html', {'results': results})
        else:
            raise Http404("No search query provided.")
    else:
        return render(request, '403.html', status=403)
