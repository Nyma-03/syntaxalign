from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{7,15}$',
    message="Phone number must contain 7-15 digits and may include +, spaces or -"
)

name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]{2,50}$',
    message="Name must contain only letters and spaces (2-50 characters)"
)

class LegacyProduct(models.Model):  # renamed from Product
    PRODUCT_TYPES = (('frontend','Frontend'),('fullstack','Full-Stack'),('design','Graphics/Design'))
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(LegacyProduct, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models

class DevelopmentInquiry(models.Model):

    PROJECT_TYPE_CHOICES = (
        ('business', 'Business'),
        ('personal', 'Personal'),
    )

    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)

    # ===== Business Fields =====
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_phone = models.CharField(max_length=50, blank=True, null=True,validators=[phone_validator])

    employee_name = models.CharField(max_length=255, blank=True, null=True, validators=[name_validator])
    designation = models.CharField(max_length=255, blank=True, null=True)
    employee_phone = models.CharField(max_length=50, blank=True, null=True, validators=[phone_validator])
    employee_email = models.EmailField(blank=True, null=True)

    backup_phone = models.CharField(max_length=50, blank=True, null=True, validators=[phone_validator])
    backup_email = models.EmailField(blank=True, null=True)

    project_scope = models.TextField(blank=True, null=True)
    budget_range = models.CharField(max_length=100, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)

    # ===== Personal Fields =====
    full_name = models.CharField(max_length=255, blank=True, null=True, validators=[name_validator])
    phone = models.CharField(max_length=50, blank=True, null=True, validators=[phone_validator])
    email = models.EmailField(blank=True, null=True)

    personal_project_details = models.TextField(blank=True, null=True)
    estimated_budget = models.CharField(max_length=100, blank=True, null=True)
    preferred_timeline = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.project_type == "business":
            return f"Business Inquiry - {self.company_name}"
        return f"Personal Inquiry - {self.full_name}"




class DesignInquiry(models.Model):

    PROJECT_TYPE_CHOICES = (
        ('business', 'Business'),
        ('personal', 'Personal'),
    )

    DESIGN_TYPE_CHOICES = (
        ('logo', 'Logo Design'),
        ('branding', 'Brand Identity'),
        ('social', 'Social Media Design'),
        ('uiux', 'UI/UX Design'),
        ('marketing', 'Marketing Materials'),
        ('other', 'Other'),
    )

    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    design_type = models.CharField(max_length=50, choices=DESIGN_TYPE_CHOICES)

    # Basic Contact Info
    company_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, validators=[name_validator])
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True, validators=[phone_validator])

    short_description = models.TextField(blank=True, null=True)

    proposed_offer = models.CharField(max_length=100)
    expected_duration = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.design_type} - {self.full_name}"



from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('graphic', 'Graphic Design'),
        ('development', 'Web Development'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    demo_link = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # placeholder or uploaded image

    def __str__(self):
        return self.title


# class PurchaseRequest(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     email = models.EmailField()
#     whatsapp = models.CharField(max_length=20)
#     requested_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.title} - {self.email}"
class PurchaseRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=20, validators=[phone_validator])
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} - {self.email}"