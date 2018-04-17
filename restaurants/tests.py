from django.test import TestCase
from django.urls import reverse
from restaurants.models import Restaurant
from restaurants.forms import RestaurantForm

class RestaurantModelTestCase(TestCase):
    def test_create(self):
        Restaurant.objects.create(
            name="Hamza's Pizza",
            description="Pizza that tastes really good.",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png",
            )

class RestaurantViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            "name": "Hamza's Pizza",
            "description": "Pizza that tastes really good.",
            "opening_time": "00:01:00",
            "closing_time":"23:59:00",
            "logo":"http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
        }
        self.restaurant_1 = Restaurant.objects.create(
            name="Restaurant 1",
            description="This is Restaurant 1",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.restaurant_2 = Restaurant.objects.create(
            name="Restaurant 2", 
            description="This is Restaurant 2",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.restaurant_3 = Restaurant.objects.create(
            name="Restaurant 3",
            description="This is Restaurant 3",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )

    def test_list_view(self):
        list_url = reverse("restaurant-list")
        response = self.client.get(list_url)
        for restaurant in Restaurant.objects.all():
            self.assertIn(restaurant, response.context['restaurants'])
            self.assertContains(response, restaurant.name)
            self.assertContains(response, restaurant.description)
            self.assertContains(response, restaurant.logo.url)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        detail_url = reverse("restaurant-detail", kwargs={"restaurant_id":self.restaurant_1.id})
        response = self.client.get(detail_url)
        self.assertEqual(self.restaurant_1, response.context['restaurant'])
        self.assertContains(response, self.restaurant_1.name)
        self.assertContains(response, self.restaurant_1.description)
        self.assertContains(response, self.restaurant_1.logo.url)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        create_url = reverse("restaurant-create")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(create_url, self.data)
        self.assertEqual(response2.status_code, 302)

    def test_update_view(self):
        update_url = reverse("restaurant-update", kwargs={"restaurant_id":self.restaurant_1.id})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(update_url, data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        delete_url = reverse("restaurant-delete", kwargs={"restaurant_id":self.restaurant_1.id})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)


class RestaurantFormTestCase(TestCase):
    def test_valid_form(self):
        name = "Some random restaurant"
        description = "Some random description"
        opening_time = "12:15"
        closing_time = "10:15"
        logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
        data = {
            'name':name,
            'description': description,
            'opening_time': opening_time,
            'closing_time': closing_time,
            'logo': logo,
        }
        form = RestaurantForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), name)
        self.assertEqual(form.cleaned_data.get('description'), description)

    def test_invalid_form(self):
        name = "Some restaurant"
        description = "Some random description"
        data = {
            'name':name,
            'description': description,
        }
        form = RestaurantForm(data=data)
        self.assertFalse(form.is_valid())
