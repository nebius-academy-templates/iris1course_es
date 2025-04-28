import re

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.template.loader import select_template

try:
    from posts.models import Post
except ImportError:
    assert False, 'No se ha encontrado el modelo Post'

try:
    from posts.models import Group
except ImportError:
    assert False, 'No se ha encontrado el modelo de Group'


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


class TestPost:

    def test_post_model(self):
        model_fields = Post._meta.fields
        text_field = search_field(model_fields, 'text')
        assert text_field is not None, 'Añade el nombre del evento `text` al modelo `Post`'
        assert type(text_field) == fields.TextField, (
            'El atributo `text` del modelo `Post` debe ser de tipo `TextField`'
        )

        pub_date_field = search_field(model_fields, 'pub_date')
        assert pub_date_field is not None, 'Agrega la fecha y hora del evento: el campo `pub_date` del modelo `Post`'
        assert type(pub_date_field) == fields.DateTimeField, (
            'El atributo `pub_date` del modelo `Post` debe ser del tipo `DateTimeField`'
        )
        assert pub_date_field.auto_now_add, 'El atributo `pub_date` del modelo `Post` debe ser de tipo `auto_now_add`'

        author_field = search_field(model_fields, 'author_id')
        assert author_field is not None, 'Agregar autor: el campo `author` del modelo `Post`'
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
            'El atributo `group` del modelo `Post` debe tener el parámetro `blank=True`'
        )
        assert group_field.null, (
            'El atributo `group` del modelo `Post` debe tener el parámetro `null=True`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user):
        text = 'Publicación de prueba'
        author = user

        assert Post.objects.count() == 0

        post = Post.objects.create(text=text, author=author)
        assert Post.objects.count() == 1
        assert Post.objects.get(text=text, author=author).pk == post.pk

    def test_post_admin(self):
        admin_site = site

        assert Post in admin_site._registry, 'Registra el modelo `Post` en el sitio de administración'

        admin_model = admin_site._registry[Post]

        assert 'text' in admin_model.list_display, (
            'Muestra `text` en la interfaz de administración'
        )
        assert 'pub_date' in admin_model.list_display, (
            'Muestra `pub_date` en la interfaz de administración'
        )
        assert 'author' in admin_model.list_display, (
            'Muestra `author` en la interfaz de administración'
        )

        assert 'text' in admin_model.search_fields, (
            'Agrega una opción para buscar mediante `text` en la interfaz de administración'
        )

        assert 'pub_date' in admin_model.list_filter, (
            'Agrega un filtro por `pub_date` en la interfaz de administración'
        )

        assert hasattr(admin_model, 'empty_value_display'), (
            'Añade un valor por defecto `-empty-` para los campos vacíos'
        )
        assert admin_model.empty_value_display == '-empty-', (
            'Añade un valor por defecto `-empty-` para los campos vacíos'
        )


class TestGroup:

    def test_group_model(self):
        model_fields = Group._meta.fields
        title_field = search_field(model_fields, 'title')
        assert title_field is not None, 'Agrega el nombre del evento `title` al modelo `Group`'
        assert type(title_field) == fields.CharField, (
            'El atributo `title` del modelo `Group` debe ser de tipo `CharField`'
        )
        assert title_field.max_length == 200, 'Establece la longitud máxima del `title` del modelo `Group` en 200'

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, 'Agrega un slug `slug` al modelo `Group`'
        assert type(slug_field) == fields.SlugField, (
            'El atributo `slug` del modelo `Group` debe ser de tipo `SlugField`'
        )
        assert slug_field.unique, 'El atributo `slug` del modelo `Group` debe ser único'

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, 'Agrega una descripción `description` del modelo `Group`'
        assert type(description_field) == fields.TextField, (
            'El atributo `description` del modelo `Group` adebe ser un `TextField`'
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
        try:
            response = client.get(f'/group/{post_with_group.group.slug}')
        except Exception as e:
            assert False, f'''La página `/group/<slug>/` no se carga correctamente. Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/group/{post_with_group.group.slug}/')
        if response.status_code == 404:
            assert False, 'La página `/group/<slug>/` no se encuentra, verifica esta ruta en *urls.py*'

        if response.status_code != 200:
            assert False, 'La página `/group/<slug>/` no se carga correctamente.'
        group = post_with_group.group
        html = response.content.decode()

        templates_list = ['group_list.html', 'posts/group_list.html']
        html_template = select_template(templates_list).template.source

        assert search_refind(r'{%\s*for\s+.+in.*%}', html_template), (
            'Edita la plantilla HTML, utiliza un atributo de bucle'
        )
        assert search_refind(r'{%\s*endfor\s*%}', html_template), (
            'Edita la plantilla HTML, no se ha encontrado el atributo de cierre de bucle'
        )

        assert re.search(
            r'<\s*h1\s*>\s*' + group.title + r'\s*<\s*\/h1\s*>',
            html
        ), (
            'Edita la plantilla HTML, no se ha encontrado el título del grupo '
            '`{% block header %}{{ nombre_grupo }}{% endblock %}`'
        )
        assert re.search(
            r'<\s*p\s*>\s*' + group.description + r'\s*<\s*\/p\s*>',
            html
        ), 'Edita la plantilla HTML, no se ha encontrado la descripción del grupo `<p>{{ group_description }}</p>`'
