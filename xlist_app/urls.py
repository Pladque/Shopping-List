from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    #BASIC STAFF#
    path('', views.home, name='home'),
    path('profile/', views.Profile, name='profile'),
    path('mobilenav/', views.mobilenav, name='mobilenav'),

    #LIST STAFF#
    path('myLists/', views.MyLists, name='mylists'),
    path('list/search/', views.ListSearch, name='list/search/'),
    path('shareList/<int:pk>', views.shareList, name="shareList"),
    path('deleteItem/<int:pk>', views.deleteItem, name = "delete"),
    path('deleteList/<int:pk>', views.deleteList, name="deleteList"),
    path('NewList/', views.NewListCrateView.as_view(), name='newlistcrateView'),
    path('deleteNOTMYList/<int:pk>', views.deleteNOTMYList, name="deleteNOTMYList"),
    path('ListDetails/<int:pk>/', views.ListDetailUpdateView.as_view(), name='listdetailupdate'),

    #GROUP STAFF#
    path('deleteGroup/<int:pk>', views.deleteGroup, name="deleteGroup"),
    path('NewGroup/', views.NewGroupCrateView.as_view(), name='newgroupcrateView'),
    path('deleteNOTMYGroup/<int:pk>', views.deleteNOTMYGroup, name="deleteNOTMYGroup"),
    path('GroupDetails/<int:pk>/', views.GroupDetailUpdateView, name='groupdetailupdate'),
    path('deleteUserFromGroup/<int:pk>', views.deleteUserFromGroup, name="deleteUserFromGroup"),

    #ASK STAFF#
    path('asks/', views.asks, name = "asks"),
    path('asking/<int:pk>', views.asking, name = "asking"),
    path('agreeAsk/<int:pk>', views.agreeAsk, name = "agreeAsk"),
    path('deleteAsk/<int:pk>', views.deleteAsk, name = "deleteAsk"),
    ]

