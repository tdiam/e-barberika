from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class ShopTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.tag

    def __serialize__(self):
        return self.tag


class BaseShopManager(models.Manager):
    def get_queryset(self):
        '''Omit withdrawn shops from results by default'''
        return super().get_queryset().filter(withdrawn=False)

class ShopQuerySet(models.QuerySet):
    def within_distance_from(self, lat, lng, **distance):
        '''Find shops within given distance from given point.

        Arguments:
            - lat: Latitude of reference point.
            - lng: Longitude of reference point.
            - **distance: `Distance` arguments. For supported units see:
                https://docs.djangoproject.com/en/2.1/ref/contrib/gis/measure/#supported-units

        Example:
            ```
            shops = Shop.objects.within_distance_from(39.89, 22.18, km=10)
            ```
        '''
        return self.filter(
            coordinates__dwithin=(Point(lng, lat), Distance(**distance))
        )

    def with_tags(self, tags):
        '''Find shops whose tags contain any of the input tags.

        Arguments:
            - tags: List of tag names.

        Example:
            ```
            shops = Shop.objects.with_tags(['value-for-money', 'cozy'])
            ```

        Details:
            `tags__tag__in` will search the intermediate table (shop, tag) and get
            the pairs for which the tag is listed in the input tags array.
            A join operation will return the corresponding shop for each such pair.
            If a shop had more than one of its tags matched, it would appear that
            many times in the result.
            The `.distinct()` modifier will remove such repetitions.
        '''
        return self.filter(
            tags__tag__in=tags
        ).distinct()

# Both a custom manager and custom queryset methods are used
# in order to facilitate by-default exclusion of withdrawn Shops
# and chainable custom methods like `within_distance_from` and `with_tags`.
#
# Adapted from:
# https://docs.djangoproject.com/en/2.1/topics/db/managers/#from-queryset
ShopManager = BaseShopManager.from_queryset(ShopQuerySet)


class Shop(models.Model):
    '''Physical places where the products of our application are sold'''

    # Long integers are required from the specification
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    # We will use GeoDjango for storing and querying spatial data
    # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/
    # geography=True will enable distance lookups that use metric
    # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/model-api/#geography
    #
    # NOTE: If the field is set via Python and the Point model is used,
    # the syntax is Point(longitude, latitude).
    coordinates = models.PointField(geography=True)

    withdrawn = models.BooleanField(default=False)

    tags = models.ManyToManyField(ShopTag)

    objects = ShopManager()

    def __str__(self):
        return self.name

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'lng': self.coordinates.x,
            'lat': self.coordinates.y,
            'tags': self.tags.all(),
            'withdrawn': self.withdrawn,
        }
