from django.conf import settings
from django.shortcuts import render, redirect, reverse

import stripe


# Create your views here.
def donate(request):
    """ a view to to return the landing page """

    user = request.user
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'user': user,
        'stripe': stripe,
    }

    return render(request, 'donations/donate.html', context)


def charge(request):
    amount = 5
    if request.method == 'POST':
        print('Data:', request.POST)

    return redirect(reverse('success', args=[amount]))


def success(request, args):
    amount = args

    context = {
        'amount': amount,
        'currency': '€',
    }
    return render(request, 'donations/success.html', context)
