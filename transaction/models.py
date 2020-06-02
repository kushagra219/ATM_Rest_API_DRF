from django.db import models
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.utils.translation import gettext as _

# Create your models here.

# class IntegerRangeField(models.IntegerField):
#     def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
#         self.min_value, self.max_value = min_value, max_value
#         models.IntegerField.__init__(self, verbose_name, name, **kwargs)
#     def formfield(self, **kwargs):
#         defaults = {'min_value': self.min_value, 'max_value':self.max_value}
#         defaults.update(kwargs)
#         return super(IntegerRangeField, self).formfield(**defaults)

class ATMMachine(models.Model):
    hundred_notes = models.PositiveIntegerField()
    five_hundred_notes = models.PositiveIntegerField()
    two_thousand_notes = models.PositiveIntegerField()

    def totalAmount(self):
        return self.hundred_notes * 100 + self.five_hundred_notes * 500 + self.two_thousand_notes * 2000

    def __str__(self):
        return "Money in ATM Machine - {}".format(self.totalAmount())


class Card(models.Model):
    card_no = models.CharField(max_length=8)
    card_pin = models.CharField(max_length=4)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Card - {} Amount - {}".format(self.card_no, self.amount)

    class Meta:
        ordering = ('id',)


class CardTransaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="transaction")
    amount = models.PositiveIntegerField()
    hundred_notes = models.PositiveIntegerField(null=True, blank=True)
    five_hundred_notes = models.PositiveIntegerField(null=True, blank=True)
    two_thousand_notes = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "Card - {}  Amount - {}".format(self.card.card_no, self.amount)


