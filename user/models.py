from xmlrpc.client import boolean
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
import uuid


def upload_img(instance, filename):

    ext = filename.split('.')[-1]
    if str(ext) == 'jpg' or str(ext) == 'png':
        return 'profile/' + str(instance.user.id) + '.' + str(ext)
    else:
        return 'profile/' + str(instance.user.id) + '.jpg'


class AccountManager(BaseUserManager):
    """
    create user and superuser
    """

    def create_user(self, first_name, last_name, username, phone_number, email, password):
        if not email:
            raise ValueError('Please enter your email')
        if not username:
            raise ValueError('Please enter your username')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            email=self.normalize_email(email),
        )

        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, phone_number, email, password=None):

        user = self.create_user(
            first_name,
            last_name,
            username,
            phone_number,
            email,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    # usernameはuniqueをtrueにする必要がある
    username = models.CharField(max_length=50, default='anonimous')
    # 携帯電話番号を確認する必要がある。
    # phone_number = models.
    email = models.EmailField(max_length=100, unique=True)
    phoneNumberRegex = RegexValidator(regex = r"^\d{8,16}$")
    phone_number= models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, blank=True, null=True)
    # required
    # rest_frameworkの場合にtoken発行の際is_activeがtrue出なければエラーが発生することに注意
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_lebel):
        return True


class Adress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, default=None, null=True)
    country = models.CharField(max_length=255, default='Japan')
    prefecture = models.CharField(max_length=255, default=None, null=True)
    region = models.CharField(max_length=250, default=None, null=True)
    address = models.CharField(max_length=50, default=None, null=True)
    building_name = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    postalcode = models.CharField(max_length=50, default=None, null=True)
    phoneNumberRegex = RegexValidator(regex = r"^\d{8,16}$")

    def __str__(self):
        return str(self.user)


GENDER = [
    ("男性",  "men"),
    ("女性", "women"),
]


class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        Account,  on_delete=models.CASCADE, default=None, null=True)
    gender = models.CharField(
        choices=GENDER, default=None, blank=True, null=True, max_length=2)
    birth_day = models.DateField(null=True, blank=True, default=None)
    img = models.FileField(blank=True, null=True,
                           upload_to=upload_img, default=None)
    introduction = models.TextField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user.username)


class EmailSubscribe(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    recipient_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.is_active:
            return self.user.username + '(購読中)'
        else:
            return self.user.username

class RandomNumber(models.Model):
    number = models.CharField(max_length=4, unique=True)

class AuthPhoneNumber(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    random_number = models.ForeignKey(RandomNumber, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + self.random_number.number