from django.shortcuts import redirect, render
from django.urls import reverse
from splitwise import Splitwise

def splitwise_auth(request):
    # Replace with your own consumer key and consumer secret
    consumer_key = "Dax89deUEI7YN9WHMwvqNx8hz1yWnYlTXaillgXF"
    consumer_secret = "HHLJmrpGzM96uHzsOrTS6hHQPmRYE8s45XHSO9Xn"
    
    # Create a Splitwise object
    sObj = Splitwise(consumer_key, consumer_secret)
    
    # Get the authorization URL and secret
    url, secret = sObj.getAuthorizeURL()
    
    # Store the secret value in the user's session
    request.session['splitwise_secret'] = secret
    
    # Redirect the user to the authorization URL
    return redirect(url)

# Map the splitwise_auth view to the /splitwise/auth/ URL

def home(request):
    return render(request, 'splitWise/home.html')
