from rest_framework import serializers
from .models import *

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardTransaction
        fields = "__all__"

    