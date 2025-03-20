from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import (
    user_management, 
    user_details, 
    toggle_user_status,
    delete_user
)

urlpatterns=[ 
    path('',views.home,name='home'),
    path('about_us',views.about,name='about'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register_user/', views.RegisterView.as_view(), name='register_user'),
    path("create-user/", views.create_user, name="create_user"),
    path('team/add/', views.add_team_member, name='add_team_member'),
    path('team/', views.team_list, name='team_list'),
    path('team/edit/<int:member_id>/', views.edit_team_member, name='edit_team_member'),
    path('team/delete/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('team/delete/<int:member_id>/', views.delete_team_member_confirm, name='delete_team_member'),
    path('team/delete/<int:member_id>/', views.delete_team_member, name='delete_team_member'),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),


     path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Properties URLs
    path('properties/my/', views.my_properties_view, name='my_properties'),
    path('properties/browse/', views.browse_properties_view, name='browse_properties'),
    path('properties/favorites/', views.favorites_view, name='favorites'),
    
    # Appointments URLs
    path('appointments/', views.appointments_view, name='appointments'),
    
    # Payments URLs
    path('payments/', views.payments_view, name='payments'),

     path('settings/', views.settings_view, name='settings'),
        path('logout/', views.logout_view, name='logout'),

    # Help & Support URLs
    path('support/', views.support_view, name='support'),

        path('manage/', user_management, name='user_management'),

    # View specific user details
    path('manage/user/<int:user_id>/', user_details, name='user_details'),
    
     path('users/<int:user_id>/', views.user_details, name='user_details'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/update-profile-pic/', views.update_profile_pic, name='update_profile_pic'),
 path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locations/new/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/edit/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),
    path('property-types/', views.PropertyTypeListView.as_view(), name='property_type_list'),
    path('property-types/<int:pk>/', views.PropertyTypeDetailView.as_view(), name='property_type_detail'),
    path('property-types/create/', views.PropertyTypeCreateView.as_view(), name='property_type_create'),
    path('property-types/<int:pk>/update/', views.PropertyTypeUpdateView.as_view(), name='property_type_update'),
    path('property-types/<int:pk>/delete/', views.PropertyTypeDeleteView.as_view(), name='property_type_delete'),
     path('property_detail_home/<int:property_id>/', views.property_detail_home, name='property_detail_home'),
    path('properties/<int:property_id>/inquiry/', views.property_inquiry, name='property_inquiry'),
    # Rental Property URLs
    path('properties/', views.RentalPropertyListView.as_view(), name='rental_property_list'),
    path('properties/<int:pk>/', views.RentalPropertyDetailView.as_view(), name='rental_property_detail'),
    path('properties/create/', views.RentalPropertyCreateView.as_view(), name='rental_property_create'),
    path('properties/<int:pk>/update/', views.RentalPropertyUpdateView.as_view(), name='rental_property_update'),
    path('properties/<int:pk>/delete/', views.RentalPropertyDeleteView.as_view(), name='rental_property_delete'),
    
    # Property Image URLs
    path('properties/<int:property_pk>/images/add/', views.PropertyImageCreateView.as_view(), name='property_image_create'),
    path('images/<int:pk>/update/', views.PropertyImageUpdateView.as_view(), name='property_image_update'),
    path('images/<int:pk>/delete/', views.PropertyImageDeleteView.as_view(), name='property_image_delete'),
    path('images/<int:pk>/set-primary/', views.set_primary_image, name='property_image_set_primary'),
    path('properties/<int:property_pk>/images/reorder/', views.reorder_images, name='property_image_reorder'),
    # API endpoints for dependent dropdowns
    # AJAX URLs for dependent dropdowns
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-wards/', views.load_wards, name='ajax_load_wards'),

    # Toggle user account status (activate/deactivate)
    path('manage/user/<int:user_id>/toggle-status/', 
         toggle_user_status, 
         name='toggle_user_status'),
    
    # Delete user account
    path('manage/user/<int:user_id>/delete/', 
         delete_user, 
         name='delete_user'),
    path('property/<int:property_id>/contact/', views.contact_owner, name='contact_owner'),


path('properties_list/', views.PropertyListView.as_view(), name='property_list'),
    path('properties_list2/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('property_table_list/', views.PropertyTableListView.as_view(), name='property_table_list'),
path('properties_list_home/', views.PropertyListhomeView.as_view(), name='property_list_home'),

path('properties_list_out/', views.PropertyListView_out.as_view(), name='properties_list_out'),


]
