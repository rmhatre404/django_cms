from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Content
from .serializers import ContentSerializer


class ContentListCreateView(APIView):
    """
    Handles listing and creating content items.
    - Admin users can view all content.
    - Authors can only view and create their own content.
    - Supports search and pagination.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Default page size (adjustable globally)

        # Admin sees all content; authors see their own
        if request.user.is_staff:
            contents = Content.objects.all().order_by('id')  # Added ordering for pagination consistency
        else:
            contents = Content.objects.filter(author=request.user).order_by('id')  # Added ordering

        # Apply search filter
        search_query = request.query_params.get('search', '')
        if search_query:
            contents = contents.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(categories__icontains=search_query)
            )

        # Paginate results
        result_page = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Handles creating new content. Ensures that only PDF files are uploaded.
        """
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            # Validate document file type
            document = request.data.get('document')
            if document and not document.name.endswith('.pdf'):
                return Response({"document": ["Only PDF files are allowed."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Assign the logged-in user as the author and save content
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
    """
    Handles retrieving, updating, and deleting individual content items.
    - Admin can access and modify all content.
    - Authors can only access and modify their own content.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """
        Retrieve the content object if it exists and the user has access.
        """
        try:
            content = Content.objects.get(pk=pk)
            # Admin can access all; authors can only access their own content
            if user.is_staff or content.author == user:
                return content
            return None
        except Content.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a single content item by ID.
        """
        content = self.get_object(pk, request.user)
        if not content:
            return Response({"detail": "Not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a content item by ID. Only PDF files are allowed for the document field.
        """
        content = self.get_object(pk, request.user)
        if not content:
            return Response({"detail": "Not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            # Validate document file type
            document = request.data.get('document')
            if document and not document.name.endswith('.pdf'):
                return Response({"document": ["Only PDF files are allowed."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save updates to the content item
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a content item by ID.
        """
        content = self.get_object(pk, request.user)
        if not content:
            return Response({"detail": "Not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the content item
        content.delete()
        return Response({"detail": "Content deleted."}, status=status.HTTP_204_NO_CONTENT)
