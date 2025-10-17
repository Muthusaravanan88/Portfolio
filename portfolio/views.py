from django.shortcuts import render,redirect  
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.conf import settings
import threading
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import threading
from django.core.mail import EmailMessage



def home(request):
    return render(request,'home.html')

def contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            body = f"""
            New Contact Form Submission:

            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """
            email_message = EmailMessage(
                subject=f"Portfolio Message: {subject}",
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['muthusaravananb.sc@gmail.com'],
            )
            email_message.send(fail_silently=False)
            return JsonResponse({'success': True, 'message': 'Email sent successfully'})
        except Exception as e:
            print("Email sending failed:", e)
            return JsonResponse({'success': False, 'message': 'Error sending email'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
