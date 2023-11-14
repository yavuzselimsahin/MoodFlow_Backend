from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Note
from .serializers import NoteSerializer
from rest_framework.decorators import permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@permission_classes([IsAuthenticated])
class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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