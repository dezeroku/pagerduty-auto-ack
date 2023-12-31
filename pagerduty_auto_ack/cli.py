import argparse
import logging
import os
import time

from . import pd

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="pagerduty-auto-ack",
        description="Monitor and automatically ACKnowledge PagerDuty incidents",
    )

    parser.add_argument("--pagerduty-api-key", required=True)
    parser.add_argument(
        "--interval",
        required=False,
        type=int,
        default=60,
        help="how often (in seconds) to run the check",
    )
    parser.add_argument(
        "--urgency",
        required=False,
        choices=["high", "low"],
        action="append",
        default=[],
        dest="urgencies",
        help="defaults to all urgencies",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    pd_api_key = args.pagerduty_api_key

    try:
        ack_incidents = []
        with pd.get_client(pd_api_key) as pd_client:
            user = pd.get_current_user(pd_client)
            user_email = user.get("email")
            user_id = user.get("id")

            logger.info(f"Running as user: {user_email}")

            while True:
                incidents = pd.get_triggered_incidents(
                    pd_client, user_ids=[user_id], urgencies=args.urgencies
                )

                ack_incidents += incidents

                # PD API supports max of 250 acks at the same time
                # well, you shouldn't have that many anyway...
                incidents = incidents[:250]
                incident_ids = list(map(lambda x: x.get("id"), incidents))

                pd.acknowledge_incidents(pd_client, incident_ids)

                logger.info(f"Incidents acknowledged: {len(incident_ids)}")
                logger.debug(f"Sleeping for {args.interval} seconds")
                time.sleep(args.interval)

    except KeyboardInterrupt:
        count = len(ack_incidents)
        logger.info(f"Acknowledged {count} incidents")
        print("You can find a list of acknowledged incidents below:")
        for incident in ack_incidents:
            print(
                "#{0} {1}".format(
                    incident.get("incident_number"), incident.get("html_url")
                )
            )


if __name__ == "__main__":
    main()
