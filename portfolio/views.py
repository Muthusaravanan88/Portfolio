from django.shortcuts import render,redirect  
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.conf import settings
import threading
from django.contrib import messages


def home(request):
    return render(request,'home.html')

# Background thread for sending email
class EmailThread(threading.Thread):
    def __init__(self, subject, text_content, html_content, from_email, to_email):
        self.subject = subject
        self.text_content = text_content
        self.html_content = html_content
        self.from_email = from_email
        self.to_email = to_email
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.text_content,
            from_email=self.from_email,
            to=self.to_email
        )
        email.attach_alternative(self.html_content, "text/html")
        email.send(fail_silently=False)


def contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['muthusaravananb.sc@gmail.com']

            # Plain text
            text_content = f"""
            You have received a new message from your portfolio contact form.

            Name: {name}
            Email: {mail}
            Subject: {subject}
            Message: {message}
            """

            # HTML version
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>New Contact Message</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {mail}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Message:</strong><br>{message}</p>
            </body>
            </html>
            """

            # Send in background thread
            EmailThread(subject, text_content, html_content, from_email, to_email).start()

            # Success message
            messages.success(request, "✅ Your message has been sent successfully. Thank you!")

        except Exception as e:
            print("Error sending email:", e)
            messages.error(request, "❌ Something went wrong while sending your message. Please try again later.")

        return redirect('home')
