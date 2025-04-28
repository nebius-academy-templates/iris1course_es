from django.shortcuts import render

ice_cream_catalog = [
    {
        'id': 0,
        'title': 'Helado de vainilla clásico',
        'description': 'Auténtico helado para los verdaderos conocedores del sabor. '
                       'Si el helado aparece en la mesa, no durará mucho.',
    },
    {
        'id': 1,
        'title': 'Helado de saltamontes',
        'description': 'Aderezado con '
                       'saltamontes colombianos caramelizados.',
    },
    {
        'id': 2,
        'title': 'Helado de cheddar',
        'description': 'Con sabor a auténtico queso en un cono de barquillo.',
    },
]


def ice_cream_detail(request, pk):
    template = 'ice_cream/detail.html'
    context = {'ice_cream': ice_cream_catalog[pk]}
    return render(request, template, context)


def ice_cream_list(request):
    template = 'ice_cream/list.html'
    context = {'ice_cream_list': ice_cream_catalog}
    return render(request, template, context)
