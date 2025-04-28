import pytest
from django import forms
from posts.models import Post


class TestCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client):
        try:
            response = user_client.get('/create')
        except Exception as e:
            assert False, f'''La página `/create` no se descarga adecuadamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get('/create/')
        assert response.status_code != 404, 'No se ha encontrado la página `/create/`, verifica esta ruta en *urls.py*'
        assert 'form' in response.context, 'Asegúrate de haber agregado `form` al contexto de página de `/create/`'
        assert len(response.context['form'].fields) == 2, 'Asegúrate de que el formulario `form` en la página `/create/` tenga 2 campos'
        assert 'group' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `group`'
        )
        assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `group` de tipo `ModelChoiceField`'
        )
        assert not response.context['form'].fields['group'].required, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo opcional `group`'
        )

        assert 'text' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `text`'
        )
        assert type(response.context['form'].fields['text']) == forms.fields.CharField, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `text` de tipo `CharField`'
        )
        assert response.context['form'].fields['text'].required, (
            'Asegúrate de que el formulario `form` en la página `/create/` tiene un campo requerido `text`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, user_client, user, group):
        text = '¡Nueva publicación de prueba!'
        try:
            response = user_client.get('/create')
        except Exception as e:
            assert False, f'''La página `/create` no se descarga adecuadamente. Error: `{e}`'''
        url = '/create/' if response.status_code in (301, 302) else '/create'

        response = user_client.post(url, data={'text': text, 'group': group.id})

        assert response.status_code in (301, 302), (
            'Asegúrate de que después de crear una publicación en la página `/create/`, '
            f'redirijas al usuario a su página de perfil `/profile/{user.username}`'
        )
        post = Post.objects.filter(author=user, text=text, group=group).first()
        assert post is not None, 'Asegúrate de haber guardado la nueva publicación al enviar el formulario en la página `/create/`'
        assert response.url == f'/profile/{user.username}/', (
            f'Asegúrate de redirigir al usuario a la página de perfil del autor `/profile/{user.username}`'
        )

        text = '¡Nueva publicación de prueba 2!'
        response = user_client.post(url, data={'text': text})
        assert response.status_code in (301, 302), (
            'Asegúrate de que después de crear una publicación en la página `/create/`, '
            f'redirijas al usuario a su página de perfil `/profile/{user.username}`'
        )
        post = Post.objects.filter(author=user, text=text, group__isnull=True).first()
        assert post is not None, 'Asegúrate de haber guardado la nueva publicación al enviar el formulario en la página `/create/`'
        assert response.url == f'/profile/{user.username}/', (
            f'Asegúrate de redirigir al usuario a la página de perfil del autor `/profile/{user.username}`'
        )

        response = user_client.post(url)
        assert response.status_code == 200, (
            'Asegúrate de mostrar mensajes de error en caso de que la entrada `form` no sea válida en la página `/create/`'
        )
