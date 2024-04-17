from django.urls import path
from SkylarkMusic_No_REST.audio_library.views import CreateTrackView, CatalogueView, TrackDetailView, get_track, \
    download_track, increase_likes, get_all_track, TrackDeleteView, TrackEditView, search_view

urlpatterns = [
    path("track/<int:pk>/", CatalogueView.as_view(), name="catalogue"),
    path("upload/<int:pk>/", CreateTrackView.as_view(), name="upload_track"),
    path("track_details/<int:pk>/", TrackDetailView.as_view(), name="track_details"),
    path("get_track/<int:pk>/", get_track, name="get_track"),
    path("get_all_track/<int:pk>/", get_all_track, name="get_all_track"),
    path("download_track/<int:pk>/", download_track, name="download_track"),
    path('increase_likes/<int:pk>/', increase_likes, name='increase_likes'),
    path('edit/<int:pk>/', TrackEditView.as_view(), name='edit_track'),
    path('delete/<int:pk>/', TrackDeleteView.as_view(), name='delete_track'),
    path('search/', search_view, name='search'),
]
