from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from users_and_roles.models import Role, Editor, Client, User, Organization
from ..models import Strategy


LOGIN_URL = 'http://host:port/rest-auth/login/'
STRATEGY_URL = 'http://host:port/strategy/display/'


class SetUpClass(APITestCase):
    fixtures = ['strategy/tests/fixtures/test_data.json']

    @classmethod
    def setUpClass(cls):
        super(SetUpClass, cls).setUpClass()
        cls.password = 'botree123'
        cls.client = APIClient()
        client_response = cls.client.post(LOGIN_URL, data={
            'email': 'botree-client@gmail.com', 'password': cls.password})
        editor_response = cls.client.post(LOGIN_URL, data={
            'email': 'botree-editor@gmail.com', 'password': cls.password})
        cls.client_profile = Client.get(id=25)
        cls.strategy = Strategy.get(1)
        cls.editor_token = editor_response.data['token']
        cls.client_token = client_response.data['token']
        print(cls.editor_token)
        print(cls.client_token)
        return


class StrategyViewTests(SetUpClass):

    def test_create_strategy_by_editor(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.editor_token)
        response = self.client.post(STRATEGY_URL, data={
            "description": "description 1", "target_market": "market 1",
            "target_persona": "persona 1", "content_pillars": "pillers 1",
            "aims": "aims 1", "client": self.client_profile.id})
        print(response.content)
        self.assertEqual(response.data['client'], self.client_profile.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_strategy_with_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.client_token)
        response = self.client.post(STRATEGY_URL, data={
            "description": "description 1", "target_market": "market 1",
            "target_persona": "persona 1", "content_pillars": "pillers 1",
            "aims": "aims 1", "client": self.client_profile.id})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_strategy_without_client_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.editor_token)
        response = self.client.post(STRATEGY_URL, data={
            "description": "description 1", "target_market": "market 1",
            "target_persona": "persona 1", "content_pillars": "pillers 1",
            "aims": "aims 1"})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_strategy_without_proper_details(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.editor_token)
        response = self.client.post(STRATEGY_URL, data={
            "description": "description 1", "target_persona": "persona 1",
            "aims": "aims 1", "client": self.client_profile.id})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_strategy_by_editor(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.editor_token)
        response = self.client.patch(STRATEGY_URL, data={
            "id": self.strategy.id, "description": "description 1",
            "target_persona": "persona 1", "content_pillars": "pillers 1"})
        print(response.content)
        self.assertEqual(response.data['description'], "description 1")
        self.assertEqual(response.data['target_persona'], "persona 1")
        self.assertEqual(response.data['content_pillars'], "pillers 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_strategy_with_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.client_token)
        response = self.client.patch(STRATEGY_URL, data={
            "id": self.strategy.id, "description": "description 1",
            "target_persona": "persona 1", "content_pillars": "pillers 1"})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_strategy(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.client_token)
        response = self.client.get(STRATEGY_URL, data={"id": self.strategy.id})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_strategy_without_strategy_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.client_token)
        response = self.client.get(STRATEGY_URL, data={})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


