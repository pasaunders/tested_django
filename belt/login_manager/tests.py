from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
import factory

class UserFactory(factory.django.DjangoModelFactory):
    """Makes users for testing."""

    class Meta:
        """Metadata for the user factory."""

        model = User
    
    username = factory.Sequence(lambda n: "User number {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class FrontendTestCases(TestCase):
    """Test that html files display properly and that routes work."""

    def setUp(self):
        """Set up client and request factories."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_route_status(self):
        """Test that the home route returns ok."""
        response = self.client.get('/')
        self.assertTrue(response.status_code == 200)

    def test_signin_route_status(self):
        """Test that the sign in route returns ok."""
        response = self.client.get(reverse_lazy('login:signin_page'))
        self.assertTrue(response.status_code == 200)

    def test_register_route_status(self):
        """Test that the register route returns ok."""
        response = self.client.get(reverse_lazy('login:register_page'))
        self.assertTrue(response.status_code == 200)

    def test_home_route_template(self):
        """Test that the home template is used for rendering."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'login_manager/index.html')

    def test_signin_route_template(self):
        """Test that the sign in template is used for rendering."""
        response = self.client.get(reverse_lazy('login:signin_page'))
        self.assertTemplateUsed(response, 'login_manager/signin.html')

    def test_register_route_template(self):
        """Test that the register template is used for rendering."""
        response = self.client.get(reverse_lazy('login:register_page'))
        self.assertTemplateUsed(response, 'login_manager/register.html')

    def test_signin_form(self):
        """Test that the html for the signin form appears on the signin page."""
        response = self.client.get(reverse_lazy('login:signin_page'))
        self.assertTrue('<form' in str(response.content))
        self.assertTrue('password' in str(response.content))
        self.assertFalse('confirm_password' in str(response.content))

    def test_signin_context(self):
        """Test that the signin route produces the expected context."""
        response = self.client.get(reverse_lazy('login:signin_page'))
        try:
            self.assertTrue('signin_form' in response.context)
        except KeyError:
            self.assertTrue(False)
