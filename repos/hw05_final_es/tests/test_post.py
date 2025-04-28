from io import BytesIO

import pytest
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db.models.query import QuerySet
from PIL import Image
from django.core.cache import cache

from posts.models import Post
from posts.forms import PostForm
from django.core.paginator import Page

from tests.utils import get_field_from_context


class TestPostView:

    @pytest.mark.django_db(transaction=True)
    def test_index_post_with_image(self, client, post):
        url_index = '/'
        cache.clear()
        response = client.get(url_index)

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            'Asegúrate de haber agregado el autor al contexto de página de la página `/` del tipo `Page`'
        )
        assert len(page_context.object_list) == 1, (
            'Asegúrate de haber pasado las publicaciones del autor correcto al contexto de página'
        )
        posts_list = page_context.object_list
        for post in posts_list:
            assert hasattr(post, 'image'), (
                'Asegúrate de que la publicación pasada al contexto de página de `/` tenga un campo `image`'
            )
            assert getattr(post, 'image') is not None, (
                'Asegúrate de que la publicación pasada al contexto de página de `/` tenga un campo `image` '
                'y que reciba una imagen'
            )

    @pytest.mark.django_db(transaction=True)
    def test_index_post_caching(self, client, post, post_with_group):
        url_index = '/'
        cache.clear()
        response = client.get(url_index)

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            'Asegúrate de haber añadido el autor al contexto de página de la página `/` del tipo `Page`'
        )
        posts_cnt = Post.objects.count()
        post.delete()
        assert len(page_context.object_list) == posts_cnt is not None, (
            'Asegúrate de haber configurado el almacenamiento en caché para la página principal `/` '
            'y que las publicaciones se almacenen en caché cuando se eliminen de la base de datos, hasta que se borre el almacenamiento en caché'
        )
        cache.clear()
        posts_cnt = Post.objects.count()
        response = client.get(url_index)
        page_context = get_field_from_context(response.context, Page)
        assert len(page_context.object_list) == posts_cnt is not None, (
            'Asegúrate de haber configurado el almacenamiento en caché para la página principal `/` '
            'y cuando se borre el almacenamiento en caché, las publicaciones se borren de la base de datos '
            'y también se borren del almacenamiento en caché'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀥󠀣󠀡󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/posts/{post_with_group.id}/')
        assert response.status_code != 404, (
            'No se encuentra la página `/posts/<post_id>/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀥󠀣󠀣󠀳
        )

        post_context = get_field_from_context(response.context, Post)
        assert post_context is not None, (
            'Asegúrate de haber pasado la publicación al contexto de página de `/posts/<post_id>/` del tipo `Post`'
        )

        try:
            from posts.forms import CommentForm
        except ImportError:
            assert False, 'El formulario CommentForm no se encuentra en posts.form'

        comment_form_context = get_field_from_context(response.context, CommentForm)
        assert comment_form_context is not None, (
            'Asegúrate de haber pasado el formulario de comentarios al contexto de página de `/posts/<post_id>/` del tipo `CommentForm`'
        )
        assert len(comment_form_context.fields) == 1, (
            'Asegúrate de que el formulario de comentarios en el contexto de página de `/posts/<post_id>/` tenga un campo'󠀲󠀡󠀣󠀨󠀦󠀥󠀣󠀧󠀳
        )
        assert 'text' in comment_form_context.fields, (
            󠀰'Asegúrate de que el formulario de comentarios en el contexto de página de `/posts/<post_id>/` contenga un campo `text`'
        )
        assert type(comment_form_context.fields['text']) == forms.fields.CharField, (
            'Asegúrate de que el formulario de comentarios en el contexto de página de `/posts/<post_id>/` '
            'contenga un campo `text` del tipo `CharField`'
        )
        assert hasattr(post_context, 'image'), (
            'Asegúrate de que la publicación pasada al contexto de página de `/posts/<post_id>/` tenga un campo `image`'
        )
        assert getattr(post_context, 'image') is not None, (
            'Asegúrate de que la publicación pasada al contexto de página de `/posts/<post_id>/` tenga un campo `image` '
            'y que reciba una imagen'
        )


class TestPostEditView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀥󠀤󠀤󠀳󠀰 Error: `{e}`'''
        if (
                response.status_code in (301, 302)
                and not response.url.startswith(f'/posts/{post_with_group.id}')
        ):
            response = client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            󠀰'No se encuentra la página `/posts/<post_id>/edit/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀥󠀤󠀦󠀳
        )

        assert response.status_code in (301, 302), (
            'Asegúrate de redirigir al usuario desde la página '
            '`/posts/<post_id>/edit/` a la página de publicaciones si no es el autor'󠀲󠀡󠀣󠀨󠀦󠀥
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_with_group):
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se carga correctamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            'No se encuentra la página `/posts/<post_id>/edit/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀥󠀥󠀡󠀳
        )

        post_context = get_field_from_context(response.context, Post)
        postform_context = get_field_from_context(response.context, PostForm)
        assert any([post_context, postform_context]) is not None, (
            'Asegúrate de haber pasado la publicación al contexto de página de `/posts/<post_id>/edit/` del tipo `Post` o `PostForm`'
        )

        assert 'form' in response.context, (
            'Asegúrate de haber agregado el formulario `form` al contexto de página de `/posts/<post_id>/edit/`'
        )
        fields_cnt = 3
        assert len(response.context['form'].fields) == fields_cnt, (
            f'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga campos {fields_cnt}'󠀲󠀡󠀣󠀨󠀦󠀥󠀥󠀤󠀳
        )
        assert 'group' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `group`'
        )
        assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `group` del tipo `ModelChoiceField`'
        )
        assert not response.context['form'].fields['group'].required, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo opcional `group`'
        )

        assert 'text' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `text`'
        )
        assert type(response.context['form'].fields['text']) == forms.fields.CharField, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `text` del tipo `CharField`'
        )
        assert response.context['form'].fields['text'].required, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo obligatorio `group`'
        )

        assert 'image' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `image`'
        )
        assert type(response.context['form'].fields['image']) == forms.fields.ImageField, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo `image` del tipo `ImageField`'
        )

    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, mock_media, user_client, post_with_group):
        text = '¡Comprobación de la edición de la publicación!'
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se cargó correctamente. Error: `{e}`'''
        url = (
            f'/posts/{post_with_group.id}/edit/'
            if response.status_code in (301, 302)
            else f'/posts/{post_with_group.id}/edit'
        )

        image = self.get_image_file('image2.png')
        response = user_client.post(url, data={'text': text, 'group': post_with_group.group_id, 'image': image})

        assert response.status_code in (301, 302), (
            󠀰'Asegúrate de redirigir al usuario desde la página `/posts/<post_id>/edit/` '
            'a la página de publicaciones después de crear la publicación'
        )
        post = Post.objects.filter(author=post_with_group.author, text=text, group=post_with_group.group).first()
        assert post is not None, (
            'Asegúrate de editar la publicación cuando el formulario correspondiente se envíe en la página `/posts/<post_id>/edit/`'
        )
        assert response.url.startswith(f'/posts/{post_with_group.id}'), (
            'Asegúrate de redirigir al usuario a la página de publicaciones `/posts/<post_id>/`'
        )
