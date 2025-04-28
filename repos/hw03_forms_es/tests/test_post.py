import pytest
from django import forms
from posts.forms import PostForm
from posts.models import Post

from tests.utils import get_field_from_context


class TestPostView:

    @pytest.mark.django_db(transaction=True)
    def test_post_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/` no se descarga adecuadamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/posts/{post_with_group.id}/')
        assert response.status_code != 404, (
            'La página `/posts/<post_id>/`  no se ha encontrado, verifica esta ruta en *urls.py*'
        )

        post_context = get_field_from_context(response.context, Post)
        assert post_context is not None, (
            'Asegúrate de haber pasado un artículo al contexto de página de `/posts/<post_id>/` de tipo `Post`'
        )


class TestPostEditView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se descarga adecuadamente. Error: `{e}`'''
        if (
                response.status_code in (301, 302)
                and not response.url.startswith(f'/posts/{post_with_group.id}')
        ):
            response = client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            'La página `/posts/<post_id>/edit/` no se ha encontrado, verifica esta ruta en *urls.py*'
        )

        assert response.status_code in (301, 302), (
            'Asegúrate de redirigir al usuario desde la página '
            '`/<username>/<post_id>/edit/` a la página de la publicación si no son el autor'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_with_group):
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se descarga adecuadamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            'La página `/posts/<post_id>/edit/` no se ha encontrado, verifica esta ruta en *urls.py*'
        )

        post_context = get_field_from_context(response.context, Post)
        postform_context = get_field_from_context(response.context, PostForm)
        assert any([post_context, postform_context]) is not None, (
            'Asegúrate de haber pasado el artículo al contexto de página de `/posts/<post_id>/edit/` de tipo `Post` o `PostForm`'
        )

        assert 'form' in response.context, (
            'Asegúrate de haber agregado `form` al contexto de página `/posts/<post_id>/edit/`'
        )
        assert len(response.context['form'].fields) == 2, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene 2 campos'
        )
        assert 'group' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene un campo `group`'
        )
        assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene un campo `group` de tipo `ModelChoiceField`'
        )
        assert not response.context['form'].fields['group'].required, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene un campo opcional `group` field'
        )

        assert 'text' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene un campo `text`'
        )
        assert type(response.context['form'].fields['text']) == forms.fields.CharField, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tiene un campo `text` de tipo `CharField`'
        )
        assert response.context['form'].fields['text'].required, (
            'Asegúrate de que el formulario `form` en la página `/posts/<post_id>/edit/` tenga un campo requerido `group` field'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, user_client, post_with_group):
        text = '¡Comprobación de la edición de la publicación!'
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''La página `/posts/<post_id>/edit/` no se descarga adecuadamente. Error: `{e}`'''
        url = (
            f'/posts/{post_with_group.id}/edit/'
            if response.status_code in (301, 302)
            else f'/posts/{post_with_group.id}/edit'
        )

        response = user_client.post(url, data={'text': text, 'group': post_with_group.group_id})

        assert response.status_code in (301, 302), (
            'Asegúrate de redirigir al usuario desde la página `/posts/<post_id>/edit/` '
            'a la página de la publicación tras la creación de la misma'
        )
        post = Post.objects.filter(author=post_with_group.author, text=text, group=post_with_group.group).first()
        assert post is not None, (
            'Asegúrate de editar la publicación al enviar el formulario en la página `/posts/<post_id>/edit/`'
        )
        assert response.url.startswith(f'/posts/{post_with_group.id}'), (
            'Asegúrate de redirigir al usuario a la página de la publicación `/posts/<post_id>/`'
        )
