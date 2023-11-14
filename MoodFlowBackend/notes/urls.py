from django.urls import path
from .views import NoteListCreateView, getRoutes, NoteDetailAPIView

urlpatterns = [
    path('', getRoutes, name='routes'),
    path('notes/', NoteListCreateView.as_view(), name='note-list'),
    path('notes/<str:pk>/', NoteDetailAPIView.as_view(), name='note-deail'),
]


