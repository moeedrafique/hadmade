from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import OrderForm
from .models import Order, OrderLineItem

from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.sessionbag import bag_contents
from products.models import Product
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    A view to return the bag page checkout.html
    """
    # stripe_public_key = settings.STRIPE_PUBLIC_KEY
    # stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag')

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'address1': request.POST['address1'],
            'address2': request.POST['address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # pid = request.POST.get('client_secret').split('_secret')[0]
            # order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, size_level in bag.items():
                for size, color_level in size_level.items():
                    for color, qty in color_level.items():
                        try:
                            product = Product.objects.get(id=item_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                product_size=size,
                                product_color_name=color,
                                quantity=qty
                            )
                            order_line_item.save()
                        except Product.DoesNotExist:
                            messages.error(request, (
                                "One of the products in your bag wasn't found in our database. "
                                "Please call us for assistance!"))
                            order.delete()
                            return redirect(reverse('bag'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                        Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('products', kwargs={'category_name': 'All'}))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        # stripe_total = round(total * 100)
        # stripe.api_key = stripe_secret_key
        # intent = stripe.PaymentIntent.create(
        #     amount=stripe_total,
        #     currency=settings.STRIPE_CURRENCY,
        # )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'country': profile.country,
                    'postcode': profile.postcode,
                    'town_or_city': profile.town_or_city,
                    'address1': profile.address1,
                    'address2': profile.address2,
                    'county': profile.county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        # if not stripe_public_key:
        #     messages.warning(request, 'Stripe public key is missing.')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            # 'stripe_public_key': stripe_public_key,
            # 'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    order_line_items  = OrderLineItem.objects.filter(order=order)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'phone_number': order.phone_number,
                'country': order.country,
                'postcode': order.postcode,
                'town_or_city': order.town_or_city,
                'address1': order.address1,
                'address2': order.address2,
                'county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    # Send confirmation email
    subject = 'Order Confirmation' + '' + '#' + order_number
    html_message = render_to_string('emails/order_confirmation.html', {'order': order,'order_line_items': order_line_items})
    plain_message = strip_tags(html_message)  # Strip HTML tags for plain text version
    from_email = 'your@example.com'  # Change this to your email address
    to_email = order.email
    #
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'order_line_items': order_line_items,
    }

    return render(request, template, context)
