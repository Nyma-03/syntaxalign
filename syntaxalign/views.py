from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import SignUpForm, LeadForm

def home(request):
    return render(request,'home.html')

def services(request):
    return render(request,'services.html')

def work(request):
    return render(request,'work.html')

def pricing(request):
    products = Product.objects.all()
    return render(request,'pricing.html',{'products':products})

def products_list(request):
    return render(request,'products.html', {'products': Product.objects.all()})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        Order.objects.create(user=request.user, product=product)
        return redirect('dashboard')
    return render(request,'product_detail.html',{'product':product})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'signup.html', {'form':form})

def contact(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LeadForm()
    return render(request,'contact.html', {'form':form})

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'dashboard.html',{'orders':orders})


def pricing(request):
    products = Product.objects.all()  # Get all products from DB
    return render(request, 'pricing.html', {'products': products})


def design(request):
    return render(request, 'design.html')

def development(request):
    return render(request, 'development.html')


from django.shortcuts import render, redirect
from .models import DevelopmentInquiry
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def start_development(request):
    if request.method == "POST":
        project_type = request.POST.get("project_type")

        errors = []

        # Validation functions
        name_pattern = re.compile(r'^[A-Za-z\s]{2,50}$')
        phone_pattern = re.compile(r'^\+?[\d\s\-]{7,15}$')
        budget_pattern = re.compile(r'^\d+(\.\d{1,2})?$')

        # Common validations
        if project_type not in ["business","personal"]:
            errors.append("Please select a valid project type.")

        if project_type == "business":
            # Required fields
            company_name = request.POST.get("company_name")
            company_email = request.POST.get("company_email")
            company_phone = request.POST.get("company_phone")
            employee_name = request.POST.get("employee_name")
            employee_phone = request.POST.get("employee_phone")
            employee_email = request.POST.get("employee_email")
            budget_range = request.POST.get("budget_range")
            timeline = request.POST.get("timeline")

            # Name validations
            if not company_name or not name_pattern.match(company_name):
                errors.append("Invalid company name.")
            if not employee_name or not name_pattern.match(employee_name):
                errors.append("Invalid employee name.")

            # Email validations
            for email_field, email_value in [("Company Email", company_email),
                                             ("Employee Email", employee_email)]:
                try:
                    validate_email(email_value)
                except ValidationError:
                    errors.append(f"Invalid {email_field}.")

            # Phone validations
            for phone_field, phone_value in [("Company Phone", company_phone),
                                             ("Employee Phone", employee_phone)]:
                if not phone_value or not phone_pattern.match(phone_value):
                    errors.append(f"Invalid {phone_field}.")

            # Budget
            if budget_range and not budget_pattern.match(budget_range):
                errors.append("Invalid budget format.")

            if errors:
                return render(request, "start_development.html", {"errors": errors})

            # Save
            DevelopmentInquiry.objects.create(
                project_type=project_type,
                company_name=company_name,
                company_email=company_email,
                company_phone=company_phone,
                employee_name=employee_name,
                employee_phone=employee_phone,
                employee_email=employee_email,
                company_address=request.POST.get("company_address"),
                designation=request.POST.get("designation"),
                backup_phone=request.POST.get("backup_phone"),
                backup_email=request.POST.get("backup_email"),
                project_scope=request.POST.get("project_scope"),
                budget_range=budget_range,
                timeline=timeline
            )

        else:  # personal
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            estimated_budget = request.POST.get("estimated_budget")
            preferred_timeline = request.POST.get("preferred_timeline")

            # Name check
            if not full_name or not name_pattern.match(full_name):
                errors.append("Invalid full name.")

            # Email check
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Invalid email address.")

            # Phone check
            if not phone or not phone_pattern.match(phone):
                errors.append("Invalid phone number.")

            # Budget check
            if estimated_budget and not budget_pattern.match(estimated_budget):
                errors.append("Invalid budget format.")

            if errors:
                return render(request, "start_development.html", {"errors": errors})

            # Save
            DevelopmentInquiry.objects.create(
                project_type=project_type,
                full_name=full_name,
                phone=phone,
                email=email,
                personal_project_details=request.POST.get("personal_project_details"),
                estimated_budget=estimated_budget,
                preferred_timeline=preferred_timeline
            )

        return redirect("thank_you")

    return render(request, "start_development.html")

# from django.shortcuts import render, redirect
# from .models import DevelopmentInquiry

# def start_development(request):

#     if request.method == "POST":
#         project_type = request.POST.get("project_type")

#         inquiry = DevelopmentInquiry.objects.create(
#             project_type=project_type,

#             # Business
#             company_name=request.POST.get("company_name"),
#             company_address=request.POST.get("company_address"),
#             company_email=request.POST.get("company_email"),
#             company_phone=request.POST.get("company_phone"),

#             employee_name=request.POST.get("employee_name"),
#             designation=request.POST.get("designation"),
#             employee_phone=request.POST.get("employee_phone"),
#             employee_email=request.POST.get("employee_email"),

#             backup_phone=request.POST.get("backup_phone"),
#             backup_email=request.POST.get("backup_email"),

#             project_scope=request.POST.get("project_scope"),
#             budget_range=request.POST.get("budget_range"),
#             timeline=request.POST.get("timeline"),

#             # Personal
#             full_name=request.POST.get("full_name"),
#             phone=request.POST.get("phone"),
#             email=request.POST.get("email"),

#             personal_project_details=request.POST.get("personal_project_details"),
#             estimated_budget=request.POST.get("estimated_budget"),
#             preferred_timeline=request.POST.get("preferred_timeline"),
#         )

#         return redirect("thank_you")

#     return render(request, "start_development.html")


def thank_you(request):
    return render(request, "thank_you.html")


from .models import DesignInquiry
def start_design(request):

    if request.method == "POST":

        DesignInquiry.objects.create(
            project_type=request.POST.get("project_type"),
            design_type=request.POST.get("design_type"),

            company_name=request.POST.get("company_name"),
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),

            short_description=request.POST.get("short_description"),

            proposed_offer=request.POST.get("proposed_offer"),
            expected_duration=request.POST.get("expected_duration"),
        )

        return redirect("thank_you")

    return render(request, "start_design.html")



from django.shortcuts import render, redirect
from .models import Product
from .forms import PurchaseRequestForm

def buy_now(request):
    category = request.GET.get('category')
    if category in ['graphic', 'development']:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    return render(request, 'buy_now.html', {'products': products})

def purchase_request(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'purchase_success.html', {'product': product})
    else:
        form = PurchaseRequestForm(initial={'product': product})
    return render(request, 'purchase_request.html', {'form': form, 'product': product})



from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
