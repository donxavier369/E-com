from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category'

class BrandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brand' 

class VariantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Variant'      
