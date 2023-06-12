import rest_framework.pagination as pgn
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from game_shop.models import Game
from game_shop.serializers import GameSerializer


class MyPagination(pgn.PageNumberPagination):
    page_size  = 10
    page_query_param = 'page_num'
    max_page_size = 100


class GamePagination(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = MyPagination

    

class MyPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

@api_view(['GET'])
def serve_game_pagination(request):
    paginator = MyPagination()
    game_objects = Game.objects.all()
    paginated_games = paginator.paginate_queryset(game_objects, request)
    serializer = GameSerializer(paginated_games, many=True)
    return paginator.get_paginated_response(serializer.data)