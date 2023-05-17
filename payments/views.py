from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from order.models import Order,OrderItem
from products.models import Product
from .models import Payment
from .serializers import paymentSerializer
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY
class CreatePayment(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request, orderId):
        
        user = request.user
        self.check_object_permissions(request, user)
        try:
            order = Order.objects.get(id=orderId)
            orderExists= Payment.objects.filter(order = order.id)
            if not orderExists:
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
                payment = Payment.objects.create( amount= intent.amount, currency= intent.currency, stripe_charge_id= intent.id, order= order ,status=intent.status)
                serializer = paymentSerializer(payment)
                return Response({'clientSecret' : intent['client_secret'], 'stripe-payment': intent, 'data' : serializer.data }, status= status.HTTP_200_OK)
            else:
                return Response({'error' :  "Order already paid"})
        except Exception as e:
            return Response({'error' : str(e)})
        except Order.DoesNotExist:
            return Response({'error' : 'Order not found'})
        
class CancelPayment(APIView):

    def cancellation(self,payment):
        stripeCancellation = stripe.PaymentIntent.cancel(
                    payment.stripe_charge_id,
                )
        payment.status = stripeCancellation.status
        payment.save()

    def __private_get(self , orderId):
            payment = Payment.objects.filter(order=orderId).first()
            query = "metadata['orderId']:'"+ str(orderId)+"'"
            currentStatus = stripe.PaymentIntent.search(
            query=query,
            )
            if payment.status != currentStatus.data[0].status:
                payment.status = currentStatus.data[0].status
                payment.save()
            return payment

    def resetQuantity(self, order):
        try:
            orderItems = OrderItem.objects.filter(order=order)
            for item in orderItems:
                product = Product.objects.get(id=item.product.id)
                product.quantity += item.quantity
                product.save()
        except OrderItem.DoesNotExist:
            raise ValidationError('OrderItem not found')
        except Product.DoesNotExist:
            raise ValidationError('Product not found')
        except Exception as e:
            raise Exception(e)
        
    def post(self, request,orderId):
        user = request.user
        self.check_object_permissions(request, user)
    
        try:
            order = Order.objects.get(id=orderId)
            payment = self.__private_get(order.id)
            date_now = timezone.now()
            two_days_ago = payment.created_at + timezone.timedelta(days=1)

            if not payment.status == 'canceled' or payment.status == 'succeeded':
                if not payment.created_at > two_days_ago:
                    self.cancellation(payment)
                    # stripeRefund = stripe.Refund.create(payment_intent=payment.stripe_charge_id, amount=payment.amount)
                    self.resetQuantity(order)
                    return Response({'data' : '1' }, status= status.HTTP_200_OK)
                else :
                    self.cancellation(payment)
                    two_days_after_created_at = payment.created_at + timezone.timedelta(days=1)
                    difference = (date_now - two_days_after_created_at).days
                    total_fee = int(difference*5)
                    # stripeRefund = stripe.Refund.create(payment_intent=payment.stripe_charge_id, amount=(payment.amount - total_fee))
                    self.resetQuantity(order)
                    return Response({'data' : '2' }, status= status.HTTP_200_OK)
                
            else:
                return Response({'error' : 'The payment already canceled' }, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error' : str(e)})
        
class UpdatePayment(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def put(self, request, orderId):
            user = request.user
            self.check_object_permissions(request, user)
            payment = Payment.objects.filter(order=orderId).first()
            query = "metadata['orderId']:'"+ str(orderId)+"'"
            currentStatus = stripe.PaymentIntent.search(
            query=query,
            )
            if payment.status != currentStatus.data[0].status:
                payment.status = currentStatus.data[0].status
                payment.save()
            return Response(status= status.HTTP_204_NO_CONTENT)