from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from random import randint
from .bot_init import bot


# Create your models here.

#####TEST++++++TEST++++++++TEST+++++++TEST+++++++++++
class Contact(models.Model):

    name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(max_length=50, blank=True, verbose_name='email')
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return "{} {}".format(self.name, self.phone)



class Files(models.Model):

    file = models.FileField(upload_to='contact', blank=True, null=True, verbose_name='Файл')
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.name

#####TEST++++++TEST++++++++TEST+++++++TEST+++++++++++





















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
    head = models.ForeignKey('Supervisor', blank=True, null=True, verbose_name='Руководитель', on_delete=models.SET_NULL)
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

    STATE = (
        ('PR', 'Ожидает выплаты'),
        ('PM', 'На оплату'),
        #('P', 'Оплачено')
    )

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    fio = models.CharField(max_length=100, blank=True, null=True, verbose_name='ФИО')
    benefit = models.CharField(max_length=100, blank=True, null=True, verbose_name='Льгота')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Сформирована')
    sum = models.IntegerField(null=True, verbose_name='Сумма выплаты')
    date_of_payment = models.DateField(null=True, editable=True, verbose_name='Дата выплаты')
    state = models.CharField(max_length=100, blank=True, null=True, choices=STATE, default='PR', verbose_name='Состояние')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Гибкие льготы (к выплате)'
        verbose_name_plural = 'Гибкие льготы (к выплате)'

    def __str__(self):
        return f"{self.fio}"



class ApplicationArchive(models.Model):
    STATE = (
        #('AP', 'Одобрено'),
        ('RJ', 'Отклонено'),
        #('PR', 'На рассмотрении'),
        #('PM', 'На оплату'),
        ('P', 'Оплачено')
    )

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Перемещение')
    fio = models.CharField(max_length=100, blank=True, null=True, verbose_name='ФИО')
    benefit = models.CharField(max_length=100, blank=True, null=True, verbose_name='Льгота')
    state = models.CharField(max_length=100, blank=True, null=True, choices=STATE, verbose_name='Состояние')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Комментарий')
    sum = models.IntegerField(null=True, verbose_name='Сумма выплаты')

    class Meta:
        verbose_name = 'Архив гибких льгот'
        verbose_name_plural = 'Архив гибких льгот'

    def __str__(self):
        return f"{self.fio}"

class ActiveApplication(models.Model):
    STATE = (
        ('AP', 'Одобрено'),
        ('RJ', 'Отклонено'),
        ('PR', 'На рассмотрении'),
        #('PM', 'На оплату'),
        #('P', 'Оплачено')
    )

    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Сформирована')
    fio = models.CharField(max_length=100, blank=True, null=True, verbose_name='ФИО')
    benefit = models.CharField(max_length=100, blank=True, null=True, verbose_name='Льгота')
    sum = models.IntegerField(null=True, verbose_name='Сумма выплаты')
    state = models.CharField(max_length=100, blank=True, null=True, choices=STATE, default="PR", verbose_name='Состояние')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Укажите причину при отклонении заявления')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Гибкие льготы (активные)'
        verbose_name_plural = 'Гибкие льготы (активные)'

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
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    #count = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Пакет документов'

    def total(self):
        #return self.item.document
        return self.document.image

    def __str__(self):
        return self.document.document


class DocumentsInApplicationForPayment(models.Model):
    application_payment = models.ForeignKey(ApplicationForPayment, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, editable=False)

    class Meta:
        verbose_name = 'Пакет документов'

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



#SICK_LEAVE MODELS

class SickLeave(models.Model):
    chat_id = models.IntegerField(blank=True, null=True, editable=False)
    fio = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, editable=True, verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, editable=True, verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Больничный (активные)'
        verbose_name_plural = 'Больничный (активные)'

    def __str__(self):
        return f"{self.fio}"



class BenefitSession(models.Model):
    session_id = models.UUIDField()





#MODEL FOR APPLICATIONS ROLE

class ApplicationRoleNotification(models.Model):

    ROLES = (
        ("CA", "Касса"),
        ("G", "Утверждает документ")
    )

    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Заголовок')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    role = models.CharField(max_length=100, blank=True, null=True, choices=ROLES, verbose_name='Роль')
    person = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Получатель уведомления')

    class Meta:
        verbose_name = 'Оповещения'
        verbose_name_plural = 'Оповещения'

    def __str__(self):
        return f"{self.title}"





