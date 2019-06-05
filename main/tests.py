from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm
from django.test import TestCase,Client, LiveServerTestCase
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
            'first_name': 'Anuj',
            'middle_name': 'Sharma',
            'last_name':'Bhardwaj', 
            'address':'faltu',
            'email_address': 'sharmanuj003@gmail.com',
            'contact_no':'1234567890',
            'username': 'anuj',
            'password1': 'anuj',
            'password2': 'anuj'
        }
        self.response = self.client.post(url, data)
        self.signup_url = reverse('signup')

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
    #     response = self.client.get(self.signup_url)
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

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='anuj', email='sharmanuj003@gmail.com', password='anuj')
        self.response = self.client.post(reverse('password_reset'), { 'email': 'sharmanuj003@gmail.com' })
        self.email = mail.outbox[0]

    # def test_email_subject(self):
    #     self.assertEqual('[Django Boards] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('anuj', self.email.body)
        self.assertIn('sharmanuj003@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['sharmanuj003@gmail.com',], self.email.to)

class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'anuj', email = 'sharmanuj003@gmail.com',password = 'anuj')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm',kwargs = {'uidb64':self.uid,'token': self.token})
        self.response = self.client.get(url,follow = True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_view_function(self):
        view = resolve('/accounts/reset/{uidb64}/{token}/'.format(uidb64 = self.uid, token = self.token))
        self.assertEquals(view.func.view_class,auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input')
        self.assertContains(self.response, 'type="password"')


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='anuj',email='sharmanuj003@gmail.com',password='anuj')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        user.set_password('anuj')
        user.save()

        url = reverse('password_reset_confirm',kwargs={'uidb64':uid, 'token':token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    # def test_html(self):
    #     password_reset_url = reverse('login')
    #     self.assertContains(self.response,'invalid password reset link')
    #     self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='anuj', email='sharmanuj003@gmail.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='anuj', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        '''
        refresh the user instance from database to get the new password
        hash updated by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        '''
        response = self.client.get(reverse('index'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        '''
        refresh the user instance from the database to make
        sure we have the latest data.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))


class LoginRequiredSignupTests(TestCase):
    def setUp(self):
        User.objects.create(username='anuj')
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    # def test_redirection(self):
    #     login_url = reverse('login')
    #     self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


# class StaffTests(TestCase):
#     def setUp(self):
#         guests = Guests.objects.create(first_name='Anuj', middle_name='Sharma', last_name='Bhardwaj', address='faltu',email_address = 'sharmanuj003@gmail.com',contact_no = '1234567890')
#         # user = User.objects.create_user(username='anuj', email='sharmanuj003@gmail.com', password='anuj')
#         # topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
#         # Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
#         url = reverse('topic_posts')
#         self.response = self.client.get(url)

#     def test_status_code(self):
#         self.assertEquals(self.response.status_code, 200)

#     def test_view_function(self):
#         view = resolve('/boards/1/topics/1/')
#         self.assertEquals(view.func, topic_posts)


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'])

