from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views import View
from django.contrib.gis.geos import Point

from ..helpers import ApiMessage, ApiResponse
from ..models import Shop, ShopTag


class ShopsView(View):
    def get(self, request):
        '''Returns a list of the shops in the observatory.

        Parameters:
         - `start`: Pagination offset.
         - `count`: Pagination page size.
         - `sort`: Sort criterion of the form <field>|<ASC|DESC>.
         - `status`:
            - `ACTIVE`: Select shops that have not been withdrawn from the observatory.
            - `WITHDRAWN`: Select shops that have been withdrawn.
            - `ALL`: Select all shops.

        The view validates the parameter values and returns 400 Bad Request if any
        malformed data occurs.
        '''
        ALLOWED_STATUS_TYPES = ['ALL', 'ACTIVE', 'WITHDRAWN']
        ALLOWED_SORT_FIELDS = ['id', 'name']
        ALLOWED_SORT_TYPES = ['ASC', 'DESC']

        start = request.data.get('start', 0)
        count = request.data.get('count', 20)
        status = request.data.get('status', 'ACTIVE')
        sort = request.data.get('sort', 'id|DESC')

        # Check `start` parameter
        try:
            start = int(start)
            if start < 0:
                raise ValueError
        except ValueError:
            return ApiMessage('Το `start` πρέπει να είναι θετικός ακέραιος', status=400)

        # Check `count` parameter
        try:
            count = int(count)
            if count < 0:
                raise ValueError
        except ValueError:
            return ApiMessage('Το `count` πρέπει να είναι θετικός ακέραιος', status=400)

        # Check `status` parameter
        if status not in ALLOWED_STATUS_TYPES:
            return ApiMessage(f'Μη έγκυρο status καταστημάτων "{status}"', status=400)

        # Check `sort` parameter
        try:
            sort_field, sort_type = sort.split('|')
            if sort_field not in ALLOWED_SORT_FIELDS or sort_type not in ALLOWED_SORT_TYPES:
                raise ValueError
        except ValueError:
            return ApiMessage(f'Μη έγκυρο κριτήριο ταξινόμησης "{sort}"', status=400)
        else:
            # Process `sort`
            if sort_type == 'ASC':
                order_by = sort_field
            else:
                order_by = '-' + sort_field

        # Process `status`
        if status == 'ALL':
            shops = Shop._base_manager.all()
        elif status == 'WITHDRAWN':
            shops = Shop._base_manager.filter(withdrawn=True)
        else: # ACTIVE
            shops = Shop.objects.all()

        # Process `start` and `count`
        num_of_shops = shops.count()
        shops = shops.order_by(order_by)
        shops = shops[start : start+count]

        data = {
            'start': start,
            'count': count,
            'total': num_of_shops,
            'shops': shops
        }

        return ApiResponse(data)

    def post(self, request):
        '''Creates new shop.

        Parameters:
         - `name`: Name of the shop.
         - `address`: Address of the shop.
         - `lng`: Longitude.
         - `lat`: Latitude.
         - `tags`: List of strings that will be applied as tags to the shop (default []).
        '''
        name = request.data.get('name')
        address = request.data.get('address')
        lng = request.data.get('lng')
        lat = request.data.get('lat')
        tags = request.data.getlist('tags')

        try:
            lng = float(lng)
            lat = float(lat)
        # TypeError will occur if argument is not number or string (eg None)
        # ValueError will occur if argument cannot be parsed into a float
        except (TypeError, ValueError):
            return ApiMessage('Τα πεδία συντεταγμένων πρέπει να είναι έγκυροι δεκαδικοί αριθμοί', status=400)

        shop = Shop(
            name=name,
            address=address,
            coordinates=Point(lng, lat)
        )
        try:
            # save() does not call the validators
            # so we need to call full_clean() explicitly
            # https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.full_clean
            shop.full_clean()
            shop.save()
        except (ValidationError, IntegrityError):
            return ApiMessage('Η μορφή των δεδομένων δεν είναι έγκυρη', status=400)

        tag_objs = [ShopTag(tag=tag) for tag in tags]
        shop.tags.set(tag_objs)
        return ApiResponse(shop, status=201)
