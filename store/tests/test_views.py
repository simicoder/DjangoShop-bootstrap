from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Category, ProductImage
import json

class TestViews(TestCase):

	def setUp(self):
		self.client = Client()
		self.home_url = reverse('store:home_view')
		self.create_product_url = reverse('store:create_view')


	def test_home_view_GET(self):
		response = self.client.get(self.home_url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'store/home.html')


	def test_product_creates_POST(self):
		Category.objects.create(name = "dev")

		response = self.client.post(self.create_product_url, {
			'title': 'title',
			'price': 20,
			'description': 'des',
			'seller': 'admin',
			'category': 'dev'
			})

		self.assertEquals(response.status_code, 302)

