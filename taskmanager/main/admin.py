from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import (
    User,
    Department,
    Supervisor,
    ApplicationForPayment,
    DocumentsInApplicationForPayment,
    Document,
    ActiveApplication,
    DocumentsInApplication,
    ApplicationArchive,
    DocumentsInApplicationArchive,
    ApplicationRoleNotification,
    SickLeave)
from django.template.loader import get_template
from django.utils.safestring import mark_safe


class PostAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"slug": ("user_fio", "department",)}
    list_display = ("user_fio", "department_user", "job")
    readonly_fields = ('balance', 'wood_coins', 'access', 'pin_code')
    list_filter = ["access", "department_user"]
    search_fields = ["user_fio"]
    fields = (
                    "user_fio",
                    "phone",
                    "sex",
                    "dateOfBirth",
                    "department_user",
                    "is_supervisor",
                    "job",
                    "dateOfHiring",
                    "supervisors",
                    "balance",
                    "wood_coins",
                    "pin_code",
                    "access",
                    "fired"
                )

    def account_actions(self, obj):
        print("WE SAVED USER")

admin.site.register(User, PostAdmin)


class SupervisorAdmin(admin.ModelAdmin):
    list_display = ("sup_fio",)

admin.site.register(Supervisor, SupervisorAdmin)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Department, CategoryAdmin)


#TEST++++++++++++++++++++++++++++++++++++++++
class DocumentsInApplicationForPaymentInLine(admin.StackedInline):
    model = DocumentsInApplicationForPayment
    readonly_fields = ["preview"]
    extra = 0

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.document.image.url}" width="300" height="300" style="object-fit:contain">')


class ApplicationForPaymentAdmin(admin.ModelAdmin):
    inlines  = [DocumentsInApplicationForPaymentInLine]
    readonly_fields = ["fio", "benefit", "sum", "created"]
    list_display = ["fio", "benefit", "sum", "state", "created"]

admin.site.register(ApplicationForPayment, ApplicationForPaymentAdmin)


class DocumentsInArchiveInLine(admin.StackedInline):
    model = DocumentsInApplicationArchive
    readonly_fields = ["preview"]
    extra = 0

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.document.image.url}" width="300" height="300" style="object-fit:contain">')


class ApplicationArchiveAdmin(admin.ModelAdmin):
    inlines = [DocumentsInArchiveInLine]
    readonly_fields = ["fio", "benefit", "sum", "state", "description", "created"]
    list_display = ["fio", "benefit", "sum", "state", "created"]

admin.site.register(ApplicationArchive, ApplicationArchiveAdmin)

class DocumentInline(admin.StackedInline):
    model = DocumentsInApplication
    readonly_fields = ['preview']
    extra = 0

    def urll(self, obj):
        return obj.document.image

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.document.image.url}" width="300" height="300" style="object-fit:contain">')

class ApplicationAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
    readonly_fields = ["fio", "benefit", "sum", "created",]
    list_filter = ["state"]
    list_display = ["fio", "benefit", "sum", "state", "created",]

admin.site.register(ActiveApplication, ApplicationAdmin)
admin.site.register(Document)


class SickLeaveActiveApplication(admin.ModelAdmin):
    list_display = ["fio", "department"]

admin.site.register(SickLeave, SickLeaveActiveApplication)


class ApplicationRoleNotificationAdmin(admin.ModelAdmin):
    list_display = ["title"]

admin.site.register(ApplicationRoleNotification, ApplicationRoleNotificationAdmin)