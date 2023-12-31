import logging

import pdpyras

logger = logging.getLogger(__name__)


def get_client(api_key: str):
    return pdpyras.APISession(api_key)


def get_current_user(client: pdpyras.APISession):
    return client.rget("users/me")


def get_triggered_incidents(client: pdpyras.APISession, user_ids=[], urgencies=[]):
    logger.debug("Listing incidents")

    return client.rget(
        "incidents",
        params={
            "user_ids": user_ids,
            "urgencies": urgencies,
            "total": True,
            "statuses": ["triggered"],
            "sort_by": "incident_number:desc",
        },
    )


def acknowledge_incidents(client: pdpyras.APISession, incident_ids=[]):
    logger.debug("Acknowleding incidents")
    if not incident_ids:
        logger.debug("No incidents to acknowledge")
        return

    body = {
        "incidents": [
            {"id": incident_id, "type": "incident_reference", "status": "acknowledged"}
            for incident_id in incident_ids
        ]
    }

    return client.rput(
        "incidents",
        params={
            "total": True,
        },
        json=body,
    )
