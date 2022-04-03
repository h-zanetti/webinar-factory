from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        user.is_active=True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # User information
    username = None
    email = models.EmailField('endereço de email', max_length=255, unique=True)
    first_name = models.CharField('nome', max_length=30)
    last_name = models.CharField('sobrenome', max_length=30)
    # cpf = models.CharField('CPF', max_length=11, unique=True, blank=True, null=True)
    is_organizer = models.BooleanField('organizador', default=False, help_text='Define se o usuário é um organizador, podem criar eventos na plataforma.')
    is_speaker = models.BooleanField('palestrante', default=False, help_text='Define se o usuário é um palestrante, podem ser chamados para participar de eventos.')
    is_staff = models.BooleanField('staff status', default=False, help_text='Define se o usuário tem permissão de entrar no site administrativo.')
    is_active = models.BooleanField('ativo', default=True, help_text='Define se o usuário deve ser tratado como ativo. Desmarque este campo ao invés de deletar usuários.')
    # is_trusty = models.BooleanField('confiável', default=False, help_text='Define se o usuário confirmou seu e-mail.')
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    # Django stuff
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_phone_number(self):
        phone_number = PhoneNumber.objects.filter(user=self, is_main=True)
        if phone_number:
            return phone_number.first()
        else:
            return None

    def get_all_phone_numbers(self):
        return PhoneNumber.objects.filter(user=self)

class PhoneNumber(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name="usuário")
    ddi = models.IntegerField(verbose_name='DDI')
    ddd = models.IntegerField(verbose_name='DDD')
    number = models.IntegerField(unique=True, verbose_name='número')
    is_main = models.BooleanField(verbose_name='telefone principal')

    def __str__(self):
        return f'+{self.ddi} ({self.ddd}) {self.number}'
