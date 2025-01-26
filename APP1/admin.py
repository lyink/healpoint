from django.contrib import admin
from . import models

class DepartmentAdmin(admin.ModelAdmin):
    #list_editable = ()
    list_per_page = 5
    list_max_show_all = 5
    list_display=('department_name',)
admin.site.register(models.Department,DepartmentAdmin)


class ProgramsAdmin(admin.ModelAdmin):
      #list_editable = ()
    list_per_page = 5
    list_max_show_all = 5
    list_display=('program_name','program_duration','program_fee','date_registered','department',)
admin.site.register(models.Programs,ProgramsAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_editable = ('program',)
    list_per_page = 5
    list_max_show_all = 5
    list_display=('course_name','program',)
admin.site.register(models.Course,CourseAdmin)




from django.contrib import admin
from .models import Doctors  # Import the Doctors model

class DoctorsAdmin(admin.ModelAdmin):
    # Fields that can be edited directly from the list view
    list_editable = ('specialization', 'contact_number', 'email')

    # Number of items to display per page in the admin list view
    list_per_page = 10

    # Maximum number of items to display in the "Show all" view
    list_max_show_all = 100

    # Fields to display in the admin list view
    list_display = (
        'first_name',
        'last_name',
        'specialization',
        'date_joined',
        'contact_number',
        'email',
    )

    # Add search functionality for specific fields
    search_fields = ('first_name', 'last_name', 'specialization', 'email')

    # Add filters for specific fields
    list_filter = ('specialization', 'date_joined')

    # Enable date hierarchy for the 'date_joined' field
    date_hierarchy = 'date_joined'

# Register the Doctors model with the custom admin class
admin.site.register(Doctors, DoctorsAdmin)

class HerroesAdmin(admin.ModelAdmin):
    list_per_page = 8
    list_max_show_all = 8
    list_display=('full_name','heading','title','image_tag','date_registered','program',)
admin.site.register(models.Herroes,HerroesAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_editable = ('program',)
    list_per_page = 8
    list_max_show_all = 8
    list_display=('full_name','regno','image_tag','date_registered','program',)
admin.site.register(models.Student,StudentAdmin)

 
from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    # Fields that can be edited directly from the list view
    list_editable = ('title', 'author', 'publication_date')

    # Number of items to display per page in the admin list view
    list_per_page = 10

    # Maximum number of items to display in the "Show all" view
    list_max_show_all = 100

    # Fields to display in the admin list view
    list_display = (
        'id',  # Add this line to include the primary key
        'title',
        'author',
        'publication_date',
        'display_categories',  # Custom method to display categories
        'display_tags',        # Custom method to display tags
    )

    # Set 'list_display_links' to a field not in 'list_editable'
    list_display_links = ('id',)  # Link to the change form using the 'id' field

    # Add search functionality for specific fields
    search_fields = ('title', 'content', 'author__username', 'categories__name', 'tags__name')

    # Add filters for specific fields
    list_filter = ('author', 'publication_date', 'categories', 'tags')

    # Enable date hierarchy for the 'publication_date' field
    date_hierarchy = 'publication_date'

    # Custom method to display categories in the list view
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'

    # Custom method to display tags in the list view
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'

# Register the Post model with the custom admin class
admin.site.register(Post, PostAdmin)

# Optionally, register Category and Tag models with default admin settings
admin.site.register(Category)
admin.site.register(Tag)