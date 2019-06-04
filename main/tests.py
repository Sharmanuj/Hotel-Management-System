from django.test import TestCase
from django.urls import reverse

# Create your tests here.

from .views import *
from main.models import Staff,Customer,RoomType,Facility

class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Customer.objects.create(first_name='Anuj', middle_name='Sharma', last_name='Bhardwaj', address='faltu',email_address = 'a@gmail.com',contact_no = '1234567890')

    def test_first_name(self):
        customer = Customer.objects.get(first_name="Anuj")
        self.assertEquals(customer.first_name, 'Anuj')

    def test_middle_name(self):
        customer = Customer.objects.get(middle_name="Sharma")
        self.assertEquals(customer.middle_name, 'Sharma')

    def test_last_name(self):
        customer = Customer.objects.get(last_name="Bhardwaj")
        self.assertEquals(customer.last_name, 'Bhardwaj')

    def test_contact_no(self):
        customer = Customer.objects.get(contact_no="1234567890")
        self.assertEquals(customer.contact_no, '1234567890')

    def test_address(self):
        customer = Customer.objects.get(address="faltu")
        self.assertEquals(customer.address,'faltu')


    def test_email_address(self):
        customer = Customer.objects.get(email_address="a@gmail.com")
        self.assertEquals(customer.email_address,'a@gmail.com')


class StaffModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Staff.objects.create(first_name='Anuj', middle_name='Sharma', last_name='Bhardwaj', address='faltu',email_address = 'a@gmail.com',contact_no = '1234567890')

    def test_first_name(self):
        staff = Staff.objects.get(first_name="Anuj")
        self.assertEquals(staff.first_name, 'Anuj')

    def test_middle_name(self):
        staff = Staff.objects.get(middle_name="Sharma")
        self.assertEquals(staff.middle_name, 'Sharma')

    def test_last_name(self):
        staff = Staff.objects.get(last_name="Bhardwaj")
        self.assertEquals(staff.last_name, 'Bhardwaj')

    def test_contact_no(self):
        staff = Staff.objects.get(contact_no="1234567890")
        self.assertEquals(staff.contact_no, '1234567890')

    def test_address(self):
        staff = Staff.objects.get(address="faltu")
        self.assertEquals(staff.address,'faltu')


    def test_email_address(self):
        staff = Staff.objects.get(email_address="a@gmail.com")
        self.assertEquals(staff.email_address,'a@gmail.com')

class RoomTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        RoomType.objects.create(name='faltu',price='1')

    def test_name(self):
        roomtype = RoomType.objects.get(name='faltu')
        self.assertEquals(roomtype.name, 'faltu') 

    def test_price(self):
        roomtype = RoomType.objects.get(price='1')
        self.assertEquals(roomtype.price, 1)  
 

class FacilityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Facility.objects.create(name='Ac',price="100")

    def test_name(self):
        facility = Facility.objects.get(name = 'Ac')
        self.assertEquals(facility.name,'Ac')

    def test_price(self):
        facility = Facility.objects.get(price = '100')
        self.assertEquals(facility.price,100)


       

# class RoomTests(TestCase):
#     def test_home_view_status_code(self):
#         url = reverse('rooms')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 302)

class SignupTests(TestCase):
    def setUp(self):
        Signup.objects.create(user_name='anuj',password='anuj' )

    # def test_signup_view_success_status_code(self):
    #     url = reverse('signup')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_board_topics_view_not_found_status_code(self):
    #     url = reverse('board_topics', kwargs={'pk': 99})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 404)

    # def test_board_topics_url_resolves_board_topics_view(self):
    #     view = resolve('/boards/1/')
    #     self.assertEquals(view.func, board_topics)