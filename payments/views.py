from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly

import requests
import stripe
from order.models import Order
from .models import Payment
from .serializers import paymentSerializer
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
class CreatePayment(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request, orderId):
        
        user = request.user
        self.check_object_permissions(request, user)
        try:
            order = Order.objects.get(id=orderId)
            if not order.paid:
                intent = stripe.PaymentIntent.create(
                    amount = order.total_amount,
                    currency = 'USD',
                    automatic_payment_methods={
                    'enabled': True,
                    },
                    metadata = {
                        'orderId' : orderId,
                        'userId' : user.id,
                    },
                    receipt_email = request.user.email
                )
                order.paid = True
                order.save()
                payment = Payment.objects.create( amount= intent.amount, currency= intent.currency, stripe_charge_id= intent.id, order= order )
                serializer = paymentSerializer(payment)
                return Response({'clientSecret' : intent['client_secret'], 'stripe-payment': intent, 'data' : serializer.data }, status= status.HTTP_200_OK)
            else:
                return Response({'error' :  "Order already paid"})
        except Exception as e:
            return Response({'error' : str(e)})
        except Order.DoesNotExist:
             return Response({'error' : 'Order not found'})