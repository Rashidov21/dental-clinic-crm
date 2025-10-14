from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('dashboard_page')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'user': request.user})


def set_language(request):
    """Custom language switcher that works with our translation system"""
    if request.method == 'GET':
        language = request.GET.get('language', 'uz')
        next_url = request.GET.get('next', '/')
        
        # Set language in session
        request.session['django_language'] = language
        
        # Redirect to the next URL
        return redirect(next_url)
    
    return redirect('/')


# API endpoints for AJAX requests
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@require_http_methods(["POST"])
@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})