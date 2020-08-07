from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse


class ShoppingList(models.Model):
    list_name = models.CharField(max_length=50, null=False)
    date_created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shopping_lists', null = True, blank=True)
    owners = models.ManyToManyField(User)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Done")

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return '{}'.format(self.list_name)


class ShoppingItem(models.Model):
    name = models.CharField(max_length=50, null=False)
    count = models.IntegerField(null=True, blank = True)
    list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='shopping_items', blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ('-date_created',)


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='groups_by_user', null = True, blank=True)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return '{}'.format(self.name)


class AskForShare(models.Model):
    who_asked = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='who_asked', null = True, blank=True)
    whos_list = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='whos_list', null = True, blank=True)
    what_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='what_list', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.what_list)

    @classmethod
    def create(cls, who_asked,whos_list, what_list ):
        ask = cls(who_asked=who_asked,whos_list = whos_list,  what_list = what_list)
        return ask