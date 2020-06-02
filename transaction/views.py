from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, generics, filters
from .serializers import * 
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView
import json
# Create your views here.

class registerCardAPI(generics.CreateAPIView):
    serializer_class = CardSerializer


class authenticateCardAPI(APIView):
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
            card_no = request.data.get("card_no")
            card_pin = request.data.get("card_pin")
            if card_no is None or card_pin is None:
                return Response({"success":"False", "detail":"Please provide both card number and pin"},
                                status=HTTP_400_BAD_REQUEST)
            card = Card.objects.get(card_no=card_no, card_pin=card_pin)
            if not card:
                return Response({"success":"False", "detail": "Invalid Credentials"},
                                status=HTTP_404_NOT_FOUND)
            return Response({"success":"True", "detail":"Card Validation Successful"}, status=HTTP_200_OK)


class depositMoneyAPI(APIView):
    
    def post(self, request, *args, **kwargs):
            card_no = request.data.get("card_no")
            card_pin = request.data.get("card_pin")
            amount = request.data.get("amount")
            hundred_notes = request.data.get("100")
            five_hundred_notes = request.data.get("500")
            two_thousand_notes = request.data.get("2000")
            if card_no is None or card_pin is None or amount is None:
                return Response({"success":"False", "detail":"Please provide both card number and pin"},
                                status=HTTP_400_BAD_REQUEST)
            authenticateCard = authenticateCardAPI()
            response = authenticateCard.post(request=request, card_no=card_no, card_pin=card_pin)
            if response.data["success"] == "True":
                amount = int(amount)
                hundred_notes = int(hundred_notes)
                five_hundred_notes = int(five_hundred_notes)
                two_thousand_notes = int(two_thousand_notes)
                card = Card.objects.get(card_no=card_no, card_pin=card_pin) 
                transaction = CardTransaction.objects.create(card=card, amount=amount, hundred_notes=hundred_notes, five_hundred_notes=five_hundred_notes, two_thousand_notes=two_thousand_notes)
                card.amount += amount
                atm = ATMMachine.objects.get(pk=1)
                atm.hundred_notes += hundred_notes
                atm.five_hundred_notes += five_hundred_notes
                atm.two_thousand_notes += two_thousand_notes
                atm.save()
                card.save()
                return Response({"success":"True", "detail":"Transaction Successful", "balance":card.amount}, status=HTTP_200_OK)
            else:
                return Response({"success":"False", "detail": "Invalid Credentials"},
                                    status=HTTP_404_NOT_FOUND)

                
class withdrawMoneyAPI(APIView):
    
    def post(self, request, *args, **kwargs):
            card_no = request.data.get("card_no")
            card_pin = request.data.get("card_pin")
            amount = request.data.get("amount")
            if card_no is None or card_pin is None or amount is None:
                return Response({"success":"False", "detail":"Please provide both card number and pin"},
                                status=HTTP_400_BAD_REQUEST)
            authenticateCard = authenticateCardAPI()
            response = authenticateCard.post(request=request, card_no=card_no, card_pin=card_pin)
            if response.data["success"] == "True":
                amount = int(amount)
                card = Card.objects.get(card_no=card_no, card_pin=card_pin) 
                if card.amount < amount:
                    return Response({"success":"False", "detail":"Transaction UnSuccessful", "detail":"not enough balance"}, status=HTTP_200_OK)
                else:
                    two_thousand_notes = amount % 2000
                    if two_thousand_notes > 0:
                        amount -= two_thousand_notes * 2000
                    five_hundred_notes = amount % 500
                    if five_hundred_notes > 0:
                        amount -= five_hundred_notes * 500
                    hundred_notes = amount % 100
                    if hundred_notes > 0:
                        amount -= hundred_notes * 100
                    transaction = CardTransaction.objects.create(card=card, amount=amount, hundred_notes=hundred_notes, five_hundred_notes=five_hundred_notes, two_thousand_notes=two_thousand_notes)
                    card.amount -= amount
                    atm = ATMMachine.objects.get(pk=1)
                    atm.hundred_notes += hundred_notes
                    atm.five_hundred_notes += five_hundred_notes
                    atm.two_thousand_notes += two_thousand_notes
                    atm.save()
                    card.save()
                    return Response({"success":"True", "detail":"Transaction Successful", "balance":card.amount, "100":hundred_notes, "500":five_hundred_notes, "2000":two_thousand_notes}, status=HTTP_200_OK)
            else:
                return Response({"success":"False", "detail": "Invalid Credentials"},
                                    status=HTTP_404_NOT_FOUND)

            










