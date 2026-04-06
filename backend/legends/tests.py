from django.test import TestCase
from rest_framework.test import APIClient
from .models import Legend
from .serializers import LegendSerializer

class LegendModelTest(TestCase):
    def test_create_legend_with_new_fields(self):
        legend = Legend.objects.create(
            name="AristotleModel",
            description="Philosopher",
            biography="Ancient Greek philosopher and scientist.",
            lang="el"
        )
        self.assertEqual(legend.biography, "Ancient Greek philosopher and scientist.")
        self.assertEqual(legend.lang, "el")
        self.assertEqual(legend.slug, "aristotlemodel")

class LegendSerializerTest(TestCase):
    def test_serializer_contains_new_fields(self):
        legend = Legend.objects.create(
            name="AristotleSerializer",
            description="Philosopher",
            biography="Ancient Greek philosopher and scientist.",
            lang="el"
        )
        serializer = LegendSerializer(instance=legend)
        data = serializer.data
        self.assertEqual(data['name'], "AristotleSerializer")
        self.assertEqual(data['description'], "Philosopher")
        self.assertEqual(data['biography'], "Ancient Greek philosopher and scientist.")
        self.assertEqual(data['lang'], "el")

class LegendApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Legend.objects.create(
            name="AristotleApi",
            description="Philosopher",
            biography="Ancient Greek philosopher and scientist.",
            lang="el"
        )

    def test_list_legends_contains_new_fields(self):
        response = self.client.get('/api/setting/legends')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        aristotle = next(item for item in data if item['name'] == 'AristotleApi')
        self.assertEqual(aristotle['biography'], "Ancient Greek philosopher and scientist.")
        self.assertEqual(aristotle['lang'], "el")
