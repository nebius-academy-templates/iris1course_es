import pytest


class TestAuthUrls:

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = ['/auth/login/', '/auth/logout/', '/auth/signup/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'''La página `{url}` no se carga adecuadamente. Error: `{e}`'''
            assert response.status_code != 404, f'No se encuentra la página `{url}`, verifica esta ruta en *urls.py*'
            assert response.status_code == 200, (
                f'Error {response.status_code} al abrir `{url}`. Revisa la función de vista correspondiente'
            )
