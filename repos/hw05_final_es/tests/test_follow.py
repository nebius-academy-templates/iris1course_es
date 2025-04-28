import re
import tempfile

from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.core.paginator import Page

import pytest


try:
    from posts.models import Post
except ImportError:
    assert False, 'No se encontró el modelo Post'

try:
    from posts.models import Follow
except ImportError:
    assert False, 'No se encontró el modelo Follow'


def search_field(model_fields, searching_field_name):
    for field in model_fields:
        if field.name == searching_field_name:
            return field
    return None


def search_refind(execution, user_code):
    """Búsqueda para iniciar"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestFollow:

    @pytest.mark.parametrize('field_name', ['author', 'user'])
    def test_follow(self, field_name):
        model_name = 'Follow'
        related_name = 'follower' if field_name == 'user' else 'following'
        checking_field = search_field(Follow._meta.fields, field_name)
        field_in_model_text = (f'El campo `{field_name}` del modelo `{model_name}`')
        assert checking_field is not None, (
            f'{field_in_model_text} falta o ha sido renombrado. '󠀲󠀡󠀣󠀨󠀦󠀤󠀡󠀢󠀳
        )
        assert isinstance(checking_field, ForeignKey), (
            f'{field_in_model_text} '
            'debe tener una relación muchos a uno '
            'al modelo user. Comprueba la clase field.'
        )
        assert checking_field.related_model == get_user_model(), (
            f'{field_in_model_text} debe tener una relación con el modelo '󠀲󠀡󠀣󠀨󠀦󠀤󠀡󠀦󠀳
            f'`{get_user_model().__name__}`'
        )
        assert checking_field.remote_field.related_name == related_name, (
            f'Al declararse, {field_in_model_text} debe contener '
            f'`related_name=\'{related_name}\'`'
        )
        assert not checking_field.unique, (
            f'{field_in_model_text} '
            'no debe limitarse a valores únicos. '
            'Un autor puede tener muchos '
            'seguidores. Un usuario puede seguir a muchos '
            'autores. '
        )
        assert checking_field.remote_field.on_delete.__name__ == 'CASCADE', (
            f'La {field_in_model_text} deben '
            '`on_delete=models.CASCADE`.'
        )

    def check_url(self, client, url, str_url):
        try:
            response = client.get(f'{url}')
        except Exception as e:
            assert False, f'''La página `{str_url}` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀤󠀢󠀣󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302) and response.url == f'{url}/':
            response = client.get(f'{url}/')
        assert response.status_code != 404, f'No se encuentra la página `{str_url}`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀤󠀢󠀥󠀳
        return response

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, user):
        response = self.check_url(client, '/follow', '/follow/')
        if not(response.status_code in (301, 302) and response.url.startswith('/auth/login')):
            assert False, (
                'Asegúrate de que los usuarios no autorizados sean redirigidos desde `/follow/` hacia la página de inicio de sesión'󠀲󠀡󠀣󠀨󠀦󠀤󠀢󠀦󠀳
            )

        response = self.check_url(client, f'/profile/{user.username}/follow', '/profile/<username>/follow/')
        if not(response.status_code in (301, 302) and response.url.startswith('/auth/login')):
            assert False, (
                'Asegúrate de que los usuarios no autorizados sean redirigidos desde `profile/<username>/follow/` '
                'hacia la página de inicio de sesión'
            )

        response = self.check_url(client, f'/profile/{user.username}/unfollow', '/profile/<username>/unfollow/')
        if not(response.status_code in (301, 302) and response.url.startswith('/auth/login')):
            assert False, (
                'Asegúrate de que los usuarios no autorizados sean redirigidos desde `profile/<username>/unfollow/` '
                'hacia la página de inicio de sesión'
            )

    @pytest.mark.django_db(transaction=True)
    def test_follow_auth(self, user_client, user, post):
        assert hasattr(user, 'follower'), (
            'Al declarar, el campo `user` del modelo `Follow` debe contener '󠀲󠀡󠀣󠀨󠀦󠀤󠀣󠀡󠀳
            '`related_name="follower"'
        )
        assert user.follower.count() == 0, 'Prueba que el número de seguidores se calcule correctamente'
        self.check_url(user_client, f'/profile/{post.author.username}/follow', '/profile/<username>/follow/')
        assert user.follower.count() == 0, 'Prueba que no puedas seguir tu propia cuenta'

        user_1 = get_user_model().objects.create_user(username='TestUser_2344')
        user_2 = get_user_model().objects.create_user(username='TestUser_73485')

        self.check_url(user_client, f'/profile/{user_1.username}/follow', '/profile/<username>/follow/')
        assert user.follower.count() == 1, 'Prueba que puedas seguir a un usuario'
        self.check_url(user_client, f'/profile/{user_1.username}/follow', '/profile/<username>/follow/')
        assert user.follower.count() == 1, 'Prueba que puedes seguir a un usuario sólo una vez'

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        Post.objects.create(text='Publicación de prueba 4564534', author=user_1, image=image)
        Post.objects.create(text='Publicación de prueba 354745', author=user_1, image=image)

        Post.objects.create(text='Publicación de prueba 245456', author=user_2, image=image)
        Post.objects.create(text='Publicación de prueba 9789', author=user_2, image=image)
        Post.objects.create(text='Publicación de prueba 4574', author=user_2, image=image)

        response = self.check_url(user_client, '/follow', '/follow/')
        assert 'page_obj' in response.context, (
            'Asegúrate de haber agregado la variable `page_obj` al contexto de página de `/follow/`'
        )
        assert type(response.context['page_obj']) == Page, (
            'Asegúrate de haber agregado la variable `page_obj` en la página `/follow/` sea del tipo `Page`'
        )
        assert len(response.context['page_obj']) == 2, (
            'Asegúrate de que la página `/follow/` muestre las publicaciones de los autores que sigues'󠀲󠀡󠀣󠀨󠀦󠀤󠀣󠀩󠀳
        )

        self.check_url(user_client, f'/profile/{user_2.username}/follow', '/profile/<username>/follow/')
        assert user.follower.count() == 2, 'Prueba que puedes seguir a un usuario'
        response = self.check_url(user_client, '/follow', '/follow/')
        assert len(response.context['page_obj']) == 5, (
            'Asegúrate de que la página `/follow/` muestre las publicaciones de los autores que sigues'
        )

        self.check_url(user_client, f'/profile/{user_1.username}/unfollow', '/profile/<username>/unfollow/')
        assert user.follower.count() == 1, 'Prueba que puedes dejar de seguir a un usuario'
        response = self.check_url(user_client, '/follow', '/follow/')
        assert len(response.context['page_obj']) == 3, (
            'Asegúrate de que la página `/follow/` muestre las publicaciones de los autores que sigues'󠀲󠀡󠀣󠀨󠀦󠀤󠀣󠀩󠀳
        )

        self.check_url(user_client, f'/profile/{user_2.username}/unfollow', '/profile/<username>/unfollow/')
        assert user.follower.count() == 0, 'Prueba que puedes dejar de seguir a un usuario'
        response = self.check_url(user_client, '/follow', '/follow/')
        assert len(response.context['page_obj']) == 0, (
            'Asegúrate de que la página `/follow/` muestre las publicaciones de los autores que sigues'󠀲󠀡󠀣󠀨󠀦󠀤󠀣󠀩󠀳
        )
