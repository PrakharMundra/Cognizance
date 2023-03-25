from django.shortcuts import redirect, render
from django.urls import reverse
from splitwise import Splitwise,Expense,User
from .config import Config
from django.conf import settings
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from django.contrib import messages
from splitwise.error import SplitwiseError
import random

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


def splitwise_oauth_callback(request):
    print(request.session['splitwise_secret'])
    oauth_token = request.GET.get('oauth_token')
    oauth_verifier = request.GET.get('oauth_verifier')
    sObj = Splitwise("Dax89deUEI7YN9WHMwvqNx8hz1yWnYlTXaillgXF", "HHLJmrpGzM96uHzsOrTS6hHQPmRYE8s45XHSO9Xn")
    access_token = sObj.getAccessToken(oauth_token, request.session['splitwise_secret'], oauth_verifier)
    request.session['splitwise_access_token'] = access_token
    return redirect('groups')


# def splitwise_friends(request):
#     # Retrieve the access token from the session
#     access_token = request.session.get('splitwise_access_token')

#     # Create a Splitwise object and set the access token
#     sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
#     sObj.setAccessToken(access_token)

#     # Retrieve the user's friends from Splitwise
#     friends = sObj.getFriends()
#     # for friend in friends:
#         # print(friend)
#         # print(friend.getId())
#         # print(friend.getFirstName())
#         # print(friend.getLastName())
#         # print(friend.getEmail())
#         # print(friend.getDisplayName())
#         # print(friend.getPicture())

#     # Render the friends template with the list of friends
#     return render(request, 'splitWise/friends.html', {'friends': friends})

def groups(request):
    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(request.session['splitwise_access_token'])
    groups = sObj.getGroups()
    return render(request, 'splitWise/groups.html', {'groups': groups})

def get_group(request, group_id):
    sObj = Splitwise("Dax89deUEI7YN9WHMwvqNx8hz1yWnYlTXaillgXF", "HHLJmrpGzM96uHzsOrTS6hHQPmRYE8s45XHSO9Xn")
    sObj.setAccessToken(request.session['splitwise_access_token'])

    group = sObj.getGroup(group_id)

    # Do something with the group information
    # ...

    return render(request, 'splitWise/group.html', {'group': group})

# def add_expense(request, group_id):
#     sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
#     sObj.setAccessToken(request.session['splitwise_access_token'])
#     group = sObj.getGroup(group_id)
#     users = group.getMembers()

#     if request.method == 'POST':
#         payer_id = request.POST['payer']
#         expense = Expense()
#         expense.setCost(request.POST['amount'])
#         expense.setDescription(request.POST['description'])

#         # Set up payer and calculate owed shares
#         payer = next((user for user in users if str(user.getId()) == payer_id), None)
#         print(payer)
#         payer_share = float(request.POST['amount']) / len(users)
#         print(payer_share)
#         users_owed_shares = [str(round(payer_share, 2))] * len(users)
#         print(users_owed_shares)
#         users_owed_shares[users.index(payer)] = str(round(float(request.POST['amount']) - payer_share, 2))

#         # Set up users and add to expense
#         expense_users = []
#         for user, owed_share in zip(users, users_owed_shares):
#             expense_user = ExpenseUser()
#             expense_user.setId(user.getId())
#             expense_user.setPaidShare('0.00')
#             expense_user.setOwedShare(owed_share)
#             expense_users.append(expense_user)
        
#         expense.setUsers(expense_users)
        
#         # Create the expense and redirect to group view
#         expense, errors = sObj.createExpense(expense)
#         return redirect('expense_details', expense_id=expense.getId())

#     return render(request, 'splitWise/add_expense.html', {'users': users})

