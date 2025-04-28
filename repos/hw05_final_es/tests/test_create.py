from io import BytesIO

import pytest
from django import forms
from django.core.files.base import File
from PIL import Image

from posts.models import Post


class TestCreateView:

    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client):
        try:
            response = user_client.get('/create/')
        except Exception as e:
            assert False, f'''La página `/create/` no se carga adecuadamente. 󠀲󠀡󠀣󠀨󠀦󠀣󠀨󠀢󠀳󠀰Error: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get('/create/')
        assert response.status_code != 404, 'No se encuentra la página `/create/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀣󠀨󠀤󠀳
        assert 'form' in response.context, 'Asegúrate de haber agregado `form` al contexto de página de `/create/`'
        fields_cnt = 3
        assert len(response.context['form'].fields) == fields_cnt, (
            f'Asegúrate de que el formulario `form` en la página `/create/` tenga campos {fields_cnt}'
        )
        assert 'group' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `group`'
        )
        assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `group` del tipo `ModelChoiceField`'
        )
        assert not response.context['form'].fields['group'].required, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo opcional `group`'
        )

        assert 'text' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `text`'
        )
        assert type(response.context['form'].fields['text']) == forms.fields.CharField, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `text` del tipo `CharField`'
        )
        assert response.context['form'].fields['text'].required, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `text` obligatorio'
        )

        assert 'image' in response.context['form'].fields, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `image`'
        )
        assert type(response.context['form'].fields['image']) == forms.fields.ImageField, (
            'Asegúrate de que el formulario `form` en la página `/create/` tenga un campo `image` del tipo `ImageField`'
        )

    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, mock_media, user_client, user, group):
        text = '¡Nueva publicación de prueba!'
        try:
            response = user_client.get('/create')
        except Exception as e:
            assert False, f'''La página `/create` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀣󠀩󠀦󠀳󠀰 Error: `{e}`'''
        url = '/create/' if response.status_code in (301, 302) else '/create'

        image = self.get_image_file('image.png')
        response = user_client.post(url, data={'text': text, 'group': group.id, 'image': image})

        assert response.status_code in (301, 302), (
            'Asegúrate de que después de crear una publicación en la página `/create/`, '
            f'rediriges al usuario a su página de perfil `/profile/{user.username}`'
        )
        post = Post.objects.filter(author=user, text=text, group=group).first()
        assert post is not None, 'Asegúrate de guardar la nueva publicación cuando se envíe el formulario correspondiente en la página `/create/`'
        assert response.url == f'/profile/{user.username}/', (
            f'Asegúrate de redirigir al usuario a la página de perfil del autor `/profile/{user.username}`'
        )

        text = '¡Nueva publicación de prueba 2!'
        image = self.get_image_file('image2.png')
        response = user_client.post(url, data={'text': text, 'image': image})
        assert response.status_code in (301, 302), (
            'Asegúrate de que después de crear una publicación en la página `/create/`, '
            f'rediriges al usuario a su página de perfil `/profile/{user.username}`'
        )
        post = Post.objects.filter(author=user, text=text, group__isnull=True).first()
        assert post is not None, 'Asegúrate de guardar la nueva publicación cuando se envíe el formulario correspondiente en la página `/create/`'
        assert response.url == f'/profile/{user.username}/', (
            f'Asegúrate de redirigir al usuario a su página de perfil `/profile/{user.username}`'
        )

        response = user_client.post(url)
        assert response.status_code == 200, (
            'Asegúrate de mostrar mensajes de error en caso de una entrada `form` no válida en la página `/create/`'
        )
