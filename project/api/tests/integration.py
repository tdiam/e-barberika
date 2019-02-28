import requests

from django.test import LiveServerTestCase

########################################################################
# URLS
########################################################################

# urls
api_root = '/observatory/api/'
urls = {
    'register': api_root + 'register/',
    'login': api_root + 'login/',
    'logout': api_root + 'logout/',

    'products': api_root + 'products/',
    'shops': api_root + 'shops/',
    'prices': api_root + 'prices/',
}

########################################################################
# TEST DATA
########################################################################

# test product data
products_data = {
    1: {
        'name':         'Προϊόν Στα Ελληνικά',
        'description':  'περιγραφή με κείμενο και αλλα',
        'category':     'κατηγορια',
        'tags':         ['Tags', 'of', 'first', 'ελληνικα', 'ταγκς'],
        'withdrawn':    False
    },
    2: {
        'name':         'SecondProduct',
        'description':  'SecondDescription',
        'category':     'SecondCategory',
        'tags':         ['Tags', 'of', 'second', 'Product'],
        'withdrawn':    False
    },
    3: {
        'name':         'ProductName',
        'description':  'ProductDescription',
        'category':     'FirstCategory',
        'tags':         ['Tags', 'of', 'first', 'Product'],
        'withdrawn':    False
    }
}

products = {
    1: {'id': 1, **products_data[1]},
    2: {'id': 2, **products_data[2]},
    3: {'id': 1, **products_data[3]}
}

products_list = {
    'start':    0,
    'count':    10,
    'total':    2,
    'products': [products[1], products[2]]
}

# test shop data
shops_data = {
    1: {
        'name':         'FirstShop',
        'address':      'AddressOfFirstShop',
        'lat':          37.97864720247794,
        'lng':          23.78350140530576,
        'tags':         ['Tags', 'of', 'first', 'shop'],
        'withdrawn':    False
    },
    2: {
        'name':         'SecondShop',
        'address':      'AddressOfSecondShop',
        'lat':          37.98136303504576,
        'lng':          23.78413117565094,
        'tags':         ['Tags', 'of', 'second', 'shop'],
        'withdrawn':    False
    },
    3: {
        'name':         'OtherShop',
        'address':      'OtherAddress',
        'lat':          37.97864720247794,
        'lng':          23.78350140530576,
        'tags':         ['Tags', 'of', 'first', 'shop'],
        'withdrawn':    False
    }
}

shops = {
    1: {'id': 1, **shops_data[1]},
    2: {'id': 2, **shops_data[2]},
    3: {'id': 1, **shops_data[3]}       # 3 == '1 updated'
}

shops_list = {
    'start': 0,
    'count': 10,
    'total': 2,
    'shops': [shops[1], shops[2]]
}

# user info
user = {
    'username': 'michaelscott',
    'password': 'ohhowtheturntables',
}

# empty headers, will be updated with token
headers = {}

########################################################################
# TEST DEFINITION
########################################################################

