from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import LoginForm


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            # I can't use the helper function, i don't give a fuck.
            # I am not that good at python to figure out why the fuck does calling ModelBackend directly works but using helper function
            # not. I swear I spent fucking 2 hours just for this stupid erorr.
            # Fuck good practice. If you're seeing this, then you might get an idea how stressful this shit for me is. I don't want to
            # do any Django. Period.
            # For other people that experience the same weird error, may god bless you.
            # user = ModelBackend().authenticate(request=request, username=form.cleaned_data['staff_id'], password=form.cleaned_data['password'])
            username = form.cleaned_data.get("staff_id")
            password = form.cleaned_data.get("password")
            # previously `authenticate` does not work, now it works. I don't know why, only god knows.
            # I kept the comment above in check in case well things happen.
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                return redirect(request.session.get("next", "Dashboard"))

            form.add_error(None, "Invalid staff ID or password")
    else:
        form = LoginForm()

    return render(request, "app/login.html", {"form": form})


def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect("Login")
