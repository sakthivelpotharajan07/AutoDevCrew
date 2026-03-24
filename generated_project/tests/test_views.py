Python

import unittest
from django.test import TestCase, Client
from django.urls import reverse
from cake_ordering.models import Cake, Order

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.cake1 = Cake.objects.create(name='Chocolate', description='Delicious Chocolate Cake', price=20.0)
        self.order1 = Order.objects.create(name='John Doe', email='john@example.com', phone='1234567890', cake=self.cake1)

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_cake_list_view(self):
        url = reverse('cake_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cake_list.html')

    def test_cake_detail_view(self):
        url = reverse('cake_detail', args=[self.cake1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cake_detail.html')

    def test_order_view(self):
        url = reverse('order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

    def test_order_post_view(self):
        url = reverse('order')
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '9876543210',
            'cake': self.cake1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_success'))

    def test_order_success_view(self):
        url = reverse('order_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_success.html')