from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class PostImagesInline(admin.TabularInline):
    model = PostImages
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110">') 
    
    get_image.short_description = "Изображение"

class PostNetAdminForm(forms.ModelForm):

    content = forms.CharField(label="Текст статьи", widget=CKEditorUploadingWidget())
    class Meta:
        model = PostNet
        fields = "__all__"

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserNet
        fields = ('age', 'description', 'telephone', 'email', 'gender',)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserNet
        fields = ('age', 'description', 'telephone', 'email', 'gender')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

@admin.register(UserNet)
class UserNetAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('age', 'description', 'telephone', 'email', 'gender', 'time_create',)
    list_display_links = ('email',)
    search_fields = ('email', )
    list_filter = ('gender',)
    # prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ()
    ordering = ('email',)

admin.site.unregister(Group)

@admin.register(PostNet)
class PostNetAdmin(admin.ModelAdmin):
    inlines = [PostImagesInline]
    form = PostNetAdminForm
    save_on_top = True
    save_as = True
    list_display = ('author', 'title', 'content', 'photo', 'time_create',)
    list_display_links = ('author', 'title')
    readonly_fields = ('get_image',)
    # search_fields = ('name', )
    list_filter = ('author',)
    # prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Заголовок', {
            'fields': (('title',),)
        }),
        ('Описание', {
            'fields': (('content', 'get_image'))
        }),
    )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="100" height="110">')
    get_image.short_description = "Фото"

@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'description')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">') 
    
    get_image.short_description = "Изображение"



    
    

admin.site.site_title = "Kondratyev Project"
admin.site.site_header = "Kondratyev Project"
