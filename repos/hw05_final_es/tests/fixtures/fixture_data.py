import tempfile

import pytest
from mixer.backend.django import mixer as _mixer
from posts.models import Post, Group


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def post(user):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(text='Publicación de prueba 1', author=user, image=image)


@pytest.fixture
def group():
    return Group.objects.create(title='Grupo de prueba 1', slug='test-link', description='Test group description')


@pytest.fixture
def post_with_group(user, group):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(text='Publicación de prueba 2', author=user, group=group, image=image)


@pytest.fixture
def few_posts_with_group(mixer, user, group):
    """Devolver un registro con el mismo autor y grupo."""
    posts = mixer.cycle(20).blend(Post, author=user, group=group)
    return posts[0]


@pytest.fixture
def another_few_posts_with_group_with_follower(mixer, user, another_user, group):
    mixer.blend('posts.Follow', user=user, author=another_user)
    mixer.cycle(20).blend(Post, author=another_user, group=group)
