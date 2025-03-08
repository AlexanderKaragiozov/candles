import random
from operator import index

from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, get_object_or_404, redirect
import json

from django.urls import reverse

from candle.models import Candle, Gallery, CandleOrder, Customer, Contacts
import candle.spreadsheet as spreadsheet
from collections import Counter
# Create your views here.

def home(request):
    last_3_candles = Candle.objects.order_by('-date_added').exclude(monthly=True)[:3]
    monthly_package = Candle.objects.get(monthly=True)

    most_common = (
        CandleOrder.objects.values('candle')  # Group by candle ID
        .annotate(count=Count('candle'))  # Count occurrences
        .order_by('-count')[:3]  # Get the top 3 most common
    )
    most_sold:list= []
    # for candle in most_common:
    #     candle = Candle.objects.get(id=candle['candle'])
    #     most_sold.append(candle)
    promotions = Candle.objects.filter(promotion_price__gt=0)[:3]

    # gallery pull 6 images
    gallery_first_3 = Gallery.objects.all()[:Gallery.objects.count()]

    return render(request,'index.html',{'candles':last_3_candles,'most_ordered':most_sold,'MEDIA_URL': settings.MEDIA_URL,"promotions":promotions, 'gallery_first_3':gallery_first_3,'monthly_package':monthly_package})

def gallery(request):
    gallery = Gallery.objects.all()
    return render(request,'gallery.html',{'gallery':gallery})


def get_cart_from_cookies(request):
    cart = request.COOKIES.get('cart', '{}')  # Get cart from cookies, default to empty if not found
    return json.loads(cart)

# Helper function to save the cart in cookies
def save_cart_to_cookies(response, cart):
    response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*30)  # Store for 30 days

import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Candle

def add_to_cart(request, candle_id):
    if request.method == "POST":

        quantity = int(request.POST.get("quantity", 1))  # Ensure quantity is an integer
        print(f"{candle_id} >>>>>>>>> {quantity}")
        # Get existing cart data from cookies
        cart = request.COOKIES.get("cart", "{}")
        try:
            cart = json.loads(cart)  # Convert JSON string to dictionary
        except json.JSONDecodeError:
            cart = {}

        # Ensure the value is an integer before adding
        cart[str(candle_id)] = cart.get(str(candle_id), 0) + quantity

        # Create response without the message
        response = JsonResponse({"cart": cart})
        print(cart)
        # Store the updated cart in cookies (valid for 7 days)
        response = redirect("cart_view")  # Redirect to cart page

        # Set the cookie properly
        response.set_cookie(
            "cart",
            json.dumps(cart),
            max_age=7 * 24 * 60 * 60,  # 7 days
            httponly=False,
            samesite="Lax"
        )

        return response  # Important: return this response

    return JsonResponse({"error": "Невалидна заявка"}, status=400)



def cart_view(request):
    # Get the cart cookie
    cart = request.COOKIES.get("cart", "{}")

    try:
        cart = json.loads(cart)  # Convert JSON string to Python dictionary
    except json.JSONDecodeError:
        cart = {}
    total_cart_price = 0
    shipping = 0
    amount_needed_for_free_shipping = 0
    total_price_with_shipping = 0
    # Extract candle IDs and quantities
    cart_items = []  # Keep all items, not overwrite
    print(f"cart {cart}")
    for candle_id, quantity in cart.items():
        try:

            candle = Candle.objects.get(pk=int(candle_id))  # Get candle object
            if candle.promotion_price!=0:
                total_cart_price += candle.promotion_price * quantity
            else:
                total_cart_price += candle.price * quantity
            if total_cart_price < 70:
                shipping = 4.99

            cart_items.append({"id": int(candle_id), "name": candle.name, "price": candle.price,"cent":candle.cent,"quantity": quantity, "image": candle.image, 'total_price': candle.price * quantity, 'description': candle.description,"promotion_price":candle.promotion_price})
        except Candle.DoesNotExist:
            continue  # Skip if candle not found
    total_price_with_shipping = round(total_cart_price + shipping,2)
    amount_needed_for_free_shipping = 70-total_cart_price
    context = {"items": cart_items}
    context.update({"total_cart_price": total_cart_price})
    context.update({"shipping": shipping})
    context.update({"total_price_with_shipping": total_price_with_shipping})
    context.update({"needed_amount":amount_needed_for_free_shipping})

    return render(request, "cart2.html", context)
def remove_from_cart(request, candle_id):
    # Get the cart from cookies
    cart = request.COOKIES.get("cart", "{}")
    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    # Remove the item from the cart
    if str(candle_id) in cart:
        del cart[str(candle_id)]  # Delete the item from the cart

    # Save the updated cart in cookies
    response = redirect(reverse('cart_view'))
    response.set_cookie('cart', json.dumps(cart))

    return response
