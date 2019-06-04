from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from .forms import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
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
        facility = Facility.objects.get(price = 100)
        self.assertEquals(facility.price,  100)


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, Signup)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'anuj',
            'password1': 'anuj',
            'password2': 'anuj'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    # def test_redirection(self):
    #     '''
    #     A valid form submission should redirect the user to the home page
    #     '''
    #     self.assertRedirects(self.response, self.signup_url)

    # def test_user_creation(self):
    #     self.assertTrue(User.objects.exists())

    # def test_user_authentication(self):
    #     '''
    #     Create a new request to an arbitrary page.
    #     The resulting response should now have a `user` to its context,
    #     after a successful sign up.
    #     '''
    #     response = self.client.get(self.home_url)
    #     user = response.context.get('user')
    #     self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())



    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', )
        # self.assertContains(self.response, 'type="text"', 1)
        # self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', )

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = Signup()
        expected = ['staff_id','first_name','middle_name','last_name','contact_no','email','username','password1','password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', )
        self.assertContains(self.response, 'type="email"', )


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'sharmanuj003@gmail.com'
        User.objects.create_user(username='anuj', email=email, password='anuj')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to `password_reset_done` view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'sharmanuj003@email.com'})

    def test_redirection(self):
        '''
        Even invalid emails in the database should
        redirect the user to `password_reset_done` view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))