def add_expense(request, group_id):
    if request.method == 'POST':
        sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
        sObj.setAccessToken(request.session['splitwise_access_token'])

        # Get the selected user
        
        # Get the list of group members
        group = sObj.getGroup(group_id)
        members = group.getMembers()
        payer = random.choice(members)
        payer_id = payer.id
        # Calculate the split equally amount
        amount = request.POST.get('amount')
        split_equally = request.POST.get('split_equally')
        amount_per_person=0
        if split_equally:
            num_members = len(members)
            amount_per_person = round(float(amount) / num_members, 2)

        # Create the expense object
        expense = Expense()
        expense.setCost(amount)
        expense.setDescription(request.POST.get('description'))
        expense.setGroupId(group_id)
        payer = next((user for user in members if user.getId() == payer_id), None)
        print(payer.getFirstName())
        # expense.setDetails(payer.getFirstName())
        # expense.addUser(payer_id)
        expense.setCurrencyCode("INR")
        expense.setUsers([])
        expense.setSplitEqually(split_equally)

        # Add the users to the expense object
        for member in members:
            user = ExpenseUser()
            user.setId(member.getId())
            if member.getId() == payer_id:
                user.setPaidShare(amount)
                user.setOwedShare("0.00")
            else:
                user.setPaidShare("0.00")
                user.setOwedShare(str(amount_per_person))
            expense.getUsers().append(user)

        # Create the expense on Splitwise
        try:
            expense = sObj.createExpense(expense)
            print(expense)
        except :
         # Handle the exception here
            print("Error creating expense:")

        if expense:
            # Redirect to the expense details page
            # return redirect('expense_details', kwargs={'expense_id': expense.getId(), 'group_id': group_id})
            return redirect('get_group', group_id=group_id)
        else:
            print("f")

    else:
        # Get the list of group members
        sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
        sObj.setAccessToken(request.session['splitwise_access_token'])
        group = sObj.getGroup(group_id)
        members = group.getMembers()
        payer = random.choice(members)

        # Render the add expense form
        return render(request, 'splitWise/add_expense.html', {'group_id': group_id, 'members': members,'payer': payer})

def add_expense_normal(request, group_id):
    if request.method == 'POST':
        sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
        sObj.setAccessToken(request.session['splitwise_access_token'])

        # Get the selected user
        payer_id = int(request.POST.get('payer'))

        # Get the list of group members
        group = sObj.getGroup(group_id)
        members = group.getMembers()

        # Calculate the split equally amount
        amount = request.POST.get('amount')
        split_equally = request.POST.get('split_equally')
        amount_per_person=0
        if split_equally:
            num_members = len(members)
            amount_per_person = round(float(amount) / num_members, 2)

        # Create the expense object
        expense = Expense()
        expense.setCost(amount)
        expense.setDescription(request.POST.get('description'))
        expense.setGroupId(group_id)
        payer = next((user for user in members if user.getId() == payer_id), None)
        print(payer.getFirstName())
        # expense.setDetails(payer.getFirstName())
        # expense.addUser(payer_id)
        expense.setCurrencyCode("INR")
        expense.setUsers([])
        expense.setSplitEqually(split_equally)

        # Add the users to the expense object
        for member in members:
            user = ExpenseUser()
            user.setId(member.getId())
            if member.getId() == payer_id:
                user.setPaidShare(amount)
                user.setOwedShare("0.00")
            else:
                user.setPaidShare("0.00")
                user.setOwedShare(str(amount_per_person))
            expense.getUsers().append(user)

        # Create the expense on Splitwise
        try:
            expense = sObj.createExpense(expense)
            print(expense)
        except :
         # Handle the exception here
            print("Error creating expense:")

        if expense:
            # Redirect to the expense details page
            # return redirect('expense_details', kwargs={'expense_id': expense.getId(), 'group_id': group_id})
            return redirect('get_group', group_id=group_id)
        else:
            print("f")

    else:
        # Get the list of group members
        sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
        sObj.setAccessToken(request.session['splitwise_access_token'])
        group = sObj.getGroup(group_id)
        members = group.getMembers()

        # Render the add expense form
        return render(request, 'splitWise/add_expense_normal.html', {'group_id': group_id, 'members': members})




def expense_details(request, expense_id):
    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(request.session['splitwise_access_token'])

    expense = sObj.getExpense(expense_id)
    group = sObj.getGroup(expense.getGroupId())
    users = expense.getUsers()

    return render(request, 'splitWise/expense_details.html', {'expense': expense, 'group': group, 'users': users})