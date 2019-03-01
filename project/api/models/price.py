# price model

from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from project.api.models import Shop, Product
from project.api.helpers import user_is_volunteer

#########################


def datetime_now():
    '''default value for `date_from` field'''
    return datetime.now()

def datetime_oneyearfromnow():
    '''default value for `date_to` field`'''
    return datetime.now() + timedelta(days=365)

#########################

class Price(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_from = models.DateField(null=False, blank=False, default=datetime_now)
    date_to = models.DateField(null=False, default=datetime_oneyearfromnow)

    def __str__(self):
        return f'Price[shop="{self.shop}", product="{self.product}", price="{self.price}", date_from="{self.date_from}", date_to="{self.date_to}"]' + (' -- old' if self.date_to < datetime.now().date() else '')

    @staticmethod
    def parse_date(date_str: str):
        '''
        Raises ValueError in case of bad string format
        '''
        if len(date_str) != 10:
            raise ValueError('expecting YYYY-MM-DD format')

        date = datetime.strptime(date_str, '%Y-%m-%d')

        return date

    def convert_to_str(date):
        return datetime.strftime(date, '%Y-%m-%d')

    @staticmethod
    def check_dates(date_from, date_to):
        '''
        Ensure consistency
        '''
        return (date_from is not None) and (date_to is not None) and date_from <= date_to

    def clean(self):
        '''
        checks that a Price object is valid. raises `ValidationError` otherwise
        '''
        if (self.date_from is None) or (self.date_to is None):
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
            return None

        has_unsolvable_conflicts = Price.objects.filter(
            date_from__gte=p.date_from,
            date_from__lte=p.date_to,
            shop__id=p.shop.id,
            product__id=p.product.id).exists()

        if has_unsolvable_conflicts:
            return None

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
            return p
        except IntegrityError:
            return None

    @staticmethod
    def dates_between(date_from, date_to):
        '''return an iteratable of dates from @date_from until @date_to (non inclusive)'''
        result = []
        dt = date_from
        while dt <= date_to:
            result.append(dt)
            dt += timedelta(days=1)

        return result

    def explode(self):
        '''given a price object, return a list of its data for all days'''
        result = []

        for date in Price.dates_between(self.date_from, self.date_to):
            o = {
                'date': Price.convert_to_str(date),
                'productId': self.product.id,
                'productName': self.product.name,
                'productTags': [tag.tag for tag in self.product.tags.all()],
                'shopName': self.shop.name,
                'shopAddress': self.shop.address,
                'shopTags': [tag.tag for tag in self.shop.tags.all()],
                'shopId': self.shop.id,
                'price': float(self.price)
            }

            try:
                o['shopDist'] = self.geoDist.km
            except AttributeError:
                o['shopDist'] = 0

            result.append(o)

        return result

    @staticmethod
    def sort_objects(objects, criteria):
        # sort by each criterion in reverse order
        if not criteria or not objects:
            return

        criteria.reverse()
        for (sort_field, sort_type) in criteria:
            objects.sort(key=lambda o: o[sort_field], reverse=(sort_type=='DESC'))
