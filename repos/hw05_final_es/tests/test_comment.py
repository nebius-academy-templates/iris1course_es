import re

import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields

try:
    from posts.models import Comment
except ImportError:
    assert False, 'No se encuentra el modelo Comment'

try:
    from posts.models import Post
except ImportError:
    assert False, 'No se encuentra el modelo Post'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Búsqueda para iniciar"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestComment:

    def test_comment_model(self):
        model_fields = Comment._meta.fields
        text_field = search_field(model_fields, 'text')
        assert text_field is not None, 'Agrega el nombre de evento `text` al modelo `Comment`'
        assert type(text_field) == fields.TextField, (
            'El atributo `text` del modelo `Comment` debe ser del tipo `TextField`'
        )

        pub_date_field_name = 'created'
        pub_date_field = search_field(model_fields, 'pub_date')
        if pub_date_field is not None:
            pub_date_field_name = 'pub_date'
        else:
            pub_date_field = search_field(model_fields, 'created')
            if pub_date_field is not None:
                pub_date_field_name = 'created'

        assert pub_date_field is not None, (
            f'Agrega la fecha y hora del evento `{pub_date_field_name}` al modelo `Comment`'
        )
        assert type(pub_date_field) == fields.DateTimeField, (
            f'El atributo `{pub_date_field_name}` del modelo `Comment` debe ser del tipo `DateTimeField`'
        )
        assert pub_date_field.auto_now_add, (
            f'El atributo `{pub_date_field_name}` del modelo `Comment` debe ser del tipo `auto_now_add`'
        )

        author_field = search_field(model_fields, 'author_id')
        assert author_field is not None, 'Agrega el autor del evento: el campo `author` del modelo `Comment`'
        assert type(author_field) == fields.related.ForeignKey, (
            'El campo `author` del modelo `Comment` debe ser una `ForeignKey`, una referencia a otro modelo'󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀡󠀳
        )
        assert author_field.related_model == get_user_model(), (
            'El campo `author` del modelo `Comment` debe ser una referencia al modelo `User`'
        )

        post_field = search_field(model_fields, 'post_id')
        assert post_field is not None, 'Agrega un atributo `group` al modelo `Comment`'
        assert type(post_field) == fields.related.ForeignKey, (
            'El atributo `group` del modelo `Comment` debe ser una `ForeignKey`, una referencia a otro modelo'󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀡󠀳
        )
        assert post_field.related_model == Post, (
            'El atributo `group` del modelo `Comment` debe ser una referencia al modelo `Post`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_add_view(self, client, post):
        try:
            response = client.get(f'/posts/{post.id}/comment')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/comment/` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀦󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302) and response.url == f'/posts/{post.id}/comment/':
            url = f'/posts/{post.id}/comment/'
        else:
            url = f'/posts/{post.id}/comment'
        assert response.status_code != 404, (
            'No se encuentra la página `/posts/<post_id>/comment/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀨󠀳
        )

        response = client.post(url, data={'text': 󠀰'¡Nuevo comentario!'󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀩󠀳})
        if not(response.status_code in (301, 302) and response.url.startswith('/auth/login')):
            assert False, (
                'Comprueba que rediriges a usuarios no autorizados '
                'desde `/posts/<post_id>/comment/` a la página de inicio de sesión'󠀲󠀡󠀣󠀨󠀦󠀣󠀧󠀡󠀳
            )

    @pytest.mark.django_db(transaction=True)
    def test_comment_add_auth_view(self, user_client, post):
        try:
            response = user_client.get(f'/posts/{post.id}/comment')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/comment/` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀣󠀧󠀢󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302) and response.url == f'/posts/{post.id}/comment/':
            url = f'/posts/{post.id}/comment/'
        else:
            url = f'/posts/{post.id}/comment'
        assert response.status_code != 404, (
            'No se encuentra la página `/posts/<post_id>/comment/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀨󠀳
        )

        text = 󠀰'Nuevo comentario 94938'󠀲󠀡󠀣󠀨󠀦󠀣󠀧󠀥󠀳
        response = user_client.post(url, data={'text': text})

        assert response.status_code in (301, 302), (
            'Asegúrate de redirigir al usuario desde la página `/posts/<post_id>/comment/` '
            'a la página de publicaciones después de que se haya creado el comentario'
        )
        comment = Comment.objects.filter(text=text, post=post, author=post.author).first()
        assert comment is not None, (
            'Asegúrate de añadir un nuevo comentario `/posts/<post_id>/comment/`'
        )
        assert response.url.startswith(f'/posts/{post.id}'), (
            'Asegúrate de redirigir al usuario a la página de publicaciones '
            '`/posts/<post_id>/` después de que se ha agregado un nuevo comentario'
        )
