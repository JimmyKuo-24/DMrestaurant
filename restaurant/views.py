from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import  ProfileForm, ReservationForm, OrderForm
from .models import TimeSlot, Order, Cuisine, Profile
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def homepage(request):
    if request.user.is_active:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()

                user_email = request.user.email
                reservation_date = reservation.time_slot.date
                reservation_time = reservation.time_slot.time

                email_subject = 'Reservation Confirmation'
                email_message = f'Dear {request.user.first_name} {request.user.last_name},\n\nThank you for your reservation on {reservation_date} at {reservation_time}. We will contact you shortly to confirm your reservation.\n\nBest regards,\nThe Restaurant Team'
                try:
                    send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
                    logger.info(f'Reservation email sent to {user_email}')
                    messages.success(request, 'Reservation submitted successfully. Please check your email for confirmation. You can also choose cuisines before arriving.')
                except Exception as e:
                    logger.error(f'Error sending reservation email to {user_email}: {e}')
                    messages.error(request, 'Error sending reservation email. Please try again later.')

                return redirect('homepage')
        else:
            form = ReservationForm()

        time_slots = TimeSlot.objects.all()
        return render(request, 'restaurant/homepage.html', {'form': form, 'time_slots': time_slots})
    messages.info(request, 'Welcome to 【Danjon Meshi Restaurant】. Reservation-only restaurant for dine-in use! Please login or register to make a reservation.')
    return render(request, 'restaurant/homepage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.is_active = True
            user.email = profile_form.cleaned_data.get('email')
            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'restaurant/register.html', {'form': form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_id = request.user.id
            profile = Profile.objects.get(user_id=user_id)
            if user.is_staff:
                return redirect('homepage')
            elif profile.is_gourmet and profile.is_cook:
                return redirect('homepage')
            elif profile.is_gourmet:
                return redirect('gourmet')
            elif profile.is_cook:
                return redirect('cook')
            else: 
                return render(request, 'restaurant/login.html', {'form': form, 'error': 'Account not approved yet.'})
    else:
        form = AuthenticationForm()
    return render(request, 'restaurant/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def gourmet(request):
    user = request.user
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    if user.is_staff or profile.is_gourmet:
        return render(request, 'restaurant/gourmet.html')
    else:
        return redirect('homepage')

@login_required
def cook(request):
    user = request.user
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    if user.is_staff or profile.is_cook:
        return render(request, 'restaurant/cook.html')
    else:
        return redirect('homepage')


@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        user = request.user
        if user.is_active:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    cuisines = Cuisine.objects.all()    
    return render(request, 'restaurant/order.html', {'form': form, 'cuisines': cuisines})

@login_required
def order_confirmation(request, order_id):
    try:
        orders = Order.objects.filter(user=request.user, status='Pending')
        total_price = sum(order.cuisine.price * order.quantity for order in orders)
        if request.method == 'POST':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                new_order = order_form.save(commit=False)
                new_order.user = request.user
                new_order.status = 'Pending'
                new_order.save()
                return redirect('order_confirmation', order_id=new_order.id)
    except ObjectDoesNotExist:
        logger.error('Order does not exist.')
        return redirect('order')
    
    order_totals = []
    for order in orders:
        order_total = order.cuisine.price * order.quantity
        order_totals.append({
            'order': order,
            'order_total': order_total,
        })

    return render(request, 'restaurant/order_confirmation.html', {
        'orders': order_totals,
        'total_price': total_price,
        'order_form': OrderForm(),
        'order_id': order_id,
        })
    

@login_required
def order_confirm(request, order_id):
    try:
        orders = Order.objects.filter(user=request.user, status='Pending')
        total_price = sum(order.cuisine.price * order.quantity for order in orders)
        try:
            send_mail(
                'Order Confirmation',
                f'Thank you for your order, {request.user.first_name} {request.user.last_name}. You have ordered the following items：\n\n' + '\n'.join([f'{order.cuisine.name} x {order.quantity}' for order in orders]) + f'\n\nTotal price：$ {total_price:.0f} TWD.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            orders.update(status='Confirmed')
            messages.success(request, 'Order submitted successfully. Please check your email for confirmation. Don\'t click button again！')
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(request, 'Error sending reservation email. Please try again later.')
        return redirect('order_confirmation', order_id=order_id)
    except ObjectDoesNotExist:
        logger.error('Order does not exist.')
    return redirect('order_confirmation', order_id=order_id)

@login_required
def order_increase(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    order.quantity += 1
    order.save()
    return redirect('order_confirmation', order_id=order_id)

@login_required
def order_decrease(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    if order.quantity > 1:
        order.quantity -= 1
        order.save()
    return redirect('order_confirmation', order_id=order_id)

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending')
    order.delete()
    return redirect('order_confirmation', order_id=order_id)

@login_required
def add_item_to_order(request, order_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.status = 'Pending'
            new_order.save()
    return redirect('order_confirmation', order_id=order_id)
