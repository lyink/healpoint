from django.urls import path
from . import views

urlpatterns=[ 
    path('',views.home,name='home'),
    path('about_us',views.about,name='about'),
    path('herroes',views.herroes,name='herroes'),
    path('doctors',views.doctors,name='doctors'),
    path('online_application',views.application,name='application'),
    path('courses',views.courses,name='courses'),


    path('post_list', views.post_list, name='post_list'),

    # Individual blog post detail page
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # List of posts by category
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),

        path('contact-us/', views.contact_us, name='contact_us'),

    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),

    # List of posts by tag
    path('tag/<int:tag_id>/', views.tag_posts, name='tag_posts')
]