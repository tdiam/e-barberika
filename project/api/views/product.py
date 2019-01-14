from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views import View

from ..helpers import ApiMessage, ApiResponse
from ..models import Product, ProductTag


class ProductsView(View):
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
            return ApiMessage('The `start` must be a positive integer', status=400)

        # Check `count` parameter
        try:
            count = int(count)
            if count < 0:
                raise ValueError
        except ValueError:
            return ApiMessage('The `count` must be a positive integer', status=400)

        # Check `status` parameter
        if status not in ALLOWED_STATUS_TYPES:
            return ApiMessage(f'Invalid product status "{status}"', status=400)

        # Check `sort` parameter
        try:
            sort_field, sort_type = sort.split('|')
            if sort_field not in ALLOWED_SORT_FIELDS or sort_type not in ALLOWED_SORT_TYPES:
                raise ValueError
        except ValueError:
            return ApiMessage(f'Invalid sorting criterion "{sort}"', status=400)
        else:
            # Process `sort`
            if sort_type == 'ASC':
                order_by = sort_field
            else:
                order_by = '-' + sort_field

        # Process `status`
        if status == 'ALL':
            products = Product._base_manager.all()
        elif status == 'WITHDRAWN':
            products = Product._base_manager.filter(withdrawn=True)
        else: # ACTIVE
            products = Product.objects.all()

        # Process `start` and `count`
        num_of_products = products.count()
        products = products.order_by(order_by)
        products = products[start : start+count]

        data = {
            'start': start,
            'count': count,
            'total': num_of_products,
            'products': products
        }

        return ApiResponse(data)

    def post(self, request):
    
        name = request.data.get('name')
        description = request.data.get('description')
        category = request.data.get('category')
        tags = request.data.getlist('tags')

        product = Product(
            name=name,
            description=description,
            category=category
        )
        try:
            # save() does not call the validators
            # so we need to call full_clean() explicitly
            # https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.full_clean
            product.full_clean()
            product.save()
        except (ValidationError, IntegrityError):
            return ApiMessage('Data format is invalid', status=400)

        tag_objs = [ProductTag(tag=tag) for tag in tags]
        for t in tag_objs:
            t.save()
        product.tags.set(tag_objs)
        return ApiResponse(product, status=201)

class ProductView(View):
    def get(self, request, pk=None):
        '''Returns the product with the given id (pk). Error 404 if not found.'''
        try:
            product = Product.objects.get(pk=pk)
        # ValueError will be raised when pk cannot be converted to integer
        except (Product.DoesNotExist, ValueError):
            return ApiMessage(f'Product with id {pk} not found.', status=404)
        else:
            return ApiResponse(product)

    def put(self, request, pk=None):
        '''Replaces existing product.
        Parameters: Same as in POST /products.
        '''

        try:
            product = Product.objects.get(pk=pk)
        except (Product.DoesNotExist, ValueError):
            return ApiMessage(f'Product with id {pk} not found.', status=404)

        name = request.data.get('name')
        description = request.data.get('description')
        category = request.data.get('category')
        tags = request.data.getlist('tags')


        product.name = name
        product.description = description
        product.category = category
        try:
            # save() does not call the validators
            # so we need to call full_clean() explicitly
            # https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.full_clean
            product.full_clean()
            product.save()
        except (ValidationError, IntegrityError):
            return ApiMessage('Data format is invalid', status=400)

        tag_objs = [ProductTag(tag=tag) for tag in tags]
        for t in tag_objs:
            t.save()

        product.tags.set(tag_objs)
        return ApiResponse(product)

    def patch(self, request, pk=None):
        '''Edits some fields of an existing product.
        Parameters: Same as in POST /products.
        '''

        try:
            product = Product.objects.get(pk=pk)
        except (Product.DoesNotExist, ValueError):
            return ApiMessage(f'Product with id {pk} not found.', status=404)

        name = request.data.get('name')
        description = request.data.get('description')
        category = request.data.get('category')
        tags = request.data.getlist('tags')

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        if category is not None:
            product.category = category

        if tags:
            tag_objs = [ProductTag(tag=tag) for tag in tags]
            for t in tag_objs:
                t.save()

            product.tags.set(tag_objs)

        try:
            product.full_clean()
            product.save()
        except (ValidationError, IntegrityError):
            return ApiMessage('Data format is invalid', status=400)

        return ApiResponse(product)
