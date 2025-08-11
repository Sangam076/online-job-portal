from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class Contact(models.Model):
    Email = models.EmailField()
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
    
JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Job(models.Model):

    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=300)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category,related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    Vacancy = models.CharField(max_length=10, null=True)
    Experience = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=30)
    passedout = models.CharField(max_length=30)
    

    def __str__(self):
        return self.title
    
    @property
    def acceptance_rate(self):
        total = self.applicant_set.count()
        accepted = self.applicant_set.filter(status='accepted').count()
        if total == 0:
            return 0
        return round((accepted / total) * 100, 2)

 

# models.py

class Applicant(models.Model):
    STATUS_CHOICES = [
        
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job.title} ({self.status})"



  

class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.job.title
    
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double XL'),
    ]
    
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('pink', 'Pink'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('brown', 'Brown'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    sizes = models.CharField(max_length=20, choices=SIZE_CHOICES, default='M')
    colors = models.CharField(max_length=20, choices=COLOR_CHOICES, default='black')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    @property
    def get_price(self):
        return self.discounted_price if self.discounted_price else self.price
    
    @property
    def is_on_sale(self):
        return self.discounted_price is not None and self.discounted_price < self.price