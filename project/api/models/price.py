# price model

import datetime

from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from project.api.models import Shop, Product
from project.api.helpers import user_is_volunteer

#########################


def datetime_now():
    '''default value for `date_from` field'''
    return datetime.datetime.now()

def datetime_oneyearfromnow():
    '''default value for `date_to` field`'''
    return datetime.datetime.now() + datetime.timedelta(days=365)

#########################

class Price(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_from = models.DateField(null=False, blank=False, default=datetime_now)
    date_to = models.DateField(null=False, default=datetime_oneyearfromnow)

    @staticmethod
    def parse_date(date_str: str):
        '''
        Raises ValueError in case of bad string format
        '''
        if len(date_str) != 10:
            raise ValueError('expecting YYYY-MM-DD format')

        date = datetime.strptime(date_str, '%Y-%m-%d')

        return date

    @staticmethod
    def check_dates(date_from, date_to):
        '''
        Ensure consistency
        '''
        return (date_from or date_to) is None or date_from <= date_to

    def clean(self):
        '''
        checks that a Price object is valid. raises `ValidationError` otherwise
        '''
        if (self.date_from or self.date_to) is None:
            raise ValidationError('dates cannot be NULL')

        if self.price <= 0:
            raise ValidationError('price must be positive')

        if not Price.check_dates(self.date_from, self.date_to):
            raise ValidationError('invalid dates')

        if not user_is_volunteer(self.user):
            raise ValidationError('unauthorized user')

    @staticmethod
    def add_price(**kwargs):
        '''
        Add a new price to the observatory.
        @return True/False
        '''
        try:
            p = Price(**kwargs)
            p.clean()
        except (TypeError, ValueError, ValidationError):
            return False

        has_unsolvable_conflicts = Price.objects.filter(
            date_from__gte=p.date_from,
            date_from__lte=p.date_to,
            shop__id=p.shop.id,
            product__id=p.product.id).exists()

        if has_unsolvable_conflicts:
            return False

        # in case of conflict, update `date_to` of old price.
        conflicting_qs = Price.objects.filter(
            date_from__lte=p.date_from,
            date_to__gte=p.date_from,
            shop__id=p.shop.id,
            product__id=p.product.id)

        if conflicting_qs.exists():
            conflicting = conflicting_qs.get()

            # resolve conflict
            conflicting.date_to = p.date_from
            conflicting.save()

        # save price
        try:
            p.save()
            return True
        except IntegrityError:
            return False
