import pytest
from posts.models import Group, Post


@pytest.fixture
def post(user):
    return Post.objects.create(text='Publicación de prueba 1', author=user)


@pytest.fixture
def group():
    return Group.objects.create(title='Grupo de prueba 1', slug='test-link', description='Descripción de grupo de prueba')


@pytest.fixture
def post_with_group(user, group):
    return Post.objects.create(text='Publicación de prueba 2', author=user, group=group)
