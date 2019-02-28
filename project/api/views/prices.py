from datetime import datetime

from django.http import HttpResponse
from django.views import View
from django.db.models import Q

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator

from project.api.models import Price, Product, Shop

from project.api.helpers import ApiResponse, ApiMessage, volunteer_required


#################################################################
## helpers

ALLOWED_SORT_FIELDS = ['geoDist', 'price', 'date']
ALLOWED_SORT_TYPE = ['ASC', 'DESC']

def ApiMessage400(x):
    return ApiMessage(x, status=400)

#################################################################


class PricesView(View):

    # GET observatory/api/prices
    def get(self, request):
        ######################################################################
        ## defaults
        ######################################################################

        start_default = 0
        count_default = 20
        sort_default = ['price|ASC']

        ######################################################################
        ## parsing url params
        ######################################################################

        start = request.data.get('start', start_default)
        count = request.data.get('count', count_default)

        geo_dist = request.data.get('geoDist', None)
        geo_lng = request.data.get('geoLng', None)
        geo_lat = request.data.get('geoLat', None)

        date_from = request.data.get('dateFrom', None)
        date_to = request.data.get('dateTo', None)

        shops = request.data.getlist('shops', None)
        products = request.data.getlist('products', None)
        tags = request.data.getlist('tags', None)

        sort = request.data.getlist('sort', sort_default)

        ######################################################################
        ## filters to apply, none by default
        ######################################################################

        geo_filter = False                  # only if `geoXXXX` is passed
        date_filter = True                  # always on
        shop_ids_filter = False             # only if `shops` is passed
        product_ids_filter = False          # only if `products` is passed
        tags_filter = False                 # only if `tags` is passed

        ######################################################################
        ## check url parameters format
        ## FUTURE: in an ideal world, all fields are checked and multiple
        ##         error messages are returned. not today :)
        ######################################################################

        # start
        try:
            start = int(start)
            if start < 0:
                raise ValueError()
        except ValueError:
            return ApiMessage400('Το `start` πρεπει να ειναι θετικος ακεραιος')

        # count
        try:
            count = int(count)
            if count < 0:
                raise ValueError()
        except ValueError:
            return ApiMessage400('Το `count` πρεπει να ειναι θετικος ακεραιος')

        # geolocation checks
        if (geo_dist or geo_lat or geo_lng) is not None:
            if  (geo_dist and geo_lat and geo_lng) is None:
                return ApiMessage400('Tα `geoDist`, `geoLng` και `geoLat` πρεπει να οριζονται μαζι')

            # distance
            try:
                geo_dist = int(geo_dist)
                if geo_dist < 0:
                    raise ValueError()
            except ValueError:
                return ApiMessage400('Το `geoDist` πρεπει να ειναι θετικος ακεραιος')

            # latitude
            try:
                geo_lat = float(geo_lat)
                if not (-90 <= geo_lat <= 90):
                    raise ValueError()
            except ValueError:
                return ApiMessage400('Το `geoLat` δεν ειναι εγκυρο')

            # lοngitude
            try:
                geo_lng = float(geo_lng)
                if not (-180 <= geo_lng <= 180):
                    raise ValueError()
            except ValueError:
                return ApiMessage400('Το `geoLng` δεν ειναι εγκυρο')

            geo_point = Point(geo_lng, geo_lat, srid=4326)
            geo_filter = True

        # date checks
        if (date_from or date_to) is None:
            date_from = datetime.now()
            date_to = date_from
        else:
            if (date_from and date_to) is None:
                return ApiMessage400('Τα `dateFrom` και `dateTo` πρεπει να οριζονται μαζι')

            try:
                date_from = Price.parse_date(date_from)
                date_to = Price.parse_date(date_to)

                if not Price.check_dates(date_from, date_to):
                    return ApiMessage400('Το `dateFrom` πρεπει να ειναι παλαιοτερο του `dateTo`')
            except ValueError:
                return ApiMessage400('Οι ημερομηνίες πρέπει να είναι EEEE-MM-HH')

        # shop ids checks
        if shops:
            try:
                shops = list({int(x) for x in shops})                   # keep unique
                shop_ids_filter = True
            except ValueError:
                return ApiMessage400('To `shops` πρεπει να ειναι λιστα ακεραιων')

        # product ids checks
        if products:
            try:
                products = list({int(x) for x in products})             # keep unique
                product_ids_filter = True
            except ValueError:
                return ApiMessage400('To `products` πρεπει να ειναι λιστα ακεραιων')

        # tags checks
        if tags:
            try:
                tags = list({str(x) for x in tags})                     # keep unique
                tags_filter = True
            except ValueError:
                return ApiMessage400('To `tags` πρεπει να ειναι λιστα απο tags')

        ########################################################################
        ## querying
        ########################################################################
        prices = Price.objects.all()

        if shop_ids_filter:
            prices = prices.filter(shop__id__in=shops)

        if product_ids_filter:
            prices = prices.filter(product__id__in=products)

        if tags_filter:
            shops_with_tags = Shop.objects.with_tags(tags)
            products_with_tags = Product.objects.with_tags(tags)

            # this could be a model method :)
            prices = prices.filter(
                Q(shop__in=shops_with_tags)
                | Q(product__in=products_with_tags))

        if date_filter:
            # this could be a model method :)
            prices = prices.filter(
                Q(date_to__gte=date_from, date_to__lte=date_to)
                | Q(date_from__gte=date_from, date_from__lte=date_to)
                | Q(date_from__lte=date_from, date_to__gte=date_to))

        if geo_filter:
            shops_within_distance = Shop.objects.within_distance_from(geo_lat, geo_lng, km=geo_dist)
            prices = prices.filter(shop__in=shops_within_distance)
            prices = prices.annotate(geoDist=Distance('shop__coordinates', geo_point))

        ########################################################################
        ## sorting
        ########################################################################
        sort_fields = []
        # sort = [str(x) for x in sort]

        order_by_args = []
        for x in sort:
            try:
                sort_field, sort_type = x.split('|')

                if sort_field not in ALLOWED_SORT_FIELDS:
                    return ApiMessage400(f'Αγνωστο κριτηριο ταξινομησης {sort_field}')
                if sort_field in sort_fields:
                    return ApiMessage400(f'Το κριτηριο ταξινομησης {sort_field} εμφανιζεται πανω απο μια φορες')
                if sort_type not in ALLOWED_SORT_TYPE:
                    return ApiMessage400(f'Μη εγκυρος τροπος ταξινομησης {sort_field}|{sort_type}')
                if sort_type == 'geoDist' and not geo_filter:
                    return ApiMessage400(f'Μη εγκυρος τροπος ταξινομησης {sort_field}|{sort_type}, δεν εχει δοθει σημειο αναφορας')

                sort_fields.append(sort_field)

                if sort_field == 'date':
                    sort_field = 'date_from'
                if sort_type == 'DESC':
                    sort_field = f'-{sort_field}'

                order_by_args.append(sort_field)
            except ValueError:
                ApiMessage400(f'Μη εγκυρο κριτηριο ταξινομησης {x}')

        # do the actual sorting
        prices = prices.order_by(*order_by_args)

        ########################################################################
        ## paging
        ## NOTE: django pagination does not allow arbitrary `start` and `count`
        ## Just slice the objects properly
        ########################################################################
        total = prices.count()
        prices = prices[start:(start+count)]

        ########################################################################
        ## bake json
        ########################################################################

        # structure
        result = dict(start=start, count=count, total=total, prices=[])

        # items
        for price in prices:
            shop_distance = None
            if geo_filter:
                shop_distance = price.geoDist.km

            result['prices'].append(dict(
                price=float(price.price),
                date=Price.convert_to_str(price.date_from),
                productName=price.product.name,
                productId=price.product.id,
                productTags=[str(x) for x in price.product.tags.all()],
                shopId=price.shop.id,
                shopName=price.shop.name,
                shopTags=[str(x) for x in price.shop.tags.all()],
                shopAddress=price.shop.address,
                shopDist=shop_distance
            ))

        ########################################################################
        ## its over, its done
        ########################################################################
        return ApiResponse(result)


    # POST /observatory/api/prices/
    @method_decorator(volunteer_required)
    def post(self, request):
        args = {
            'user': request.user
        }

        try:
            shop_id = request.data.get('shopId')
            args['shop'] = Shop.objects.get(pk=int(shop_id))
        except (TypeError, ValueError, Shop.DoesNotExist):
            return ApiMessage400(f'Μη έγκυρο shopId: {shop_id}')

        try:
            product_id = request.data.get('productId')
            args['product'] = Product.objects.get(pk=int(product_id))
        except (TypeError, ValueError, Product.DoesNotExist):
            return ApiMessage400(f'Μη έγκυρο productId: {product_id}')

        try:
            price = request.data.get('price')
            args['price'] = float(price)
        except (TypeError, ValueError):
            return ApiMessage400(f'Μη έγκυρη τιμή προϊόντος: {price}')

        try:
            date_from = request.data.get('dateFrom')
            args['date_from'] = Price.parse_date(date_from)
        except (TypeError, ValueError):
            return ApiMessage400(f'Μη έγκυρη μορφή ημερομηνίας: {date_from}')

        try:
            date_to = request.data.get('dateTo')
            args['date_to'] = Price.parse_date(date_to)
        except (TypeError, ValueError):
            return ApiMessage400(f'Μη έγκυρη μορφή ημερομηνίας: {date_to}')

        # try creating new price
        p = Price.add_price(**args)

        if p is None:
            return ApiMessage400('Ήταν αδύνατη η πρόσθεση της πληροφορίας στο σύστημα')

        # all ok
        # return 200, resource created
        return ApiResponse({
            'id': p.id,
            'dateFrom': Price.convert_to_str(p.date_from),
            'dateTo': Price.convert_to_str(p.date_to),
            'productId': p.product.id,
            'shopId': p.shop.id,
            'price': p.price
        }, status=200)
