from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import  ShoppingList, ShoppingItem, Group, AskForShare
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def home(request):
    return render(request, 'base.html')

def mobilenav(request):
    return render(request, 'xlist_app/mobilenav.html')

@login_required
def Profile(request):
    nickname = request.user
    user_id = request.user.id
    groups = Group.objects.filter(owner=request.user)
    other_groups = Group.objects.filter(participants=request.user)
    return render(request, 'xlist_app/Profile.html', {'nickname': nickname,  'id': user_id,   'groups': groups, 'other_groups': other_groups})


#### LIST STAFF ################### LIST STAFF ################## LIST STAFF ############### LIST STAFF ############### LIST STAFF ####

@login_required
def MyLists(request):
    my_lists = ShoppingList.objects.filter(owner=request.user)
    other_lists = ShoppingList.objects.filter(owners=request.user)
    return render(request, 'xlist_app/MyLists.html',{'my_lists' : my_lists  ,  'other_lists' : other_lists })


@login_required
def ListSearch(request):
    search = request.POST.get('search')
    if search:
        lists = ShoppingList.objects.filter(list_name__iexact=search)
        lists_constains = ShoppingList.objects.filter(list_name__icontains=search)
        for lc in lists_constains:
            for l in lists:
                if l != lc:
                    lists.append(lc)
        
        if len(lists)==0:
            lists = lists_constains
        return render(request, 'xlist_app/ListSearch.html', {'lists': lists})
    return render(request, 'xlist_app/ListSearch.html', {})


def shareList(request, pk):
    share = request.POST.get('share', '/')
    # Searching in groups
    if str(share) and len(Group.objects.filter(owner=request.user).filter(name = share))!=0:
        people_to_add = Group.objects.filter(owner=request.user).get(name = share).participants.all()
        for p in people_to_add:
            ShoppingList.objects.get(id=pk).owners.add(User.objects.get(username=p))
        print("Udostepniono uzytkownikom z grupy")
    # Searching by ID
    elif share.isnumeric() and len(User.objects.filter(id=share)) != 0:
        ShoppingList.objects.get(id=pk).owners.add(User.objects.get(id=share))
        print("Udostepniono uzytkownikowi po ID")
    # Searching by nickname
    elif str(share) and len(User.objects.filter(username=share)) != 0:
        ShoppingList.objects.get(id=pk).owners.add(User.objects.get(username=share))
        print("Udostepniono uzytkownikowi po nazwie")
    # Not Found
    else: print("Nie udalo sie udostepnic")

    next = request.POST.get('back', '/')
    return HttpResponseRedirect(next)

#deletes:
def deleteNOTMYList(request, pk):
    ShoppingList.objects.get(id=pk).owners.remove(User.objects.get(id=request.user.id))
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)
def deleteList(request, pk):
    ShoppingList.objects.get(id=pk).delete()
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)

def deleteItem(request, pk):
    ShoppingItem.objects.get(id=pk).delete()
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)



#### GROUP STAFF ################ GROUP STAFF ################ GROUP STAFF ################ GROUP STAFF ################ GROUP STAFF ############



def GroupDetailUpdateView(request, pk):
    is_valid = False
    group_id = request.resolver_match.kwargs['pk']
    group = Group.objects.get(id=group_id)

    for own in group.participants.all():
        if own == request.user:
            is_valid = True
    if request.user == group.owner:
        is_valid = True

    if is_valid is True     and     request.POST.get('add'):
        if request.POST.get('add').isnumeric():
            to_add = User.objects.get(id=request.POST.get('add'))
        else:
            to_add = User.objects.get(username=request.POST.get('add'))
        group.participants.add(to_add)
        return render(request, 'xlist_app/AddPeopleToGroup.html', {'group': group, 'participants': group.participants.all()})
    elif is_valid is True:
        return render(request, 'xlist_app/AddPeopleToGroup.html', {'group': group, 'participants': group.participants.all()})
    return render(request, 'xlist_app/ListSearch.html')



def deleteGroup(request, pk):
    Group.objects.get(id=pk).delete()
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)


def deleteNOTMYGroup(request, pk):
    Group.objects.get(id=pk).participants.remove(User.objects.get(id=request.user.id))
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)


def deleteUserFromGroup(request, pk):
    get_only_num_bool = False
    group_id = ""
    #Getting only ID from link (pk) #
    for letter in reversed(request.POST.get('back')):
        if(letter.isnumeric()   and get_only_num_bool):
            group_id =letter    + group_id
        elif get_only_num_bool is True: break;
        else: get_only_num_bool = True

    Group.objects.get(id=group_id).participants.remove(User.objects.filter(id=pk)[0])
    next = request.POST.get('back', '/')

    return HttpResponseRedirect(next)


##########ASK STAFF###############ASK STAFF###################ASK STAFF##################ASK STAFF###########ASK STAFF########
def asks(request):
    asks = AskForShare.objects.filter(whos_list=request.user)
    return render(request, 'xlist_app/Asks_for_share.html', {'asks': asks})


def deleteAsk(request, pk):
    AskForShare.objects.get(id = pk).delete()
    next = request.POST.get('back', '/')
    return HttpResponseRedirect(next)


def agreeAsk(request, pk):
    user_to_add = AskForShare.objects.get(id=pk).who_asked
    #adding user to list#
    AskForShare.objects.get(id=pk).what_list.owners.add(user_to_add)
    #deleteing ask#
    AskForShare.objects.get(id=pk).delete()

    next = request.POST.get('back', '/')
    return HttpResponseRedirect(next)


@login_required
def asking(request, pk):
    whos_list = ShoppingList.objects.get(id=pk).owner
    list = ShoppingList.objects.get(id=pk)

    #creating new ask and saving it#
    new_ask = AskForShare.create(request.user,whos_list, list)
    new_ask.save()

    next = request.POST.get('back', '/')
    return HttpResponseRedirect(next)


#################CLASSES#################CLASSES#####################CLASSES######################CLASSES#######################
#To see staff inside list
class ListDetailUpdateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = ShoppingItem
    template_name = 'xlist_app/ListDetailUpdateView.html'
    context_object_name = 'products'
    fields = ['name', 'count']


    def form_valid(self, form):
        form.instance.list = ShoppingList.objects.get(id=self.request.resolver_match.kwargs['pk'])
        self.object = form.save()
        return super(ListDetailUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.model.objects.filter(list=self.request.resolver_match.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('listdetailupdate', kwargs = {'pk':self.request.resolver_match.kwargs['pk']})

    def test_func(self):
        shop_list_id= self.request.resolver_match.kwargs['pk']
        shop_list = ShoppingList.objects.get(id=shop_list_id)
        for own in shop_list.owners.all():
            if own == self.request.user:
                return True
        if self.request.user == shop_list.owner:
            return True
        return False


#To create new group
class NewGroupCrateView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'xlist_app/GroupDetailUpdateView.html'
    context_object_name = 'participants'
    fields = ['name']
    new_list_id = -1


    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return super(NewGroupCrateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('groupdetailupdate', kwargs = {'pk':self.object.id})


#To create new list
class NewListCrateView(LoginRequiredMixin, CreateView):
    model = ShoppingList
    template_name = 'xlist_app/ListDetailUpdateView.html'
    context_object_name = 'products'
    fields = ['list_name']
    new_list_id = -1


    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return super(NewListCrateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('listdetailupdate', kwargs = {'pk':self.object.id})
