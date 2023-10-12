# Python
from typing import Optional

# DRF
from rest_framework import viewsets , filters
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError

# First party
from games.models import Game
from games.serializers import (
    GameCreateSerializer,
    GameSerializer
)


class GameViewSet(viewsets.ModelViewSet):
    
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def list(self, request, *args, **kwargs):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        queryset = self.queryset
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(
        self,
        request: Request,
        pk: Optional[int] = None
    ) -> Response:
        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError(
                'Object not found!',
                code=404
            )
        serializer: GameSerializer = \
            GameSerializer(
                instance=game
            )
        return Response(data=serializer.data)

    def create(
        self,
        request: Request,
        *args: tuple,
        **kwargs: dict
    ) -> Response:
        serializer: GameCreateSerializer = \
            GameCreateSerializer(
                data=request.data
            )
        serializer.is_valid(
            raise_exception=True
        )
        game: Game = serializer.save()
        return Response(
            data={
                'status': 'ok',
                'message': f'Game {game.name} is created! Id: {game.pk}'
            }
        )

    def update(
        self,
        request: Request,
        pk: str
    ) -> Response:
        """Обновление игры."""

        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found', code=400)

        serializer: GameSerializer = \
            GameSerializer(
                instance=game,
                data=request.data
            )
        if not serializer.is_valid():
            return Response(
                data={
                    'status': 'Warning',
                    'message': f'Warning with: {game.name}'
                }
            )
        serializer.save()
        return Response(
            data={
                'status': 'OK',
                'message': f'Game: {game.name} was updated'
            }
        )

    def partial_update(
        self,
        request: Request,
        pk: str
    ) -> Response:
        """Частичное обновление игры."""

        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found', code=400)

        serializer: GameSerializer = \
            GameSerializer(
                instance=game,
                data=request.data,
                partial=True
            )
        if not serializer.is_valid():
            return Response(
                data={
                    'status': 'Warning',
                    'message': f'Warning with: {game.name}'
                }
            )
        serializer.save()
        return Response(
            data={
                'status': 'OK',
                'message': f'Game: {game.name} was updated'
            }
        )

    def destroy(
        self,
        request: Request,
        pk: str
    ) -> Response:
        """Удаление игры."""

        # TODO: мы будем проставлять
        #       ей статус 'datetime_deleted'
        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found', code=400)
        else:
            name: str = game.name
            game.delete()

        return Response(
            data={
                'status': 'OK',
                'message': f'Game {name} is deleted!'
            }
        )

