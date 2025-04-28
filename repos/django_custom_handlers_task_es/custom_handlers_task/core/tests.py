from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        response = self.client.get('/nonexist-page/')
        # Comprueba que el código de estado sea 404
        # Comprueba que se use la plantilla core/404.html
