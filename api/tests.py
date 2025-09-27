from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Product, Category, Order, ShippingAddress
from api.serializers import UserSerializer, ProductSerializer, OrderSerializer
from api import views
from api import auth
from rest_framework.test import APIRequestFactory


class TestViews(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='testuser@example.com',
            password='password123',
            first_name='Test'
        )
        self.client.login(email='testuser@example.com', password='password123')

        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            is_featured=True,
            description="",
            slug="",
            price=100,
            stock=100,
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_view(self):
        tkn = auth.get_tokens_for_user(self.user)['access']

        headers = {
            'AUTHORIZATION': f'Bearer {tkn}'
        }

        response = self.client.get(
            reverse('user_profile', kwargs={'pk': self.user.id}), headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'New',
        }
        response = self.client.post(reverse('register_user'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_featured_products_view(self):
        response = self.client.get(reverse('featured_products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['results']  # type:ignore
        product_name = self.product.name
        self.assertIn(
            product_name, [prod['name'] for prod in data]
        )

    def test_product_view_set(self):
        response = self.client.get(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = {
            'name': 'Test Product',
            'is_featured': True,
            'description': "Test description",
            'slug': "test-product",
            'price': 100,
            'stock': 100,
            'category': self.category
        }

        tkn = auth.get_tokens_for_user(self.user)['access']

        headers = {
            'AUTHORIZATION': f'Bearer {tkn}'
        }

        response = self.client.post(
            reverse('products-list'), data=product_data, headers=headers)

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_view_set(self):
        response = self.client.get(reverse('categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_view_set(self):
        shipping_address = ShippingAddress.objects.create(
            address='123 Test St',
            city='Test City',
            state='Test State',
            zip_code='12345'
        )
        order_data = {
            'products': [{'product_id': self.product.id, 'quantity': 1}],
            'shipping_address': {
                'address': shipping_address.address,
                'city': shipping_address.city,
                'state': shipping_address.state,
                'zip_code': shipping_address.zip_code
            }
        }

        tkn = auth.get_tokens_for_user(self.user)['access']

        headers = {
            'AUTHORIZATION': f'Bearer {tkn}'
        }

        response = self.client.post(
            reverse('orders-list'), order_data, headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
