from django.contrib import admin
from .models import User, Ticket, Review, UserFollows


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'user', 'time_created']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'user', 'rating', 'headline', 'body', 'time_created']


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ['followed_user', 'user']


admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)

# Register your models here.
