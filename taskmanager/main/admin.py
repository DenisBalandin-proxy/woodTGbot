from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_mptt_admin.admin import DjangoMpttAdmin
#from mptt.admin import TreeRelatedFieldListFilter
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
#from django_admin_listfilter_dropdown.filters import (
#    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
#)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('user_fio', 'phone', 'sex', 'pin_code', 'department_user')
        readonly_fields = ('sex', 'user_fio')

    def clean(self):
        cleaned_data = super().clean()

        user_from_db = User.objects.filter(user_fio=cleaned_data.get('user_fio')).first()
        print(cleaned_data.get('user_fio'))
        print(cleaned_data.get('pin_code'))


        if user_from_db:
            # print(current_user_date_of_birth)
            if user_from_db.dateOfBirth == cleaned_data.get('dateOfBirth') and not cleaned_data.get('pin_code'):
                raise ValidationError(u'Такой пользователь уже существует')
            else:
                if not cleaned_data.get('phone'):
                    raise ValidationError(u'Номер телефона не может быть пустым')
                else:
                    if not cleaned_data.get('phone').isdigit():
                        raise ValidationError(u'Введите номер в формате 89209209090')
                    else:
                        return cleaned_data
        else:
            if not cleaned_data.get('phone'):
                raise ValidationError(u'Номер телефона не может быть пустым')
            else:
                if not cleaned_data.get('phone').isdigit():
                    raise ValidationError(u'Введите номер в формате 89209209090')
                else:
                    if cleaned_data.get('pin_code'):
                        raise ValidationError(u'Поле "Код доступа к боту" не должно быть заполнено вручную')
                    else:
                        return cleaned_data

class PostAdmin(admin.ModelAdmin):
    form = UserForm
    model = User
    #prepopulated_fields = {"slug": ("user_fio", "department",)}
    list_display = ("user_fio", "department_user", "job", "show_head_of_department")
    readonly_fields = ('balance', 'wood_coins', 'access')
    list_filter = ["access", "department_user"]
    list_editable = ["department_user"]

    #list_filter = (
    #    # for ordinary fields
    #    ('department_user', RelatedDropdownFilter),
    #)




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
                    #"show_head_of_department",
                    "balance",
                    "wood_coins",
                    "pin_code",
                    "access",
                    "fired"
                )


    def account_actions(self, obj):
        print("WE SAVED USER")

    def show_head_of_department(self, obj):
        return mark_safe(obj.department_user.head)
    show_head_of_department.short_description = 'Руководитель'

admin.site.register(User, PostAdmin)


class SupervisorAdmin(admin.ModelAdmin):
    list_display = ("sup_fio",)

admin.site.register(Supervisor, SupervisorAdmin)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ("title", "head", "show_number_of_employees")
    prepopulated_fields = {"slug": ("title",)}

    def show_number_of_employees(self, obj):
        count = User.objects.filter(department_user=obj.pk)
        return len(count)

admin.site.register(Department, CategoryAdmin)


#TEST++++++++++++++++++++++++++++++++++++++++
class DocumentsInApplicationForPaymentInLine(admin.StackedInline):
    model = DocumentsInApplicationForPayment
    readonly_fields = ["preview"]
    extra = 0

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.document.image.url}" width="300" height="300" style="object-fit:contain">')


class ApplicationForPaymentAdmin(admin.ModelAdmin):
    inlines = [DocumentsInApplicationForPaymentInLine]
    readonly_fields = ["fio", "benefit", "sum", "created", "state"]
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