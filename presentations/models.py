from django.db import models
from django.urls import reverse


class Status(models.Model):
    """
    The Status model provides a status to a Presentation, which
    can be SUBMITTED, APPROVED, or REJECTED.

    Status is a Value Object and, therefore, does not have a
    direct URL to view it.
    """

    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)  # Default ordering for Status
        verbose_name_plural = "statuses"  # Fix the pluralization


class Presentation(models.Model):
    """
    The Presentation model represents a presentation that a person
    wants to give at the conference.
    """

    presenter_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    presenter_email = models.EmailField()

    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey(
        Status,
        related_name="presentations",
        on_delete=models.PROTECT,
    )

    conference = models.ForeignKey(
        "events.Conference",
        related_name="presentations",
        on_delete=models.CASCADE,
    )

    def get_api_url(self):
        return reverse("api_show_presentation", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    def approve(self):
        status = Status.objects.get(name="APPROVED")
        self.status = status
        self.save()

    def reject(self):
        status = Status.objects.get(name="REJECTED")
        self.status = status
        self.save()

    class Meta:
        ordering = ("title",)  # Default ordering for presentation
