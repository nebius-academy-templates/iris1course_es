import re
import tempfile

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.template.loader import select_template
from django.core.paginator import Page

from tests.utils import get_field_from_context

try:
    from posts.models import Post
except ImportError:
    assert False, 'No se encuentra el modelo Post'

try:
    from posts.models import Group
except ImportError:
    assert False, 'No se encuentra el modelo Group'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Buscando el lanzamiento"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestPost:

    def test_post_model(self):
        model_fields = Post._meta.fields
        text_field = search_field(model_fields, 'text')
        assert text_field is not None, 'Agrega el nombre del evento `text` al modelo `Post`'
        assert type(text_field) == fields.TextField, (
            'El atributo `text` del modelo `Post` debe ser del tipo `TextField`'
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
            f'Agrega la fecha y hora del evento `{pub_date_field_name}` al modelo `Post`'
        )
        assert type(pub_date_field) == fields.DateTimeField, (
            f'El atributo `{pub_date_field_name}` del modelo `Post` debe ser del tipo `DateTimeField`'
        )
        assert pub_date_field.auto_now_add, (
            f'Los atributos `pub_date` o `created` del modelo `Post` deben ser del tipo `auto_now_add`'
        )

        author_field = search_field(model_fields, 'author_id')
        assert author_field is not None, 'Agrega el autor del evento: el campo `author` del modelo `Post`'
        assert type(author_field) == fields.related.ForeignKey, (
            'El campo `author` del modelo `Post` debe ser una `ForeignKey`, una referencia a otro modelo'
        )
        assert author_field.related_model == get_user_model(), (
            'El campo `author` del modelo `Post` debe ser una referencia al modelo `User`'
        )

        group_field = search_field(model_fields, 'group_id')
        assert group_field is not None, 'Agrega un atributo `group` al modelo `Post`'
        assert type(group_field) == fields.related.ForeignKey, (
            'El campo `group` del modelo `Post` debe ser una `ForeignKey`, una referencia a otro modelo'
        )
        assert group_field.related_model == Group, (
            'El campo `group` del modelo `Post` debe ser una referencia al modelo `Group`'
        )
        assert group_field.blank, (
            'El atributo `group` del modelo `Post` debe tener un parámetro `blank=True`'
        )
        assert group_field.null, (
            'ThEl atributoe `group` del modelo `Post` debe tener un parámetro `null=True`'
        )

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, 'Agrega un atributo `image` al modelo `Post`'
        assert type(image_field) == fields.files.ImageField, (
            'El atributo `image` del modelo `Post` debe ser del tipo `ImageField`'
        )
        assert image_field.upload_to == 'posts/', (
            "El atributo `image` del modelo `Post` debe tener el parámetro `upload_to='posts/'`"
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user):
        text = 'Publicación de prueba'
        author = user

        assert Post.objects.count() == 0

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        post = Post.objects.create(text=text, author=author, image=image)
        assert Post.objects.count() == 1
        assert Post.objects.get(text=text, author=author).pk == post.pk

    def test_post_admin(self):
        admin_site = site

        assert Post in admin_site._registry, 'Registra el modelo `Post` en el sitio de administración'

        admin_model = admin_site._registry[Post]

        assert 'text' in admin_model.list_display, (
            'Muestra `text` en la interfaz de administración'
        )

        assert 'pub_date' in admin_model.list_display or 'created' in admin_model.list_display, (
            f'Muestra `pub_date` o `created` en la interfaz de administración'
        )
        assert 'author' in admin_model.list_display, (
            'Muestra `author` en la interfaz de administración'
        )

        assert 'text' in admin_model.search_fields, (
            'Agrega una opción para buscar por `text` en la interfaz de administración'
        )

        assert 'pub_date' in admin_model.list_filter or 'created' in admin_model.list_filter, (
            f'Agrega un filtro por `pub_date` o `created` en la interfaz de administración'
        )

        assert hasattr(admin_model, 'empty_value_display'), (
            'Agrega un valor predeterminado `-empty-` para campos vacíos'󠀲󠀡󠀣󠀨󠀦󠀤󠀧󠀣󠀳
        )
        assert admin_model.empty_value_display == '-empty-', (
            'Agrega un valor predeterminado `-empty-` para campos vacíos'󠀲󠀡󠀣󠀨󠀦󠀤󠀧󠀣󠀳
        )


