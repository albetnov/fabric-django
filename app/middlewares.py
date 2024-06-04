from collections.abc import Callable
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


class AuthMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if not request.user.is_authenticated and request.path not in ["/login", "/health"] and "static" not in request.path:
            messages.add_message(request, messages.ERROR,
                                 "You must be logged in")

            if "assets" not in request.path:
                request.session["next"] = request.path

            return redirect("Login")

        return self.get_response(request)
