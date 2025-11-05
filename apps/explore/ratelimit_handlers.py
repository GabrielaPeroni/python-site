from django.contrib import messages
from django.shortcuts import redirect


def ratelimited_error(request, exception):
    """
    Mostra uma mensagem user-friendly ao invez de um erro generico
    """
    messages.error(
        request,
        "Você excedeu o limite de pedidos. Por favor, aguarde alguns minutos antes de tentar novamente.",
    )

    # Redirect to the explore page
    return redirect("explore:explore")
