from django.contrib import admin, messages
from .models import Freelancer, Issue, Bill
from django.utils.html import format_html
from . import actions
# Register your models here.

def sync_issues(modeladmin, request, queryset):
    freelancers = queryset.all()
    for freelancer in freelancers:
        try:
            actions.sync_user_issues(freelancer)
        except ValueError as err:
            messages.error(request,err)

sync_issues.short_description = "Sync open issues"

def generate_bill(modeladmin, request, queryset):
    freelancers = queryset.all()
    for freelancer in freelancers:
        try:
            print(f"Genereting bill for {freelancer.user.email}")
            actions.generate_freelancer_bill(freelancer)
        except ValueError as err:
            messages.error(request,err)
generate_bill.short_description = "Generate bill"

def mask_as_done(modeladmin, request, queryset):
    issues = queryset.update(status='DONE')
mask_as_done.short_description = "Mark as DONE"

def mask_as_ignored(modeladmin, request, queryset):
    issues = queryset.update(status='IGNORED')
mask_as_ignored.short_description = "Mark as IGNORED"

def mask_as_paid(modeladmin, request, queryset):
    issues = queryset.update(status='PAID')
mask_as_paid.short_description = "Mark as PAID"

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', "email"]
    actions = [sync_issues, generate_bill]
    def full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    def email(self, obj):
        return obj.user.email


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('id', 'github_number', 'title', 'status', 'duration_in_hours', 'bill_id', 'github_url')
    list_filter = ['status', 'bill__status']
    actions = [mask_as_done, mask_as_ignored]
    def github_url(self,obj):
        return format_html("<a rel='noopener noreferrer' target='_blank' href='{url}'>open in github</a>", url=obj.url)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer','status', 'total_duration_in_hours', 'total_price','paid_at')
    list_filter = ['status']
    actions = [mask_as_paid]
