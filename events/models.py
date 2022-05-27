from django.db import models
from django.urls import reverse


class State(models.Model):
    """
    The State model represents a US state with its name
    and abbreviation.

    State is a Value Object and, therefore, does not have a
    direct URL to view it.
    """

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.abbreviation}"

    class Meta:
        ordering = ("abbreviation",)  # Default ordering for State


class Location(models.Model):
    """
    The Location model describes the place at which an
    Event takes place, like a hotel or conference center.
    """

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    room_count = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    picture_url = models.URLField(max_length=200, null=True)
    state = models.ForeignKey(
        State,
        related_name="+",  # do not create a related name on State
        on_delete=models.PROTECT,
    )

    def get_api_url(self):
        return reverse("api_show_location", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)  # Default ordering for Location


class Conference(models.Model):
    """
    The Conference model describes a specific conference.
    """

    # Has a one-to-many relationship with presentations.Presentation
    # Has a one-to-many relationship with attendees.Attendee

    name = models.CharField(max_length=200)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    max_presentations = models.PositiveSmallIntegerField()
    max_attendees = models.PositiveIntegerField()

    location = models.ForeignKey(
        Location,
        related_name="conferences",
        on_delete=models.CASCADE,
    )

    def get_api_url(self):
        return reverse("api_show_conference", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("starts", "name")  # Default ordering for Conference
