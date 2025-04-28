from django.shortcuts import render


def page_not_found(request, exception):
    # La variable exception contiene información de depuración
    # que no se pasará a la plantilla de la página 404
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')
