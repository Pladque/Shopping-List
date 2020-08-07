from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ShoppingList)
admin.site.register(ShoppingItem)
admin.site.register(AskForShare)
admin.site.register(Group)


