from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from myApp.forms import RegistrationForm,LoginForm
from django.core.mail import send_mail
from myApp.tasks import send_mail_task

# importing for reset password
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomSetPasswordForm,CustomPasswordResetForm

# importing for products
from .models import ProductCategory
from django.core.paginator import Paginator

# Create your views here.

# function for rendering home page
def home(request):
     return render(request,'myApp/home.html')


def registrationView(request):
     if request.method == 'POST':
          form=RegistrationForm(request.POST)
          if form.is_valid():
               user=form.save()
               login(request,user)
               email=form.cleaned_data.get('email')
               send_mail_task.delay(email)
               messages.success(request,"registration successfully")
               form=RegistrationForm()
          else:
               messages.error(request,"form values are not valid")     
               return redirect("register")
     else:
          form=RegistrationForm()
     return render(request,'myApp/register.html',{'form':form}) 



def loginView(request):
     if request.method == 'POST':
          form=LoginForm(data=request.POST)   
          if form.is_valid():
               uname=form.cleaned_data['username']
               upass=form.cleaned_data['password']
               user=authenticate(username=uname,password=upass) 

               if user is not None:
                    login(request,user)
                    messages.success(request,'login Successfully')
                    form = LoginForm() 
                    return redirect('home')
               else:
                    messages.error(request,"somethis is wenting wrong")
          else:
               messages.error(request,"form values are not valid") 
                      
     else:
          form=LoginForm()          
     return render(request,'myApp/login.html',{'form':form})     


def logoutView(request):
     logout(request)
     messages.success(request,"logged out successfully.")
     return redirect('home')



# view for forgot password

def password_reset(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            user = User.objects.filter(email=data).first()
            if user:
                    subject = "Password Reset Requested"
                    email_template_name = "myApp/password_reset_email.html"
                    c = {
                        # "email": user.email,
                        'domain': '127.0.0.1:8000',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),            
                    }
                    print(c)
                    email = render_to_string(email_template_name, c)
                    try:
                        # subject, email, 'manikak220@gmail.com', [user.email], fail_silently=False --> parameters of send_mail
                        send_mail(subject, email, 'manikak220@gmail.com', [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse('Invalid header found.')
            return redirect("password_reset_done")
    form = CustomPasswordResetForm()
    return render(request=request, template_name="myApp/password_reset_form.html", context={"form":form})


# 
def password_reset_done(request):
    return render(request, 'myApp/password_reset_done.html')    




# Password reset confirm view
def password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'myApp/password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('Password reset link is invalid!')
    

# Password reset complete view
def password_reset_complete(request):
    return render(request, 'myApp/password_reset_complete.html')    

# views for products categories
def product_categories(request):
    search_query= request.GET.get('search',"")
     # Get entries from request or default to 3
    entries_per_page = int(request.GET.get('entries', 3)) 
    if search_query:
          categories_list = ProductCategory.objects.filter(name__icontains=search_query)   
    else:
          categories_list=ProductCategory.objects.all() 

      # Show entries_per_page categories per page -->(categories_list,per_page=3)
    paginator=Paginator(categories_list,entries_per_page) 
    page_number = request.GET.get('page')        
    page_obj = paginator.get_page(page_number)
    context={
        "categories": page_obj,
        "total_entries": paginator.count,
        "search_query": search_query,
        "entries_per_page": entries_per_page,
     }
    return render(request, 'myApp/product_categories.html',context)    

def create_product_category(request):
    if request.method=="POST":
          name=request.POST.get('name')
          description=request.POST.get('description')
          status=request.POST.get('status')
          try:  
            post=ProductCategory.objects.create(name=name,description=description,status=status)
            post.save()
            messages.success(request,"created successfully")
            post=ProductCategory()
            return redirect('/create_product_category')
          except Exception as e:
               print(e) 
    else:               
       return render(request,'myApp/createProductCategory.html',)
    
def delete_product_category(request,id):
    product_category=ProductCategory.objects.get(pk=id)
    if request.method == "POST":
        product_category.delete()
        messages.success(request,"deleted successfully")
        return redirect('/product_categories')
    else:
         return render(request,'myApp/productCategoryDelete.html',{'product_category':product_category})
 
          
           
def update_product_category(request,id):
    product_category=ProductCategory.objects.get(pk=id)
    if request.method == "POST":
         
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')

        try:
            product_category.name = name
            product_category.description = description
            product_category.status = status
            product_category.save()

            messages.success(request, "Updated successfully")
            return redirect('/product_categories')
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while updating the product category")

    return render(request, 'myApp/updateProductCategory.html', {'product_category': product_category})