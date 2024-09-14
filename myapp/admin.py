from django.contrib import admin
from .models import *

# @admin.register(likeeinvoicemodel)
# class LikeeInvoiceAdmin(admin.ModelAdmin):
#     list_display = ('invoice_id', 'username', 'diamonds', 'price', 'timestamp')
#     search_fields = ('invoice_id', 'username')

# @admin.register(tiktokinvoicemodel)
# class TiktokInvoiceAdmin(admin.ModelAdmin):
#     list_display = ('invoice_id', 'username', 'coin', 'price', 'timestamp')
#     search_fields = ('invoice_id', 'username')

@admin.register(CoinOption)
class CoinOptionAdmin(admin.ModelAdmin):
    list_display = ('coins', 'price')
    list_filter = ('coins', 'price')
    search_fields = ('coins', 'price')

@admin.register(diamondsOption)
class diamondsOptionAdmin(admin.ModelAdmin):
    list_display = ('diamonds', 'price')
    list_filter = ('diamonds', 'price')
    search_fields = ('diamonds', 'price')

class TikTokProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_name', 'username', 'status', 'comments', 'issue')
    list_filter = ('status', 'comments', 'issue')
    search_fields = ('profile_name', 'username', 'unique_id', 'invoice_id')
    readonly_fields = ('invoice_id',)

admin.site.register(TikTokProfiledata, TikTokProfileAdmin)

class LikeeProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_name', 'username', 'status', 'comments', 'issue')
    list_filter = ('status', 'comments', 'issue')
    search_fields = ('profile_name', 'username', 'invoice_id')
    readonly_fields = ('invoice_id',)

admin.site.register(LikeeProfiledata, LikeeProfileAdmin)



# Register the Status model
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name fields
    search_fields = ('name',)      # Add search functionality based on name

# Register the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')  # Display ID and text fields
    search_fields = ('text',)      # Add search functionality based on text

# Register the Issue model
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name fields
    search_fields = ('name',)      # Add search functionality based on name
