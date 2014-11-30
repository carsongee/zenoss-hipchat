"""
Python command to generate hipchat notification from Zenoss
events.
"""
from __future__ import print_function
import argparse
import sys


from zenoss_hipchat import config
from zenoss_hipchat.hipchat import HipChatEvent


def entry_point():
    """
    Entry point to script.
    """

    parser = argparse.ArgumentParser(
        prog='zenoss_hipchat',
        description=('Converts arguments into templated strings and uses '
                     'HipChat APIv1 to send the event to a HipChat room '
                     'specified by the environment variable HIPCHAT_ROOM '
                     'and the API token in the environment variable '
                     'HIPCHAT_TOKEN')
    )

    # Add required arguments
    req_opts = parser.add_argument_group('required arguments')
    req_opts.add_argument('-d', '--device', type=str, required=True,
                          help='Device where event occurred')
    req_opts.add_argument('-i', '--info', type=str, required=True,
                          help='Short message for event')
    req_opts.add_argument('-c', '--component', type=str, required=True,
                          help='Component of device for event')
    req_opts.add_argument('-s', '--severity', type=int, required=True,
                          help='Severity number from 0-5. See '
                          'http://community.zenoss.org/docs/DOC-9437#d0e6134')
    req_opts.add_argument('-u', '--url', type=str, required=True,
                          help='URL to go to event notificaiton')
    req_opts.add_argument('-m', '--message', type=str, required=True,
                          help='Long event message')

    # Optional arguments
    parser.add_argument('-b', '--cleared-by', type=str,
                        help='What cleared the event (when --clear is set)')
    parser.add_argument('-o', '--clear', action="store_true",
                        help="Set if event is being cleared")

    args = parser.parse_args()

    if not config.HIPCHAT_API_V1_TOKEN and not config.HIPCHAT_ROOM_ID:
        print('Environment variable "HIPCHAT_TOKEN" and "HIPCHAT_ROOM" '
              'must be specified and valid before this command can be run')
        sys.exit(-1)

    if args.clear and not args.cleared_by:
        print('--cleared-by is required when using --clear')
        sys.exit(-1)

    hip_chat_event = HipChatEvent(**vars(args))
    hip_chat_event.send()