class IntegrationTests:
    '''
    acts as a wrapper class, so that integration tests will not run along
    with the unit tests
    '''

    class IntegrationTests(LiveServerTestCase):
        '''Created as a LiveServerTestCase, which spawns a live server'''

        ########################################################################
        # TEST SENARIO
        ########################################################################
        def test_client(self):
            '''integration tests, based on test client'''

            # register and login
            self.runTest('user_registers') # extra
            self.runTest('user_logs_in')

            # products
            self.runTest('user_adds_two_products')
            self.runTest('user_lists_the_products')
            self.runTest('user_updates_a_product')
            self.runTest('user_gets_a_product')
            self.runTest('user_deletes_a_product')

            # shops
            self.runTest('user_adds_two_shops')
            self.runTest('user_lists_the_shops')
            self.runTest('user_updates_a_shop')
            self.runTest('user_gets_a_shop')
            self.runTest('user_deletes_a_shop')

            # logout
            self.runTest('user_logs_out')

        ########################################################################
        # UTILITY FUNCTIONS
        ########################################################################

        def runTest(self, testName):
            '''run action `testName`, while printing a good informative message'''
            with self.subTest(testName):
                print(testName.ljust(40, '.'), end='')
                getattr(self, testName)()

                # if we reach this, test `testName` has passed
                print('OK')

        def assertShopsEqual(self, shop_1, shop_2):
            '''check that two shops are equal (equality check is not good enough, tags may be in different order'''
            self.assertEqual(set(shop_1['tags']), set(shop_2['tags']))
            for field in ['id', 'address', 'lat', 'lng', 'name', 'withdrawn']:
                self.assertEqual(shop_1[field], shop_2[field])

            # assert that returned shop has no other fields
            for field in shop_1:
                self.assertIn(field, shop_2.keys())

        def assertProductsEqual(self, prod_1, prod_2):
            '''check that two products are equal (equality check is not good enough, tags may be in different order'''
            # special check for tags, because their order may change
            self.assertEqual(set(prod_1['tags']), set(prod_2['tags']))
            for field in ['id', 'category', 'description', 'name', 'withdrawn']:
                self.assertEqual(prod_1[field], prod_2[field])

            # assert that returned shop has no other fields
            for field in prod_1:
                self.assertIn(field, prod_2.keys())

        ########################################################################
        # INDIVIDUAL USER TESTS
        ########################################################################

        def user_registers(self):
            '''a new user registers'''
            r = requests.post(self.live_server_url + urls['register'], data={
                'username': user['username'],
                'password': user['password'],
            })

            self.assertEqual(r.status_code, 200)

        def user_logs_in(self):
            '''user logs in after registering'''
            r = requests.post(
                self.live_server_url + urls['login'],
                data=user
            )

            self.assertEqual(r.status_code, 200)

            # update data
            headers['x-observatory-auth'] = r.json()['token']

        def user_logs_out(self):
            '''user logs out'''
            r = requests.post(
                self.live_server_url + urls['logout'],
                headers=headers
            )
            self.assertEqual(r.status_code, 200)

            # make sure that token is no longer valid
            # try deleting something
            r = requests.delete(
                self.live_server_url + urls['shops'] + '1/',
                headers=headers
            )
            self.assertEqual(r.status_code, 401)

            # make sure that shop was not deleted
            r = requests.get(self.live_server_url + urls['shops'] + '1')
            self.assertEqual(r.status_code, 200)
            self.assertShopsEqual(r.json(), shops[3])

        ########################################################################
        # INDIVIDUAL SHOP TESTS
        ########################################################################

        def user_adds_two_shops(self):
            '''user adds two shops, we make sure that they are added properly'''
            for shop in [1, 2]:
                shop_data = shops_data[shop]

                r = requests.post(
                    self.live_server_url + urls['shops'],
                    data=shop_data,
                    headers=headers
                )
                self.assertEqual(r.status_code, 200)

                # get the newly created shop
                r = requests.get(self.live_server_url + urls['shops'] + str(shop))
                self.assertEqual(r.status_code, 200)
                self.assertShopsEqual(r.json(), shops[shop])

        def user_lists_the_shops(self):
            '''user lists the two shops, we make sure that response is ok'''
            r = requests.get(
                self.live_server_url + urls['shops'],
                data={'start': 0, 'count': 10, 'status': 'ACTIVE', 'sort': 'id|ASC'}
            )
            self.assertEqual(r.status_code, 200)
            response = r.json()

            # check paging
            for field in ['start', 'count', 'total']:
                self.assertEqual(response[field], shops_list[field])

            # check shops
            self.assertEqual(len(response['shops']), len(shops_list['shops']))
            for x, y in zip(response['shops'], shops_list['shops']):
                self.assertShopsEqual(x, y)

        def user_updates_a_shop(self):
            '''user updates shop 1 with data from shop 3'''
            r = requests.put(
                self.live_server_url + urls['shops'] + '1/',
                data=shops_data[3],
                headers=headers
            )
            self.assertEqual(r.status_code, 200)

            r = requests.get(self.live_server_url + urls['shops'] + '1')
            self.assertEqual(r.status_code, 200)
            response = r.json()

            self.assertShopsEqual(response, shops[3])

        def user_gets_a_shop(self):
            '''user asks for shop 1, check that data was returned ok'''
            r = requests.get(self.live_server_url + urls['shops'] + '1')
            self.assertEqual(r.status_code, 200)
            self.assertShopsEqual(r.json(), shops[3])

        def user_deletes_a_shop(self):
            '''user deletes shop 2'''
            r = requests.delete(
                self.live_server_url + urls['shops'] + '2',
                headers=headers
            )
            self.assertEqual(r.status_code, 200)

            # check that shop is withdrawn
            r = requests.get(self.live_server_url + urls['shops'] + '2')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()['withdrawn'], True)


        ########################################################################
        # INDIVIDUAL PRODUCT TESTS
        ########################################################################

        def user_adds_two_products(self):
            '''user adds two products, we make sure that they are added properly'''
            for product in [1, 2]:
                product_data = products_data[product]

                r = requests.post(
                    self.live_server_url + urls['products'],
                    data=product_data,
                    headers=headers
                )
                self.assertEqual(r.status_code, 200)

                # get the newly created product
                r = requests.get(self.live_server_url + urls['products'] + str(product))
                self.assertEqual(r.status_code, 200)
                self.assertProductsEqual(r.json(), products[product])

        def user_lists_the_products(self):
            '''user lists the two products, we make sure that response is ok'''
            r = requests.get(
                self.live_server_url + urls['products'],
                data={'start': 0, 'count': 10, 'status': 'ACTIVE', 'sort': 'id|ASC'}
            )
            self.assertEqual(r.status_code, 200)
            response = r.json()

            # check paging
            for field in ['start', 'count', 'total']:
                self.assertEqual(response[field], products_list[field])

            # check products
            self.assertEqual(len(response['products']), len(products_list['products']))
            for x, y in zip(response['products'], products_list['products']):
                self.assertProductsEqual(x, y)

        def user_updates_a_product(self):
            '''user updates product 1 with data from product 3'''
            r = requests.put(
                self.live_server_url + urls['products'] + '1/',
                data=products_data[3],
                headers=headers
            )
            self.assertEqual(r.status_code, 200)

            r = requests.get(self.live_server_url + urls['products'] + '1')
            self.assertEqual(r.status_code, 200)
            response = r.json()

            self.assertProductsEqual(response, products[3])

        def user_gets_a_product(self):
            '''user asks for product 1, check that data was returned ok'''
            r = requests.get(self.live_server_url + urls['products'] + '1')
            self.assertEqual(r.status_code, 200)
            self.assertProductsEqual(r.json(), products[3])

        def user_deletes_a_product(self):
            '''user deletes product 2'''
            r = requests.delete(
                self.live_server_url + urls['products'] + '2',
                headers=headers
            )
            self.assertEqual(r.status_code, 200)

            # check that product is withdrawn
            r = requests.get(self.live_server_url + urls['products'] + '2')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()['withdrawn'], True)
