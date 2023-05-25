from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from random import randint

# Create your models here.
#DEPARTMENT MODEL

class User(models.Model):
    SEXES = (
        ('M', 'М'),
        ('F', 'Ж'),
    )

    ACCESS = (
        ('A', 'Подтверждено'),
        ('P', 'На рассмотрении')
    )

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    user_fio = models.CharField(max_length=100, verbose_name='ФИО', blank=False)
    phone = models.CharField(max_length=50, verbose_name='Телефон', null=True)
    pin_code = models.IntegerField(verbose_name='Код доступа к боту', null=True)
    sex = models.CharField(max_length=1, choices=SEXES, blank=True, verbose_name='Пол')
    dateOfBirth = models.DateField(blank=True, null=True, editable=True, verbose_name='Дата рождения')
    department_user = TreeForeignKey('Department', null=True, on_delete=models.PROTECT, related_name='users', verbose_name='Отдел')
    is_supervisor = models.BooleanField(default=False, verbose_name='Руководитель')
    supervisors = models.ForeignKey('Supervisor', blank=True, null=True, verbose_name='Руководитель', on_delete=models.SET_NULL)
    job = models.CharField(max_length=100, verbose_name='Должность', blank=True)
    dateOfHiring = models.DateField(null=True, editable=True, verbose_name='Дата приёма на работу')
    balance = models.IntegerField(blank=True, null=True, editable=False, verbose_name='Баланс')
    wood_coins = models.IntegerField(blank=True, null=True, editable=False, verbose_name='WoodCoins')
    #benefits = models.BooleanField(default=False, verbose_name='Гибкие льготы')
    staff_type = models.CharField(max_length=5, blank=True, null=True, editable=False)
    access = models.CharField(max_length=1, choices=ACCESS, default='P', null=True, verbose_name='Доступ')
    fired = models.BooleanField(default=False, verbose_name='Уволен')


    def __str__(self):
        return self.user_fio

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    @classmethod
    def get(cls, param):
        pass


#class DayOff(models.Model):
#    day = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
#    name = models.CharField(max_length=30)
#    price = models.IntegerField()


#    def __str__(self):
#        return self.name

class BenefitImages(models.Model):
    fio = models.CharField(max_length=100, verbose_name='ФИО', blank=False)
    benefit = models.CharField(max_length=100)
    image = models.ImageField(blank=False, null=False, upload_to=None)
    #user = models.ForeignKey(User, related_name='ben_img', on_delete=models.CASCADE)

    def __str__(self):
        return self.benefit


class Supervisor(models.Model):
    sup_id = models.IntegerField(null=True, editable=False)
    sup_fio = models.CharField(max_length=100, verbose_name='ФИО', blank=False)
    #department_sup = TreeForeignKey('Department', on_delete=models.PROTECT, related_name='supervisor', verbose_name='Отдел', blank=True, null=True)

    def __str__(self):
        return self.sup_fio

    class Meta:
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководители'


class TempUser(models.Model):
    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    user_fio = models.CharField(max_length=100, verbose_name='ФИО', blank=False)
    access = models.CharField(max_length=1, null=True, verbose_name='Доступ')

    def __str__(self):
        return self.user_fio

    class Meta:
        verbose_name = 'Неподтверждённые пользователи'
        verbose_name_plural = 'Неподтверждённые пользователи'



