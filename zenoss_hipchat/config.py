"""
Simple environment variable based configuration for now
"""

import os


HIPCHAT_API_V1_TOKEN = os.environ.get('HIPCHAT_TOKEN', None)
HIPCHAT_ROOM_ID = os.environ.get('HIPCHAT_ROOM', None)
HIPCHAT_API_V1_ENDPOINT = os.environ.get(
    'HIPCHAT_API_ENDPOINT',
    'api.hipchat.com'
)
HIPCHAT_FROM = os.environ.get('HIPCHAT_FROM', 'Zenoss')
REQUEST_TIMEOUT = os.environ.get('HIPCHAT_TIMEOUT', 3)
NOTIFY_SEVERITY = os.environ.get('HIPCHAT_NOTIFY_SEVERITY', 4)
