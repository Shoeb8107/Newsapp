from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm,  AccountAuthenticationForm, AccountUpdateForm, CommentForm
from account.models import Account
from article.models import Article, Comment
from django.core.mail import send_mail

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt


### HOME VIEW ###
def home(request):

    # Creating our Dicts 
    context = {}
    source_selection = []
    categories_selection = []

    # if the user is authenticated
    if request.user.is_authenticated:
        #Getting the Account Object that is logged in 
        accounts = Account.objects.filter(username=request.user).first()
        
        #Adding the corresponding articles for the user view
        source_selection.append("BBC")
        if request.user.categoryTech: categories_selection.append('technology')
        if request.user.categoryPolitics: categories_selection.append('politics')
        if request.user.categorySport: categories_selection.append('sport')
        context['accounts'] = accounts

    #else show default view for non Account users
    else: 
        source_selection.append("BBC")
        categories_selection.append("politics")
    articles = Article.objects.filter(source__in=source_selection, category__in=categories_selection)

    context['articles'] = articles

    comments = Comment.objects.all()
    context['comments'] = comments


    return render(request, 'home.html', context)


### LOGIN/LOGOUT ###
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    #General Login screen
    context = {}
    user = request.user
    #Redirect logged in users to home
    if user.is_authenticated:
        return redirect('home')

    #POST request recieved and logging the user in    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'accounts/login.html', context)


### ACCOUNT VIEW ###


def account_view(request):
    #Redirect not logged in users to login
    if not request.user.is_authenticated:
        return redirect('login')
 
    context = {}
    #Account vierw contains the code to update the users profile
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user) 
        if form.is_valid(): 
            form.save()
            context['success_message'] = "Updated" 
            return redirect('home')
    else: 
        form = AccountUpdateForm(
                                initial = {
                                'username':request.user.username,
                                'profile_pic':request.user.profile_pic,
                                "categoryTech": request.user.categoryTech,
                                "categoryPolitics": request.user.categoryPolitics,
                                "categorySport": request.user.categorySport,
                                            })
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)



def account_delete_done_view(request):
    #Account deletion success message
    return render(request, 'accounts/delete-done.html')


def account_delete_view(request):
    #Account delete method

    if request.user.is_authenticated:
        if request.method =="POST":
            user = request.user
            user.delete()
            return redirect('account-delete-done')
    else:
        return redirect('home')

    return render(request, "accounts/delete.html")


def pic_delete(request):
    #Profile picture deleteion
    if request.user.is_authenticated:
        if request.method =="POST":
            user_current = request.user
            user_current.profile_pic = "default.png"
            user_current.save()
            return redirect('home')
    else:
        return redirect('home')

    return render(request, "accounts/pic-delete.html")



### COMMENTS VIEW ###
def comment_home(request, pk):
    account = Account.objects.filter(username=request.user).first()
    
    article = Article.objects.filter(pk=pk).first()

    comments = Comment.objects.filter(post=article)
    context = {'comments': comments, 'article': article, 'account' : account }

    html_form = render_to_string('accounts/modal-comment.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})



def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            comments = Comment.objects.all()
            data['html_book_list'] = render_to_string('accounts/modal_comment_list.html', {
                'comments': comments
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def comment_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
    else:
        form = CommentForm()
    return save_book_form(request, form, 'accounts/partial_comment_create.html')




def comment_update(request, pk):
    book = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=book)
    else:
        form = CommentForm(instance=book)
    return save_book_form(request, form, 'accounts/partial_comment_update.html')

@csrf_exempt
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    data = dict()
    if request.method == 'DELETE':
        comment.delete()
        data['form_is_valid'] = True  
        comments = Comment.objects.all()
        data['html_book_list'] = render_to_string('accounts/modal_comment_list.html', {
            'comments': comments
        })

    else:
        context = {'comment': comment}
        data['html_form'] = render_to_string('accounts/partial_comment_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)



### FAVOURITES VIEW ###

def checkFavorite(request, pk=None):
    if pk:
        article = Article.objects.get(pk=pk)
        if article.favourite:
            article.favourite = False
        else:
            article.favourite = True
        article.save()

    return redirect('home')



### REGISTRATION VIEW ###
def registration(request):
    context = {}

    if request.user.is_authenticated: 
        return redirect('home')
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            raw_dob = form.cleaned_data.get('DoB')
            raw_email = form.cleaned_data.get('email')
            account = authenticate(username=username, password=raw_password, DoB = raw_dob)

            send_mail('Thank you for signing up!',
            'Thank you for signing up to the Newsapp! I hope you enjoy your experience!',
            'dmclovin1998@gmail.com',
            [raw_email],
            fail_silently=False)

            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)

def favourite(request):
    context = {}
    

    if request.user.is_authenticated == True:
        articles = Article.objects.filter(favourite=True)
        context['articles'] = articles

        return render(request, 'favourite.html', context)
    else:
        return redirect( '../')

