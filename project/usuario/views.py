from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .domain.services import messages_service

@login_required
def profile(request):
    user = request.user

    if request.method == 'GET':
        form = ProfileForm(
            initial={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
            }
        )

        context = {
            "form": form,
            "user": user
        }
        return render(request, "usuario/profile.html", context)
        
    elif request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages_service.updated_profile(request)
        
        return redirect('usuario:profile')
