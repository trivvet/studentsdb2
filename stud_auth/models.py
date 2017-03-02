from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class StProfile(models.Model):
    """To keep extra user data"""
    # user mapping
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = _(u"User Profile")

    # extra user data
    mobile_phone = models.CharField(
        verbose_name=_(u"Mobile Phone"),
        max_length=12,
        blank=True,
        default='')

    language = models.CharField(
        verbose_name=_(u"Language"),
        max_length=10,
        blank=True,
        default=''
    )

    time_zone = models.CharField(
        verbose_name=_(u"Time Zone"),
        max_length=128,
        blank=True,
        default=''
    )

    address = models.CharField(
        verbose_name=_(u"Address"),
        max_length=256,
        blank=True)

    passport = models.CharField(
        verbose_name=_(u"Passport Number"),
        max_length=20,
        blank=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=_(u"Photo"),
        null=True)

    def __unicode__(self):
        return self.user.username
