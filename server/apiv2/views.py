from datetime import datetime
from itertools import count
from sqlite3 import Date
from django.db import connection
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from apiv2.models import Consumo, Generación
from apiv2.serializers import ConsumoSerializer, GeneracionSerializer, GenlistSerializer, ConlistSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class GeneracionList(APIView):
    """Returns the values of generation table in ready to consume format"""
    fromdateparam =  openapi.Parameter('from', openapi.IN_QUERY, description="from timestamp [OPTIONAL]",required=False, type=openapi.TYPE_NUMBER)
    todateparam =  openapi.Parameter('to', openapi.IN_QUERY, description="to timestamp [OPTIONAL]",required=False, type=openapi.TYPE_NUMBER)
    user_response = openapi.Response('response description', GenlistSerializer)
    
    @swagger_auto_schema(
        manual_parameters=[fromdateparam, todateparam], responses={200: user_response, 400:"requested origin timestamp is greater than the registered gen period"}
    )
    def get(self, request:Request, format=None):
       

       fromt = float(request.query_params.get("from", default=0.0))
       tot = float(request.query_params.get("to", default=0.0))
       if (fromt==0 and tot == 0):
            queryset = Generación.objects.all()
            serializer = GeneracionSerializer(queryset, many=True)
            return Response({'results':serializer.data}, status= status.HTTP_200_OK)
       else:
           lastelem = Generación.objects.last()
           if lastelem !=  None:
                lastts = lastelem.timestamp.timestamp()
                if lastts < fromt:
                    return Response("requested origin timestamp is greater than the registered gen period",  status = status.HTTP_404_NOT_FOUND)
                else:
                    firstelem = Generación.objects.first()
                    fromt = max(fromt, firstelem.timestamp.timestamp())
                    endts = min(tot, lastts) if tot > 0 else lastts
                    queryset = Generación.objects.filter(timestamp__gte = datetime.fromtimestamp(fromt), timestamp__lte = datetime.fromtimestamp(endts))
                    serializer = GeneracionSerializer(queryset, many=True)
                    return Response({'results':serializer.data}, status= status.HTTP_200_OK)
           else:
               return Response({'results':[]},  status = status.HTTP_200_OK)
           
class ConsumoList(APIView):

    """Returns the values of consumer table in ready to consume format"""

    userlist= openapi.Parameter('users', openapi.IN_QUERY, description="list of user ids [OPTIONAL]",required=False, type=openapi.TYPE_STRING)
    user_response = openapi.Response('response description', ConlistSerializer)

    @swagger_auto_schema(
        manual_parameters=[userlist], responses={200: user_response}
    )
    def get(self, request:Request, format=None):
        userlist = request.query_params.get('users', default="")
        if (userlist == ""):
            consumoset = Consumo.objects.all().order_by('uid')
            serializer = ConsumoSerializer(consumoset, many=True)
            return Response({'results':serializer.data}, status= status.HTTP_200_OK)
        else:
            userarray = userlist.split(',')
            userarray = list(map(int, userarray))
            consumoset = Consumo.objects.filter(uid__in=userarray)
            serializer = ConsumoSerializer(consumoset, many=True)
            return Response({'results':serializer.data}, status= status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uid'],
            properties={
                        'uid': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'values': openapi.Schema(type=openapi.TYPE_ARRAY,
                        items=openapi.Schema
                            ( type=openapi.TYPE_OBJECT,
                                required=['timestamp,consumo'],
                                properties={
                                    'timestamp': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'consumo': openapi.Schema(type=openapi.TYPE_NUMBER),
                                })),
                                }),
        responses={200: 'ok'}
    )   
    def post(self, request:Request, format=None):
        data = request.data
        filteru = Consumo.objects.filter(uid=data['uid'])
        if (len(filteru) > 0):
            return Response("user already exists",  status = status.HTTP_404_NOT_FOUND)
        post = []
        for dat in data['values']:
            post.append(tuple([data['uid'], dat['consumo'],datetime.fromtimestamp(dat['timestamp'])]))
            
        with connection.cursor() as cursor:
            cursor.executemany("INSERT INTO apiv2_consumo (uid, consumo, timestamp) VALUES (?, ?, ?)", post)
        
        return Response('ok', status= status.HTTP_200_OK) 