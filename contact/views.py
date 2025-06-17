from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer
from .models import Contact

class ContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Send email
            subject = f"Nouveau message de contact: {contact.subject}"
            message = f"""
            Nouveau message de contact reçu :
            
            Nom: {contact.name}
            Email: {contact.email}
            Sujet: {contact.subject}
            Message: 
            {contact.message}
            
            Date: {contact.created_at}
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
