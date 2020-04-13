from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
GENDER_CHOICES = (
    ("0", u"male"),
    ("1", u"female")
)


class UserBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20, blank=False, default='')
    middle_name = models.CharField(max_length=20, blank=True, default='')
    last_name = models.CharField(max_length=20, blank=False, default='')
    gender = models.CharField("gender", max_length=6, choices=GENDER_CHOICES, default="female")
    title = models.TextField()
    des = models.TextField(blank=False)
    birthday = models.DateField("year-month-day",null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['created']
        verbose_name = "user information"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.first_name + self.middle_name + self.last_name


class Mentor(UserBase):
    expertiseFields = models.TextField()
    isAvailable = models.BooleanField(default=False)

    class Meta:
        verbose_name = "mentor information"
        verbose_name_plural = verbose_name


class Seeker(UserBase):
    seekingFields = models.TextField(blank=True)

    class Meta:
        verbose_name = "seeker information"
        verbose_name_plural = verbose_name