import pytest


class TestTemplateView:

    @pytest.mark.django_db(transaction=True)
    def test_about_author_tech(self, client):
        urls = ['/about/author/', '/about/tech/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'''La página `{url}` no se carga adecuadamente. Error: `{e}`'''
            assert response.status_code != 404, f'La página `{url}` no se encuentra, verifica esta ruta en *urls.py*'
            assert response.status_code == 200, (
                f'Error {response.status_code} al abrir `{url}`. Comprueba la función vista correspondiente'
            )
