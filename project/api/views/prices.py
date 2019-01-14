from datetime import datetime

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View

from django.conf import settings

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from project.api.models import Price, Product, Shop


#################################################################
## helper functions

ALLOWED_SORT_FIELDS = ['geoDist', 'price', 'date']
ALLOWED_SORT_TYPE = ['ASC', 'DESC']

def JSON_RESPONSE(data, status=200):
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=status)


def JSON_RESPONSE_400(msg):
    return JSON_RESPONSE({'status': msg}, status=400)

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

        start = request.GET.get('start', start_default)
        count = request.GET.get('count', count_default)

        geo_dist = request.GET.get('geoDist', None)
        geo_lng = request.GET.get('geoLng', None)
        geo_lat = request.GET.get('geoLat', None)

        date_from = request.GET.get('dateFrom', None)
        date_to = request.GET.get('dateTo', None)

        shops = request.GET.getlist('shops', None)
        products = request.GET.getlist('products', None)
        tags = request.GET.getlist('tags', None)

        sort = request.GET.getlist('sort', sort_default)

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
            return JSON_RESPONSE_400('Το `start` πρεπει να ειναι θετικος ακεραιος')

        # count
        try:
            count = int(count)
            if count < 0:
                raise ValueError()
        except ValueError:
            return JSON_RESPONSE_400('Το `count` πρεπει να ειναι θετικος ακεραιος')

        # geolocation checks
        if (geo_dist or geo_lat or geo_lng) is not None:
            if  (geo_dist and geo_lat and geo_lng) is None:
                return JSON_RESPONSE_400('Tα `geoDist`, `geoLng` και `geoLat` πρεπει να οριζονται μαζι')

            # distance
            try:
                geo_dist = int(geo_dist)
                if geo_dist < 0:
                    raise ValueError()
            except ValueError:
                return JSON_RESPONSE_400('Το `geo_dist` πρεπει να ειναι θετικος ακεραιος')

            # latitude
            try:
                geo_lat = float(geo_lat)
                if not (-90 <= geo_lat <= 90):
                    raise ValueError()
            except ValueError:
                return JSON_RESPONSE_400('Το `geo_lat` δεν ειναι εγκυρο')

            # lοngitude
            try:
                geo_lng = float(geo_lng)
                if not (-180 <= geo_lng <= 180):
                    raise ValueError()
            except ValueError:
                return JSON_RESPONSE_400('Το `geo_lng` δεν ειναι εγκυρο')

            geo_filter = True

        # date checks
        if (date_from or date_to) is None:
            date_from = datetime.now()
            date_to = date_from
        else:
            if (date_from and date_to) is None:
                return JSON_RESPONSE_400('Τα `dateFrom` και `dateTo` πρεπει να οριζονται μαζι')

            try:
                date_from = Price.parse_date(date_from)
                date_to = Price.parse_date(date_to)

                if not Price.check_dates(date_from, date_to):
                    return JSON_RESPONSE_400('Το `dateFrom` πρεπει να ειναι παλαιοτερο του `dateTo`')
            except ValueError:
                return JSON_RESPONSE_400('Οι ημερομηνίες πρέπει να είναι EEEE-MM-HH')

        # shop ids checks
        if shops is not None:
            try:
                shops = list({int(x) for x in shops})                   # keep unique
                shop_ids_filter = True
            except ValueError:
                return JSON_RESPONSE_400('To `shops` πρεπει να ειναι λιστα ακεραιων')

        # product ids checks
        if products is not None:
            try:
                products = list({int(x) for x in products})             # keep unique
                product_ids_filter = True
            except ValueError:
                return JSON_RESPONSE_400('To `products` πρεπει να ειναι λιστα ακεραιων')

        # tags checks
        if tags is not None:
            try:
                tags = list({str(x) for x in tags})                     # keep unique
                tags_filter = True
            except ValueError:
                return JSON_RESPONSE_400('To `tags` πρεπει να ειναι λιστα απο tags')

        ########################################################################
        ## querying
        ########################################################################
        prices = Price.objects.all()

        if shop_ids_filter:
            prices = prices.filter(shop__pk__in=shops)

        if product_ids_filter:
            prices = prices.filter(product__pk__in=products)

        if tags_filter:
            shops_with_tags = Shop.objects.with_tags(tags)
            products_with_tags = Product.objects.with_tags(tags)

            prices_with_shop_tags = prices.filter(shop__in=shops_with_tags)
            prices_with_product_tags = prices.filter(product__in=products_with_tags)

            prices = prices_with_shop_tags.union(prices_with_product_tags)

        if date_filter:
            # set1: prices that end between [dateFrom, dateTo]
            # set2: prices that start between [dateFrom, dateTo]
            # set3: prices that contain [dateFrom, dateTo]

            prices_set1 = prices.filter(date_to__gte=date_from, date_to__lte=date_to)
            prices_set2 = prices.filter(date_from__gte=date_from, date_from__lte=date_to)
            prices_set3 = prices.filter(date_from__lte=date_from, date_to__gte=date_to)

            prices = prices_set1.union(prices_set2, prices_set3)

        if geo_filter:
            shops_within_distance = Shop.objects.within_distance_from(geo_lat, geo_lng, km=geo_dist)

            prices = prices.filter(shop__in=shops_within_distance)
            prices = prices.annotate(geoDist=Distance('shop__coordinates', Point(geo_lng, geo_lat, srid=4326)))


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
                    return JSON_RESPONSE_400(f'Αγνωστο κριτηριο ταξινομησης {sort_field}')
                elif sort_field in sort_fields:
                    return JSON_RESPONSE_400(f'Το κριτηριο ταξινομησης {sort_field} εμφανιζεται πανω απο μια φορες')
                elif sort_type not in ALLOWED_SORT_TYPE:
                    return JSON_RESPONSE_400(f'Μη εγκυρος τροπος ταξινομησης {sort_field}|{sort_type}')

                sort_fields.append(sort_field)

                if sort_field == 'date':
                    sort_field = 'date_from'
                if sort_type == 'DESC':
                    sort_field = f'-{sort_field}'

                order_by_args.append(sort_field)
            except ValueError:
                JSON_RESPONSE_400(f'Μη εγκυρο κριτηριο ταξινομησης {x}')

        # do the actual sorting
        prices = prices.order_by(*order_by_args)

        ########################################################################
        ## paging
        ## NOTE: django pagination does not allow arbitrary `start` and `count`
        ## Just slice the objects properly
        ########################################################################
        total = prices.count()

        if total >= start + count:
            prices = prices[start:(start+count)]
        elif total >= start:
            prices = prices[start:]
        else:
            prices = Price.objects.none()

        ########################################################################
        ## bake json
        ########################################################################

        # structure
        result = dict(start=start, count=count, total=total, prices=[])

        # items
        for price in prices:
            shop_distance = None
            if geo_filter:
                shop_distance = Distance(Point(geo_lng, geo_lat), price.shop.coordinates)

            result['prices'].append(dict(
                price=price.price,
                date=price.dateFrom.strftime('%Y-%m-%d'),
                productName=price.product.name,
                productId=price.product.id,                             # FIXME: when it comes
                productTags=[str(x) for x in price.product.tags.all()], # FIXME?
                shopId=price.shop.id,
                shopName=price.shop.name,
                shopTags=[str(x) for x in price.shop.tags.all()],       # FIXME?
                shopAddress=price.shop.address,
                shopDist=shop_distance
            ))

        ########################################################################
        ## its over, its done
        ########################################################################
        return JSON_RESPONSE(result)


    # POST /observatory/api/prices/
    def post(self, request):
        # not authenticated == anonymous.
        # FIXME: explicitly check that user is a volunteer/admin?
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return HttpResponseForbidden()

        try:
            # TODO: how do we handle NULL `date_to` field? `3000-12-12` seems like a good workaround
            args = dict(
                shop=Shop.objects.get(pk=int(request.POST.get('shopId'))),
                product=Product.objects.get(pk=int(request.POST.get('productId'))),
                price=float(request.POST.get('price')),
                date_from=Price.parse_date(request.POST.get('dateFrom')),
                date_to=Price.parse_date(request.POST.get('dateTo')),
                user=request.user
            )

            # try creating new price
            if not Price.add_price(**args):
                return HttpResponseBadRequest()

        except Exception as e:
            # if settings.DEBUG:
            # print(e.__class__.__name__, e)

            # FIXME: what if something happened on our end?
            return HttpResponseBadRequest()

        # all ok
        # return 201, resource created
        return HttpResponse(status=201)
