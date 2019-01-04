from django.views import View

from ..helpers import ApiMessage, ApiResponse
from ..models import Shop


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

        start = request.GET.get('start', 0)
        count = request.GET.get('count', 20)
        status = request.GET.get('status', 'ACTIVE')
        sort = request.GET.get('sort', 'id|DESC')

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
            "start": start,
            "count": count,
            "total": num_of_shops,
            "shops": shops
        }

        return ApiResponse(data)
