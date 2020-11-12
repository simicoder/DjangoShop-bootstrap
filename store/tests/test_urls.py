from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import home_view

class TestUrls(SimpleTestCase):

	def test_url_is_resolved(self):
		url = reverse('store:home_view')
		print(url)
		self.assertEquals(resolve(url).func, home_view)