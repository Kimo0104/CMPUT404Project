from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
import json

from models import Posts                          #Models defines how their objects are stored in the database
from serializers import PostsSerializer #serializers defines how to convert a post object to JSON
import datetime
class Posts(viewsets.ViewSet):
    #query
    #serializer_class = PostsSerializer
    
    """-----------------------------------------------
    --------------------------------------------------
    ---------- START OF DEFAULT FUNCTIONS ------------
    --------------------------------------------------
    -----------------------------------------------"""  
    
    #GET posts/ will call this function
    def list(self, request):
        # define queryset to be the output of your query
        # pass the output to the serializer. If there's multiple rows in your output set many=True; otherwise False
        # return the data from the serializer
        queryset = Posts.objects.all()  
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST posts/ will call this function
    def create(self, request):
        #get info from request body
        body_unicode = request.body.decode('utf-8')
        body_dict = json.loads(body_unicode)

        #ensure required data exists
        if not ("title" in body_dict) or not ("author_id" in body_dict):
            return HttpResponseBadRequest

        #fill in non-required data with Nones
        if not "description_type" in body_dict:
            body_dict["description_type"] = None
        if not "description" in body_dict:
            body_dict["description"] = None
        if not "image_url" in body_dict:
            body_dict["image_url"] = None

        #set fields created in back-end
        body_dict["date"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        queryset = Posts.objects.create(
            title = body_dict["title"],
            description_type = body_dict["description_type"],
            description = body_dict["description"],
            date = body_dict["date"],
            image_url = body_dict["image_url"],
            title = body_dict["author"]
        )  
        serializer = PostsSerializer(queryset, many=False)
        return Response(serializer.data)

    #GET posts/{id} will call this function
    def retrieve(self, request, pk=None):
        queryset = Posts.objects.get(id = pk) 
        serializer = PostsSerializer(queryset, many=False)
        return Response(serializer.data)

    #PUT posts/{id} will call this function
    def update(self, request, pk=None):
        pass #I don't need this, so I won't implement


    #PATCH posts/{id} will call this function
    def partial_update(self, request, pk=None):
        #get existing post
        existingPost = Posts.objects.get(id = pk) 

        #get info from request body
        body_unicode = request.body.decode('utf-8')
        body_dict = json.loads(body_unicode)

        #update any fields passed to us
        if "title" in body_dict:
            existingPost.title = body_dict["title"]
        if "author_id" in body_dict:
            existingPost.author_id = body_dict["author_id"]
        if "description_type" in body_dict:
            existingPost.description_type = body_dict["description_type"]
        if "image_url" in body_dict:
            existingPost.image_url = body_dict["image_url"]
        if "date" in body_dict:
            existingPost.date = body_dict["date"]

        #save changes
        existingPost.save()
        
        serializer = PostsSerializer(existingPost, many=False)
        return Response(serializer.data)

    #DELETE posts/{id} will call this function
    def destroy(self, request, pk=None):
        return Posts.objects.get(id = pk).delete()
    
    """-----------------------------------------------
    --------------------------------------------------
    ---------- END OF DEFAULT FUNCTIONS --------------
    --------------------------------------------------
    -----------------------------------------------"""
    
    """-----------------------------------------------
    --------------------------------------------------
    --------- START OF SPECIFIC FUNCTIONS ------------
    --------------------------------------------------
    -----------------------------------------------"""
    #GET posts/{id}/author will call this function
    #this function returns all public posts from the requested author
    @action(detail=True, methods=['get'])
    def author(self, request, pk=None):
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)
        


    #GET posts/{id}/comments will call this function
    #this function returns all 
    @action(detail=True, methods=['get']) 
    #   detail states whether an {id) needed. if detail were false, then the URL would be: posts/comments
    #   methods states which HTTP requests will call this action
    #   the name of the function determines the last part of the URL
    def comments(self, request, pk=None):
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    
    """-----------------------------------------------
    --------------------------------------------------
    --------- END OF SPECIFIC FUNCTIONS --------------
    --------------------------------------------------
    -----------------------------------------------"""