class Department(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    #supervisor_dep = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Подотдел')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отдел'

    def get_absolute_url(self):
        return reverse('user-by-department', args=[str(self.slug)])

    def __str__(self):
        return self.title




#TEST+++++++++++++++++++++++++++++

#DOCUMENT - ITEM
class Document(models.Model):
    document = models.CharField(max_length=100, blank=True, null=True, editable=False)
    image = models.ImageField(blank=False, null=False)

    class Meta:
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.document

#APPLICATION - CART

class ApplicationForPayment(models.Model):

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    fio = models.CharField(max_length=100, blank=True, null=True)
    benefit = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    sum = models.IntegerField(null=True)
    state = models.CharField(max_length=100, blank=True, null=True, default='Ожидает выплаты')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заявления к выплате'
        verbose_name_plural = 'Заявления к выплате'

    def __str__(self):
        return f"{self.fio}"



class ApplicationArchive(models.Model):
    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    fio = models.CharField(max_length=100, blank=True, null=True)
    benefit = models.CharField(max_length=100, blank=True, null=True)
    sum = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Архив заявлений'
        verbose_name_plural = 'Архив заявлений'

    def __str__(self):
        return f"{self.fio}"

class ActiveApplication(models.Model):
    STATE = (
        ('AP', 'Одобрить'),
        ('RJ', 'Отклонить'),
        ('PR', 'На рассмотрении')
    )

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    fio = models.CharField(max_length=100, blank=True, null=True)
    benefit = models.CharField(max_length=100, blank=True, null=True)
    sum = models.IntegerField(null=True)
    state = models.CharField(max_length=100, blank=True, null=True, choices=STATE, default="PR")
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Активные заявления'
        verbose_name_plural = 'Активные заявления'

    def total_price(self):
        return sum([
            cart_item.total()
            for cart_item in DocumentsInApplication.objects.filter(cart=self)
        ])

    def __str__(self):
        return f"{self.fio}"


#CONNECT APPLICATION AND DOCUMENT
class DocumentsInApplication(models.Model):
    application = models.ForeignKey(ActiveApplication, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, editable=False)
    #count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Пакет документов'

    def total(self):
        #return self.item.document
        return self.document.image

    def __str__(self):
        return self.document.document


class DocumentsInApplicationArchive(models.Model):
    application_archive = models.ForeignKey(ApplicationArchive, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, editable=False)
    #count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Пакет документов'

    def total(self):
        #return self.item.document
        return self.document.image

    def __str__(self):
        return self.document.document


class PaidApplication(models.Model):
    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    fio = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    benefit = models.CharField(max_length=100, blank=True, null=True)
    sum = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Выплаченные заявления'
        verbose_name_plural = 'Выплаченные заявления'


    def __str__(self):
        return f"{self.fio}"

#SIGNALS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#SIGNAL FOR USER APPROVING/REFUSING++++++++++++++++++++
@receiver(post_save, sender=User)
def save_user_signal(sender, instance, **kwargs):
    print("SAVE SIGNAL")
    if not instance.pin_code:
        code = randint(1000, 9999)
        instance.pin_code = code

    supervisor = Supervisor.objects.filter(sup_id=instance.pk).first()

    if instance.is_supervisor and supervisor:
        return
    elif instance.is_supervisor and not supervisor:
        Supervisor.objects.create(
            sup_id=instance.pk,
            sup_fio=instance.user_fio,
            #department_sup=instance.department_user
        )
    elif not instance.is_supervisor and supervisor:
        supervisor.delete()
    elif not instance.is_supervisor and not supervisor:
        return
    instance.update()

    from .helper import user_saved_signal_approved, user_saved_signal_refused
    #temp_user = TempUser.objects.filter(chat_id=instance.chat_id)
    #print("FFFFFFFFFFFF")
    #instance.
    #if instance.access and instance.access == "A" and not instance.balance:
    #    user_saved_signal_approved(instance.chat_id)
        #calculate_work_experience(instance.chat_id)


@receiver(post_save, sender=ActiveApplication)
def save_active_application_signal(sender, instance, **kwargs):
    if not instance.sum:
        return

    if instance.state == "PR":
        return

    if instance.state == "AP":
        app = ApplicationForPayment.objects.create(
            chat_id=instance.chat_id,
            fio=instance.fio,
            benefit=instance.benefit,
            sum=instance.sum
        )

        app_arch = ApplicationArchive.objects.create(
            chat_id=instance.chat_id,
            created=datetime.today(),
            fio=instance.fio,
            benefit=instance.benefit,
            sum=instance.sum
        )

        documents = DocumentsInApplication.objects.filter(application_id=instance.pk).all()

        for document in documents:
            DocumentsInApplicationArchive.objects.create(application_archive_id=app_arch.pk, document_id=document.document_id)

        instance.delete()

    elif instance.state == "RJ":
        ApplicationArchive.objects.create(
            chat_id=instance.chat_id,
            created=instance.created,
            fio=instance.fio,
            benefit=instance.benefit,
            sum=instance.sum
        )

        user = User.objects.filter(chat_id=instance.chat_id).first()

        current_balance = user.balance
        user.balance = current_balance + instance.sum
        user.save()

        instance.delete()

    elif instance.state == "PR":
        return
    elif instance.sum:
        return

@receiver(post_save, sender=ApplicationForPayment)
def save_app_for_payment_in_archive(sender, instance, **kwargs):
    if instance.status:
        PaidApplication.objects.create(
            chat_id=instance.chat_id,
            created=datetime.today(),
            fio=instance.fio,
            benefit=instance.benefit,
            sum=instance.sum
        )
        instance.delete()

