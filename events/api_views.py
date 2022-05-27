from crypt import methods
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Conference, Location, State
from common.json import ModelEncoder
import json
import requests
from .acls import get_photo, get_lat_and_lon, get_weather_data


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
    ]

    def get_extra_data(self, o):
        return {"state": o.state.abbreviation}


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
    ]


@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    """
    Lists the conference names and the link to the conference.

    Returns a dictionary with a single key "conferences" which
    is a list of conference names and URLS. Each entry in the list
    is a dictionary that contains the name of the conference and
    the link to the conference's information.

    {
        "conferences": [
            {
                "name": conference's name,
                "href": URL to the conference,
            },
            ...
        ]
    }
    """
    # response = []
    # conferences = Conference.objects.all()
    # for conference in conferences:
    #     response.append(
    #         {
    #             "name": conference.name,
    #             "href": conference.get_api_url(),
    #         }
    #     )
    # return JsonResponse({"conferences": response})

    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
        )
    else:  # POST
        content = json.loads(request.body)

        # Get the Location object and put it in the content dict
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )

        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_conference(request, pk):
    """
    Returns the details for the Conference model specified
    by the pk parameter.

    This should return a dictionary with the name, starts,
    ends, description, created, updated, max_presentations,
    max_attendees, and a dictionary for the location containing
    its name and href.

    {
        "name": the conference's name,
        "starts": the date/time when the conference starts,
        "ends": the date/time when the conference ends,
        "description": the description of the conference,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "max_presentations": the maximum number of presentations,
        "max_attendees": the maximum number of attendees,
        "location": {
            "name": the name of the location,
            "href": the URL for the location,
        }
    }
    """
    if request.method == "GET":
        conference = Conference.objects.get(id=pk)
        try:
            city = conference.location.city
            state = conference.location.state
            conference_lat = get_lat_and_lon(city, state)[0]
            conference_lon = get_lat_and_lon(city, state)[1]
            weather = get_weather_data(conference_lat, conference_lon)
        except:
            weather = None
        return JsonResponse(
            {"conference": conference, "weather": weather},
            encoder=ConferenceDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})
    else:  # PUT
        content = json.loads(request.body)
        try:
            if "location" in content:
                location = Location.objects.get(id=content["location"])
                content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "invalid location id"},
                status=400,
            )
        Conference.objects.filter(id=pk).update(**content)
        conference = Conference.objects.get(id=pk)
        try:
            city = conference.location.city
            state = conference.location.state
            conference_lat = get_lat(city, state)
            conference_lon = get_lon(city, state)
            weather = get_weather_data(conference_lat, conference_lon)
        except:
            weather = None
        return JsonResponse(
            {"conference": conference, "weather": weather},
            encoder=ConferenceDetailEncoder,
            safe=False,
        )


#        # copied from get detail
#        location = Location.objects.get(id=pk)
#        return JsonResponse(
#            location,
#            encoder=LocationDetailEncoder,
#            safe=False,)


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    """
    Lists the location names and the link to the location.

    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.

    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """
    # locations = [
    #     {"name": l.name, "href": l.get_api_url()}
    #     for l in Location.objects.all()
    # ]
    # return JsonResponse({"locations": locations})

    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations},
            encoder=LocationListEncoder,
        )
    else:  # POST
        content = json.loads(request.body)
        try:
            # Get the State object and put it in the content dict
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
            city = content["city"]
            content["picture_url"] = get_photo(city, state)
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )

        location = Location.objects.create(**content)

        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, pk):
    """
    Returns the details for the Location model specified
    by the pk parameter.

    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.

    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "state": the two-letter abbreviation for the state,
    }
    """
    # location = Location.objects.get(id=pk)

    # return JsonResponse(
    #     {
    #         "name": location.name,
    #         "city": location.city,
    #         "room_count": location.room_count,
    #         "created": location.created,
    #         "updated": location.updated,
    #         "state": location.state.abbreviation,
    #     }
    # )

    # copied from create
    if request.method == "GET":
        location = Location.objects.get(id=pk)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})
    else:  # PUT
        # copied from create
        content = json.loads(request.body)
        try:
            # new code
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )

        # new code
        Location.objects.filter(id=pk).update(**content)

        # copied from get detail
        location = Location.objects.get(id=pk)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