def increase_quantity(request, candle_id):
    # Get the cart from cookies
    cart = request.COOKIES.get("cart", "{}")
    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    # Increase the quantity of the item
    if str(candle_id) in cart:
        cart[str(candle_id)] += 1  # Increase the quantity

    # Save the updated cart in cookies
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.set_cookie('cart', json.dumps(cart))

    return response
def decrease_quantity(request, candle_id):
    # Get the cart from cookies
    cart = request.COOKIES.get("cart", "{}")
    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    # Decrease the quantity of the item (but not below 1)
    if str(candle_id) in cart and cart[str(candle_id)] > 1:
        cart[str(candle_id)] -= 1  # Decrease the quantity

    # Save the updated cart in cookies
    response = redirect(reverse('cart_view'))
    response.set_cookie('cart', json.dumps(cart))

    return response

def remove_from_cart(request, candle_id):
    # Get the cart from cookies
    cart = request.COOKIES.get("cart", "{}")
    try:
        cart = json.loads(cart)
    except json.JSONDecodeError:
        cart = {}

    # Remove the item from the cart
    if str(candle_id) in cart:
        del cart[str(candle_id)]  # Delete the item from the cart

    # Save the updated cart in cookies
    response = redirect(reverse('cart_view'))
    response.set_cookie('cart', json.dumps(cart))

    return response
def products(request):
    products = Candle.objects.all()
    for candle in products:
        candle.price = round(candle.price,2)
    print(products)
    return render(request,'products.html', {'products':products,'MEDIA_URL': settings.MEDIA_URL})


def view_product(request,candle_id):
    other_candle = Candle.objects.all().exclude(monthly=True)[0:4]
    candle = Candle.objects.get(pk=candle_id)

    return render(request,'product_view.html', {'candle':candle,'MEDIA_URL': settings.MEDIA_URL,'other_candle':other_candle})

def fast_buy(request, candle_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))  # Ensure quantity is an integer
        print(f"{candle_id} >>>>>>>>> {quantity}")

        # Get existing cart data from cookies
        cart = request.COOKIES.get("cart", "{}")
        try:
            cart = json.loads(cart)  # Convert JSON string to dictionary
        except json.JSONDecodeError:
            cart = {}

        # Ensure the value is an integer before adding
        cart[str(candle_id)] = cart.get(str(candle_id), 0) + quantity

        # Create response with redirect to cart page
        response = redirect("cart_view")  # Redirect to cart page

        # Set the cookie properly
        response.set_cookie(
            "cart",
            json.dumps(cart),
            max_age=7 * 24 * 60 * 60,  # 7 days
            httponly=False,
            samesite="Lax"
        )

        return response  # Return the redirect response to the cart view


def place_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # last_name = request.POST.get("last_name")
        # email = request.POST.get("email")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        # address = request.POST.get("address")
        parts = name.split()
        if len(parts) == 2:
            first_name,last_name = parts
        else:
            first_name = name
            last_name = ""



        if first_name and last_name and phone and city:
            # Create or get the customer
            customer, created = Customer.objects.get_or_create(
                email='',  # Prevent duplicate customers based on email
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "city": city,
                    "address": ''
                }
            )

            cart = request.COOKIES.get("cart")
            cart = json.loads(cart)
            order = ''
            order_url_code = 0
            # Loop through cart and create orders
            for candle_id, quantity in cart.items():
                try:
                    candle = Candle.objects.get(id=candle_id)  # Ensure candle exists
                    candle.quantity -= quantity
                    candle.save()
                    new_order = CandleOrder.objects.create(
                        customer=customer,
                        candle=candle,
                        quantity=quantity,
                        confirmed=False
                    )

                    order += f"{candle.name}-x{quantity} "
                    order_url_code += candle.id * quantity * 100
                except Candle.DoesNotExist:
                    print(f"Candle with ID {candle_id} not found.")
            order_url_code= str(order_url_code) + f"{customer.first_name.lower()}x{customer.last_name.lower()}"
            SPREADSHEET_ROW = [new_order.id,first_name, last_name, '', phone, city, '']
            SPREADSHEET_ROW.append(order)
            SPREADSHEET_ROW.append("НЕ")
            SPREADSHEET_ROW.append('НЕ')
            # Clear cart after placing order
            # request.session["cart"] = {}
            spreadsheet.append_to_sheet(SPREADSHEET_ROW)

            return render(request,"order_complete.html")
 # Redirect to an order success page

    return redirect("home")



def request_help(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        problem = request.POST.get("description")

        Contacts.objects.create(email=email, phone=phone, title=subject, problem=problem)
        home_url = reverse('home')  # Get the URL of the 'home' view
        messages.success(request, "✅ Успешно изпратена заявка!")
        return redirect(home_url + '#message')  # Append the fragment

def lichni_danni(request):
    return render(request,'lichni-danni.html')

def biscuits(request):
    return render(request,'Biscuits.html')
def tos(request):
    return render(request,'tos.html')
