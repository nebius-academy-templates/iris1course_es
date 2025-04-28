import pytest
from django.core.cache import cache
from django.core.paginator import Page, Paginator

pytestmark = [pytest.mark.django_db]

class TestGroupPaginatorView:

    def test_group_paginator_view_get(self, client, few_posts_with_group):
        try:
            response = client.get(f'/group/{few_posts_with_group.group.slug}')
        except Exception as e:
            assert False, f'''La página `/group/<slug>/` no se carga correctamente.󠀲󠀡󠀣󠀨󠀦󠀥󠀠󠀦󠀳󠀰 Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/group/{few_posts_with_group.group.slug}/')
        assert response.status_code != 404, 'No se encuentra la página `/group/<slug>/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀥󠀠󠀨󠀳
        assert 'page_obj' in response.context, (
            'Asegúrate de haber añadido la variable `page_obj` al contexto de página de `/group/<slug>/`'
        )
        assert isinstance(response.context['page_obj'], Page), (
            'Asegúrate de que la variable `page_obj` en la página `/group/<slug>/` sea del tipo `Page`'
        )

    def test_group_paginator_not_in_context_view(self, client, post_with_group):
        response = client.get(f'/group/{post_with_group.group.slug}/')
        assert response.status_code != 404, 'No se encuentra la página `/group/<slug>/`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀥󠀠󠀨󠀳
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Asegúrate de que la variable `paginator` en la página `/group/<slug>/` sea del tipo `Paginator`'
        )

    def test_index_paginator_not_in_view_context(self, client, few_posts_with_group):
        response = client.get('/')
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Asegúrate de que la variable `paginator` del objeto `page_obj` en la página `/` sea del tipo `Paginator`'
        )

    def test_index_paginator_view(self, client, post_with_group):
        cache.clear()
        response = client.get('/')
        assert response.status_code != 404, 'No se encuentra la página `/`, verifica esta ruta en *urls.py*'
        assert 'page_obj' in response.context, (
            'Asegúrate de haber agregado la variable `page_obj` al contexto de página de `/`'
        )
        assert isinstance(response.context['page_obj'], Page), (
            'Asegúrate de que la variable `page_obj` en la página `/` sea del tipo `Page`'
        )

    def test_profile_paginator_view(self, client, few_posts_with_group):
        response = client.get(f'/profile/{few_posts_with_group.author.username}/')
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Asegúrate de que la variable `paginator` del objeto `page_obj`'
            ' en la página `/profile/<username>/` sea del tipo `Paginator`'
        )
