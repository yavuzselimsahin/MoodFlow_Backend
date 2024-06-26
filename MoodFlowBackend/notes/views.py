from datetime import time,timezone, timedelta, datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note
from .serializers import NoteSerializer
from rest_framework.decorators import permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
# import logging

# logger = logging.getLogger(__name__)


@permission_classes([IsAuthenticated])
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mood']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        # Filter by 'mood' field
        mood = self.request.query_params.get('mood', None)
        if mood is not None:
            queryset = queryset.filter(mood=mood)


        date_str = self.request.query_params.get('date', None)
        if date_str is not None:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            target_date = timezone.make_aware(target_date, timezone=timezone.get_fixed_timezone(180))  # adjust for UTC+3

            # Create a range from 21:00 of the target date to 21:00 of the next day
            day_start = datetime.combine(target_date - timedelta(days=1), time(21, 0))
            day_end = datetime.combine(target_date, time(21, 0))

            queryset = queryset.filter(created__range=[day_start, day_end])


        # Order by 'updated' field
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            queryset = queryset.order_by('-updated')
        else:
            queryset = queryset.order_by('updated')

        return queryset

@permission_classes([IsAuthenticated])
class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mood']

    def get_queryset(self):
        queryset =  self.queryset.filter(user=self.request.user)

        mood = self.request.query_params.get('mood', None)
        if mood is not None:
            queryset = queryset.filter(mood=mood)


        date_str = self.request.query_params.get('date', None)
        if date_str is not None:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            target_date = timezone.make_aware(target_date, timezone=timezone.get_fixed_timezone(180))  # adjust for UTC+3

            # Create a range from 21:00 of the target date to 21:00 of the next day
            day_start = datetime.combine(target_date - timedelta(days=1), time(21, 0))
            day_end = datetime.combine(target_date, time(21, 0))

            queryset = queryset.filter(created__range=[day_start, day_end])



        
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            queryset = queryset.order_by('-updated')
        else:
            queryset = queryset.order_by('updated')
        
        return queryset

@api_view(['GET'])
def getRoutes(request):
    routes = [
         {
            'Endpoint': 'api/auth/user/',
            'method': 'GET, POST',
            'body': None,
            'description': 'Returns user'
        },
         {
            'Endpoint': 'api/auth/user/id',
            'method': 'GET, POST',
            'body': None,
            'description': 'Returns an array of notes or creates notes'
        },
        {
            'Endpoint': '/notes/',
            'method': 'GET, POST',
            'body': None,
            'description': 'Returns an array of notes or creates notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET, PUT, DELETE',
            'body': None,
            'description': 'Returns a single note object detail, updates a single note, or deletes a single note'
        },
         {
            'Endpoint': '/api/time_entries/',
            'method': 'GET, POST',
            'body': None,
            'description': 'Returns an array of time entries or creates a time entry'
        },
        {
            'Endpoint': '/api/time_entries/id',
            'method': 'GET, PUT, DELETE',
            'body': None,
            'description': 'Returns a specific time entry, updates a time entry, or deletes a time entry'
        },
    ]
    return Response(routes)

# @api_view(['GET'])
# def getNotes(request):
#     notes = Note.objects.all().order_by('-updated')
#     serializer = NoteSerializer(notes, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getNote(request, pk):
#     notes = Note.objects.get(id=pk)
#     serializer = NoteSerializer(notes, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def createNote(request):
#     data = request.data
#     note = Note.objects.create(
#         body=data['body']
#     )
#     serializer = NoteSerializer(note, many=False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# def updateNote(request, pk):
#     data = request.data
#     note = Note.objects.get(id=pk)
#     serializer = NoteSerializer(instance=note, data=data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# def deleteNote(request, pk):
#     note = Note.objects.get(id=pk)
#     note.delete()
#     return Response('Note was deleted!')