from django.contrib import admin
from django.contrib.auth.admin import Group, UserAdmin
from users.forms import CustomUserCreationForm, PasswordChangeForm
from users.models import Subscription, User

from .models import (CountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)


class UserAdmin(UserAdmin):
    form = PasswordChangeForm
    add_form = CustomUserCreationForm
    list_filter = ('email', 'username')
    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )}),
        ('Permissions', {'fields': ('role',)})
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2'
            )
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('id', 'email', 'username',)
    empty_value_display = '-none-'


class RecipesAdmin(admin.ModelAdmin):
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)
    empty_value_display = '-none-'

    def added_in_favorites(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    empty_value_display = '-none-'


class TagsAdmin(admin.ModelAdmin):
    empty_value_display = '-none-'


class SubscriptionAdmin(admin.ModelAdmin):
    empty_value_display = '-none-'


class FavoriteAdmin(admin.ModelAdmin):
    empty_value_display = '-none-'


class CountIngredientAdmin(admin.ModelAdmin):
    empty_value_display = '-none-'


@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    empty_value_display = '-none-'


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CountIngredient, CountIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)

admin.site.unregister(Group)
