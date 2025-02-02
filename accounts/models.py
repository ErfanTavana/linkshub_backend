from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):
    """
    مدیریت سفارشی کاربران برای ایجاد کاربر با شماره تماس یا ایمیل.
    """

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('حداقل یکی از ایمیل یا شماره تماس باید وارد شود.')

        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        ایجاد سوپرکاربر (مدیر) با ایمیل (شماره تلفن اختیاری است)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff') or not extra_fields.get('is_superuser'):
            raise ValueError('مدیر باید is_staff=True و is_superuser=True داشته باشد.')

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True, null=True, blank=True,
        verbose_name="ایمیل"
    )
    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True,
        verbose_name="شماره تماس"
    )
    first_name = models.CharField(
        max_length=150, blank=True,
        verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=150, blank=True,
        verbose_name="نام خانوادگی"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="کارمند (دسترسی به پنل مدیریت)"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت"
    )

    # فیلدهای مربوط به احراز هویت اجتماعی
    github_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        verbose_name="شناسه گیت‌هاب"
    )
    google_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        verbose_name="شناسه گوگل"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # ایمیل به عنوان فیلد اصلی ورود
    REQUIRED_FIELDS = ["phone_number"]  # شماره تماس الزامی نیست، ولی می‌توان آن را وارد کرد

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.email if self.email else self.phone_number
