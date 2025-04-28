import pytest
from django.contrib.auth import get_user_model
from django.core.paginator import Page

from tests.utils import get_field_from_context


class TestProfileView:

    @pytest.mark.django_db(transaction=True)
    def test_profile_view_get(self, client, post_with_group):
        url = f'/profile/{post_with_group.author.username}'
        url_templ = '/profile/<username>/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''La página `{url_templ}` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀣󠀦󠀦󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'{url}/')
        assert response.status_code != 404, (
            f'No se encuentra la página `{url_templ}`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀤󠀨󠀨󠀳
        )

        profile_context = get_field_from_context(response.context, get_user_model())
        assert profile_context is not None, f'Asegúrate de haber añadido el autor al contexto de página de `{url_templ}`'

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            f'Asegúrate de haber añadido el autor al contexto de página de `{url_templ}` del tipo `Page`'
        )
        assert len(page_context.object_list) == 1, (
            f'Make sure you passed the correct author\'s posts to the page context of `{url_templ}`'
        )
        posts_list = page_context.object_list
        for post in posts_list:
            assert hasattr(post, 'image'), (
                f'Asegúrate de que la publicación que se pasó al contexto de página de `{url_templ}` tenga un campo `image`'
            )
            assert getattr(post, 'image') is not None, (
                f'Asegúrate de que la publicación que se pasó al contexto de página de `{url_templ}` tenga un campo `image` '
                'y que reciba una imagen'
            )

        new_user = get_user_model()(username='new_user_87123478')
        new_user.save()
        url = f'/profile/{new_user.username}'
        try:
            new_response = client.get(url)
        except Exception as e:
            assert False, f'''La página `{url_templ}` no se carga correctamente. Error: `{e}`'''
        if new_response.status_code in (301, 302):
            new_response = client.get(f'{url}/')

        page_context = get_field_from_context(new_response.context, Page)
        assert page_context is not None, (
            f'Asegúrate de haber añadido el autor al contexto de página de `{url_templ}` del tipo `Page`'
        )
        assert len(page_context.object_list) == 0, (
            f'Asegúrate de haber pasado las publicaciones del autor correctas de `{url_templ}`'
        )
