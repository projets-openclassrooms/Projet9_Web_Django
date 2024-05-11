from django.contrib import admin

from litereview.models import Review, Ticket, User, UserBlock, UserFollows


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "username",
        "id",
    ]


class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "time_created", "id"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ticket",
        "user",
        "rating",
        "headline",
        "body",
        "time_created",
    ]


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ["followed_user", "user", "id"]


class UserBlockAdmin(admin.ModelAdmin):
    list_display = ["blocked_user", "user", "id"]


admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(UserBlock, UserBlockAdmin)
# Register your models here.