#SIGNALS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#SIGNAL FOR USER APPROVING/REFUSING++++++++++++++++++++
@receiver(post_save, sender=User)
def save_user_signal(sender, instance, **kwargs):
    print("SAVE SIGNAL")
    if not instance.pin_code:
        instance.wood_coins = 0
        code = randint(1000, 9999)
        instance.pin_code = code
        instance.save() #COME UP SOMETHING BETTER

    supervisor = Supervisor.objects.filter(sup_id=instance.pk).first()

    if instance.is_supervisor and supervisor:
        pass
    elif instance.is_supervisor and not supervisor:
        Supervisor.objects.create(
            sup_id=instance.pk,
            sup_fio=instance.user_fio,
            #department_sup=instance.department_user
        )
    elif not instance.is_supervisor and supervisor:
        supervisor.delete()
    elif not instance.is_supervisor and not supervisor:
        pass

    #from .helper import user_saved_signal_approved, user_saved_signal_refused
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

    if instance.state == "PR": #NOTIFY USER
        buhi = ApplicationRoleNotification.objects.filter(role='G').all()

        users = []
        for buh in buhi:
            if buh.person_id:
                user = User.objects.filter(id=buh.person_id).first()
                users.append(user)

        if not users:
            return

        for user in users:
            text = f"Новая заявка на льготы.\nФИО: {instance.fio}\nЛьгота: {instance.benefit}\nСумма: {instance.sum}"
            bot.send_message(user.chat_id, text)


    if instance.state == "RJ":
        print("NOTIFY USER")
        user = User.objects.filter(chat_id=instance.chat_id).first()

        app = ApplicationArchive.objects.create(
            chat_id=instance.chat_id,
            created=instance.created,
            fio=instance.fio,
            benefit=instance.benefit,
            state=instance.state,
            sum=instance.sum
        )

        documents = DocumentsInApplication.objects.filter(application_id=instance.pk).all()

        for document in documents:
            DocumentsInApplicationArchive.objects.create(application_archive_id=app.pk, document_id=document.document_id)


        user.balance = instance.sum + user.balance
        user.save()

        text = f"Заявка отклонена.\nФИО: {instance.fio}\nЛьгота: {instance.benefit}\nСумма: {instance.sum}\nПричина: {instance.description}"
        bot.send_message(user.chat_id, text)

        instance.delete()


    if instance.state == "AP":
        print("NOTIFY BUH KASSIR")
        app = ApplicationForPayment.objects.create(
            chat_id=instance.chat_id,
            created=instance.created,
            fio=instance.fio,
            benefit=instance.benefit,
            state='PR',
            sum=instance.sum
        )

        documents = DocumentsInApplication.objects.filter(application_id=instance.pk).all()

        for document in documents:
            DocumentsInApplicationForPayment.objects.create(application_payment_id=app.pk, document_id=document.document_id)

        buhi = ApplicationRoleNotification.objects.filter(role='CA').all()

        users = []
        for buh in buhi:
            if buh.person_id:
                user = User.objects.filter(id=buh.person_id).first()
                users.append(user)\

        if not users:
            instance.delete()
            return

        for user in users:
            text = f"Новая заявка к выплате.\nФИО: {instance.fio}\nЛьгота: {instance.benefit}\nСумма: {instance.sum}"
            bot.send_message(user.chat_id, text)

        instance.delete()


    if instance.state == "P":
        app = ApplicationArchive.objects.create(
            chat_id=instance.chat_id,
            created=instance.created,
            fio=instance.fio,
            benefit=instance.benefit,
            state=instance.state,
            description=instance.description,
            sum=instance.sum
        )

        documents = DocumentsInApplication.objects.filter(application_id=instance.pk).all()

        for document in documents:
            DocumentsInApplicationArchive.objects.create(application_archive_id=app.pk, document_id=document.pk)

        instance.delete()

@receiver(post_save, sender=ApplicationForPayment)
def save_application_for_payment_signal(sender, instance, **kwargs):
    if instance.date_of_payment and instance.state == 'PR':

        user = User.objects.filter(chat_id=instance.chat_id).first()

        #text = f"Заявка к выплате.\nФИО: {instance.fio}\nЛьгота: {instance.benefit}\nСумма: {instance.sum}\nДата выплаты:{instance.date_of_payment}"
        #bot.send_message(user.chat_id, text)

        instance.state = 'PM'
        instance.save()
    elif instance.date_of_payment and instance.state == 'PM':
        from .tasks import benefit_status_schedule
        benefit_status_schedule(instance.date_of_payment, instance.pk)

        user = User.objects.filter(chat_id=instance.chat_id).first()

        text = f"Заявка к выплате.\nФИО: {instance.fio}\nЛьгота: {instance.benefit}\nСумма: {instance.sum}\nДата выплаты:{instance.date_of_payment}"
        bot.send_message(user.chat_id, text)

    #if instance.state == "AP":
      #  instan
        #app = ApplicationForPayment.objects.create(
        #    chat_id=instance.chat_id,
        #    fio=instance.fio,
        #    benefit=instance.benefit,
        #   sum=instance.sum
        #)

       # app_arch = ApplicationArchive.objects.create(
        #    chat_id=instance.chat_id,
       #     created=datetime.today(),
     #       fio=instance.fio,
    #        benefit=instance.benefit,
     #       sum=instance.sum
      #  )

      #  documents = DocumentsInApplication.objects.filter(application_id=instance.pk).all()

    #    for document in documents:
    #        DocumentsInApplicationArchive.objects.create(application_archive_id=app_arch.pk, document_id=document.document_id)

     #   instance.delete()

   # elif instance.state == "RJ":
    #    ApplicationArchive.objects.create(
    #        chat_id=instance.chat_id,
    #        created=instance.created,
     #       fio=instance.fio,
    #        benefit=instance.benefit,
    #        sum=instance.sum
    #    )

     #   user = User.objects.filter(chat_id=instance.chat_id).first()

   #     current_balance = user.balance
   #     user.balance = current_balance + instance.sum
   #     user.save()

    #    instance.delete()

    #elif instance.state == "PR":
    #    return
    #elif instance.sum:
    #    return

