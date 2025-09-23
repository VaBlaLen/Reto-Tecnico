from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apiv1.serializers import ConsumoSerializer, GeneracionSerializer
from apiv1.csvreader import readcsv

# Create your views here.

class GeneracionList(APIView):

    """Returns the values of the generacion csv in ready to consume format"""

    def get(self, request, format=None):
        generacionset = readcsv("generacion")
        serializer = GeneracionSerializer(generacionset, many=True)
        resp = []
        for i in serializer.data:
            resp.append({"valor":i['generacion'], 'timestamp':i['timestamp']})
        return Response(resp, status=status.HTTP_200_OK)
    
class ConsumoList(APIView):
    """Returns the values of the test_consumos_10_users csv in ready to consume format"""

    def get(self, request, format=None):
        consumoset = readcsv("test_consumos_10_users")
        serializer = ConsumoSerializer(consumoset, many=True)
        resp = {}
        for i in serializer.data:
            if i['uid'] not in resp:
                resp[i['uid']] = []
            resp[i['uid']].append({"valor":i['consumo'], 'timestamp':i['timestamp']})
        return Response(resp, status=status.HTTP_200_OK)