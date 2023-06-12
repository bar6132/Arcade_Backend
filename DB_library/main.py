from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from game_shop.models import Game

@csrf_exempt
def add_games(request):
    game_data = [
        {
            'game_type': 'New',
            'console': 'PS4',
            'game_name': 'Game 1',
            'price': 50,
            'game_img': None,
            'uploader': None,
        },
        {
            'game_type': 'Old',
            'console': 'Xbox One',
            'game_name': 'Game 2',
            'price': 30,
            'game_img': None,
            'uploader': None,
        },
        # Add more game data entries as needed
    ]

    for data in game_data:
        game = Game.objects.create(
            game_type=data['game_type'],
            console=data['console'],
            game_name=data['game_name'],
            price=data['price'],
            game_img=data['game_img'],
            uploader=data['uploader'],
        )
        game.save()

    return HttpResponse('Games added successfully.')