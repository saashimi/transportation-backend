import requests
import logging
from APIimports import constants
from APIimports.models import ApiElement
import sys


logger = logging.getLogger(__name__)


def oneRingToBindThem():


    for name, metadata in constants.API_META.items():

        # Prevent duplicates for now.  Later we'll need to be
        # more sophisticated about how we handle repeated downloads
        if name in list(ApiElement.objects.values_list('apiName', flat=True)):
            print("Skipped {} because it's already in the database.".format(name))
            continue
        response = requests.get(metadata['uri'])

        try:
            response.raise_for_status()
            geojson = response.json()

            apiElement = ApiElement(
                payload=geojson,
                url=metadata['uri'],
                apiName=name,
                projectName=metadata['projectName']
            )
            apiElement.save()

        except requests.exceptions.HTTPError:
            logger.exception("non 200 response from api request " + metadata['uri'])
        except ValueError:
            logger.exception("exception parsing json in response from api request against " + metadata['uri'])
