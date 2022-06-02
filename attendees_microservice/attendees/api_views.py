import re
from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee, ConferenceVO, AccountVO
from django.views.decorators.http import require_http_methods


import json


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


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
        "conference",
    ]
    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }

    def get_extra_data(self, o):
        count = AccountVO.objects.filter(email=o.email)
        print(count)
        if count != 0:
            return {"has_account": True}
        else:
            return {"has_account": False}


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
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
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:  # POST

        content = json.loads(request.body)

        # Get the Conference object and put it in the content dict
        try:
            conference_href = content["conference"]
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
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
