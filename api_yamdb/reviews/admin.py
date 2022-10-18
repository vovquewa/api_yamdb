from django.contrib import admin

from .models import User, Review, Comment

admin.site.register(User)

# vovq: ожидает Title


class RewiewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'text', 'score',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Review, RewiewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'author', 'text', 'review')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
