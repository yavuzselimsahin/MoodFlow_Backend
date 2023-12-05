from django.urls import include, path
from .views import TimeEntryListCreateView, TimeEntryDetailAPIView, pause_time_entry, continue_time_entry

urlpatterns = [
    path('time_entries/', TimeEntryListCreateView.as_view(), name='time-entry-list'),
    path('time_entries/<str:pk>/', TimeEntryDetailAPIView.as_view(), name='time-entry-detail'),
    path('time_entries/<str:pk>/pause/', pause_time_entry, name='time-entry-pause'),
    path('time_entries/<str:pk>/continue/', continue_time_entry, name='time-entry-continue'),
]