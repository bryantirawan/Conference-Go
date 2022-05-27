import re
from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee
from django.views.decorators.http import require_http_methods
from events.models import Conference
import json
from events.api_views import ConferenceDetailEncoder


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
    ]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
    ]

    def get_extra_data(self, o):
        return {
            "conference": {
                "name": o.conference.name,
            },
        }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    Returns a dictionary with a single key "attendees" which
    is a list of attendee names and URLS. Each entry in the list
    is a dictionary that contains the name of the attendee and
    the link to the attendee's information.

    {
        "attendees": [
            {
                "name": attendee's name,
                "href": URL to the attendee,
            },
            ...
        ]
    }
    """
    # attendees = [
    #     {
    #         "name": a.name,
    #         "href": a.get_api_url(),
    #     }
    #     for a in Attendee.objects.filter(conference=conference_id)
    # ]

    # return JsonResponse({"attendees": attendees})
    if request.method == "GET":
        attendees = Attendee.objects.all()
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:

        content = json.loads(request.body)

        # Get the Conference object and put it in the content dict
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, pk):
    """
    Returns the details for the Attendee model specified
    by the pk parameter.

    This should return a dictionary with email, name,
    company name, created, and conference properties for
    the specified Attendee instance.

    {
        "email": the attendee's email,
        "name": the attendee's name,
        "company_name": the attendee's company's name,
        "created": the date/time when the record was created,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    if request.method == "GET":
        attendee = Attendee.objects.get(id=pk)

        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=pk).delete()
        print(Attendee.objects.filter(id=pk).delete())
        return JsonResponse({"deleted": count > 0})
    else:
        # copied from create
        content = json.loads(request.body)
        try:
            # new code
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference"},
                status=400,
            )

        # new code
        Attendee.objects.filter(id=pk).update(**content)

        # copied from get detail
        attendee = Attendee.objects.get(id=pk)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
