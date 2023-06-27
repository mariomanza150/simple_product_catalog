from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveBigIntegerField,
    TextChoices,
    TextField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserTypes(TextChoices):
    ADMIN = "A", _("Adminstrator")
    MANAGER = "M", _("Manager")


class User(AbstractUser):
    """
    Default custom user model for Administrative users.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("username"), max_length=255, blank=False)
    user_type = CharField(max_length=1, choices=UserTypes.choices, default=UserTypes.MANAGER)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Product(Model):
    """
    Custom product model.
    If adding fields check forms.ProductAdd and forms.ProductEdit.
    """

    sku = CharField(max_length=12, unique=True)
    name = CharField(max_length=255, blank=False)
    brand = CharField(max_length=255, blank=False)
    price = PositiveBigIntegerField(blank=False)
    description = TextField()
    views = PositiveBigIntegerField(default=0)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def count_view(self):
        self.views = self.views + 1
        self.save()

    def update(self, *args, **kwargs):
        Notification(product=self).save()
        super().update(*args, **kwargs)


class Notification(Model):
    """
    Stores notifications to be picked up by celery and sent
    """

    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    has_sent = BooleanField(default=False)
