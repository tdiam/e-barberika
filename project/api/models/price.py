# price model

from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from project.api.models import Shop, Product

#########################

class Price(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_from = models.DateField(null=False, blank=False, default=datetime.now)
    date_to = models.DateField(null=True, default=None)

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

    def is_valid(self):
        try:
            assert self.price > 0
            assert Price.check_dates(self.date_from, self.date_to)
            assert self.user.is_authenticated

            return True
        except (AssertionError, AttributeError):
            return False

    @staticmethod
    def add_price(**kwargs):
        '''
        Add a new price to the observatory.
        # TODO: how do we handle conflicting dates?
        @returns True/False
        '''

        p = Price(**kwargs)
        if not p.is_valid():
            return False

        has_unsolvable_conflicts = Price.objects.filter(date_from__gte=p.date_from).filter(date_from__lte=p.date_to).exists()

        if has_unsolvable_conflicts:
            return False

        # if these are more than one, we have already lost :)
        # FIXME: what about null `date_to`?
        try:
            conflicting = Price.objects.filter(date_from__lte=p.date_from).filter(date_to__gte=p.date_from).get()

            # resolve conflict
            conflicting.date_to = p.date_from           # FIXME: minus one day?
            conflicting.save()
        except models.ObjectDoesNotExist as e:
            pass

        # save price
        p.save()
        return True
