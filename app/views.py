from rest_framework.views import APIView
from .custom_permissions import IsAdmin, IsEditor
from rest_framework.response import Response
from rest_framework import generics, status as st
from django.contrib.auth.models import User
from .models import ContentItem, Profile, User
from rest_framework import filters
from django.http import Http404
from .serializers import UserSerializer, ContentItemSerializer, ContentItemSearchSerializer
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action, permission_classes  # other imports elided


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsEditor]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=st.HTTP_201_CREATED)
        return Response(serializer.errors, status=st.HTTP_400_BAD_REQUEST)


class APIView1(APIView):
    permission_classes = [IsAdmin | IsEditor]

    def get(self, request, format=None):
        return Response({"aa":22}, status=st.HTTP_200_OK)


class ContentItemList(APIView):
    serializer_class = ContentItemSerializer
    permission_classes = [IsAdmin | IsEditor]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return ContentItem.objects.get(pk=pk)
        except ContentItem.DoesNotExist:
            raise Http404

    def get(self, request):
        if self.request.user.is_superuser:
          items = ContentItem.objects.all()
        else:
          items = ContentItem.objects.filter(created_by=self.request.user)
        serializer = ContentItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContentItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=st.HTTP_201_CREATED)
        return Response(serializer.errors, status=st.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        content_item = self.get_object(pk)
        serializer = ContentItemSerializer(content_item, data=request.data)
        if serializer.is_valid():
          if self.request.user.is_superuser:
            serializer.save()
            return Response(serializer.data)
          elif content_item.created_by == self.request.user:
            serializer.save()
            return Response(serializer.data)
          else:
            return Response({"detail": "You do not have permission to perform this action."},
              status=st.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=st.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        content_item = self.get_object(pk)
        if self.request.user.is_superuser:
          content_item.delete()
          return Response(status=st.HTTP_204_NO_CONTENT)
        elif content_item.created_by == self.request.user:
          content_item.delete()
          return Response(status=st.HTTP_204_NO_CONTENT)
        else:
          return Response({"detail": "You do not have permission to perform this action."},
            status=st.HTTP_403_FORBIDDEN)


class ContentListView(generics.ListAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'summary', 'categories']