class TestGroup:

    def test_group_model(self):
        model_fields = Group._meta.fields
        title_field = search_field(model_fields, 'title')
        assert title_field is not None, 'Agrega el nombre del evento `title` al modelo `Group`'
        assert type(title_field) == fields.CharField, (
            'El atributo `title` del modelo `Group` debe ser del tipo `CharField`'
        )
        assert title_field.max_length == 200, 'Establece la longitud máxima de `title` del modelo `Group` en 200'

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, 'Agrega un slug `slug` al modelo `Group`'
        assert type(slug_field) == fields.SlugField, (
            'El atributo `slug` del modelo `Group` debe ser del tipo `SlugField`'
        )
        assert slug_field.unique, 'El atributo `slug` del modelo `Group` debe ser único'󠀲󠀡󠀣󠀨󠀦󠀤󠀨󠀠󠀳

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, 'Agrega una descripcion `description` del modelo `Group`'
        assert type(description_field) == fields.TextField, (
            'El atributo `description` del modelo `Group` debe ser un `TextField`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_create(self, user):
        text = 'Publicación de prueba'
        author = user

        assert Post.objects.count() == 0

        post = Post.objects.create(text=text, author=author)
        assert Post.objects.count() == 1
        assert Post.objects.get(text=text, author=author).pk == post.pk

        title = 'Grupo de prueba'
        slug = 'test-link'
        description = 'Descripción del grupo de prueba'

        assert Group.objects.count() == 0
        group = Group.objects.create(title=title, slug=slug, description=description)
        assert Group.objects.count() == 1
        assert Group.objects.get(slug=slug).pk == group.pk

        post.group = group
        post.save()
        assert Post.objects.get(text=text, author=author).group == group


class TestGroupView:

    @pytest.mark.django_db(transaction=True)
    def test_group_view(self, client, post_with_group):
        url = f'/group/{post_with_group.group.slug}'
        url_templ = '/group/<slug>/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''La página `{url_templ}` no se carga correctamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'{url}/')
        if response.status_code == 404:
            assert False, f'No se encuentra la página `{url_templ}`, verifica esta ruta en *urls.py*'󠀲󠀡󠀣󠀨󠀦󠀤󠀨󠀨󠀳

        if response.status_code != 200:
            assert False, f'La página `{url_templ}` no se carga correctamente.'󠀲󠀡󠀣󠀨󠀦󠀤󠀨󠀩󠀳

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            f'Asegúrate de haber añadido el autor al contexto de página de `{url_templ}` del tipo `Page`'
        )
        assert len(page_context.object_list) == 1, (
            f'Asegúrate de haber pasado las publicaciones del autor correcto al contexto de página `{url_templ}`'
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

        group = post_with_group.group
        html = response.content.decode()

        templates_list = ['group_list.html', 'posts/group_list.html']
        html_template = select_template(templates_list).template.source

        assert search_refind(r'{%\s*for\s+.+in.*%}', html_template), (
            'Edita la plantilla HTML, utiliza un atributo loop'
        )
        assert search_refind(r'{%\s*endfor\s*%}', html_template), (
            'Edita la plantilla HTML, no se encuentra el atributo loop de cierre'
        )

        assert re.search(
            group.title,
            html
        ), (
            'Edita la plantilla HTML, no se encuentra el título del grupo '
            '`{% block header %}{{ group_name }}{% endblock %}`'
        )
        assert re.search(
            r'<\s*p\s*>\s*' + group.description + r'\s*<\s*\/p\s*>',
            html
        ), 'Edita la plantilla HTML, no se encuentra la descripción del grupo `<p>{{ group_description }}</p>`'


class TestCustomErrorPages:

    @pytest.mark.django_db(transaction=True)
    def test_custom_404(self, client):
        url_invalid = '/some_invalid_url_404/'
        code = 404
        response = client.get(url_invalid)

        assert response.status_code == code, (
            f'Asegúrate de que las URLs que no existen devuelvan el código de respuesta {code}'
        )

        try:
            from wordicum.urls import handler404 as handler404_student
        except ImportError:
            assert False, (
                f'Asegúrate de que esté establecida una plantilla personalizada para las páginas '
                'devuelve el código de respuesta {code}'
            )

    @pytest.mark.django_db(transaction=True)
    def test_custom_403(self):
        code = 403

        try:
            from wordicum.urls import handler403
        except ImportError:
            assert False, (
                f'Asegúrate de que esté establecida una plantilla personalizada para las páginas '
                'devuelve el código de respuesta {code}'
            )
