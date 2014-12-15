"""
Hipchat API
"""
import datetime

import requests

from zenoss_hipchat import config


class HipChatEventSendException(Exception):
    """
    Exception if the send failed
    """
    pass


class HipChatEvent(object):
    """
    Simple class for sending zenoss events to hipchat
    """

    SEVERITY_MAP = [
        ('green', 'Clear'),
        ('gray', 'Debug'),
        ('purple', 'Info'),
        ('yellow', 'Warn'),
        ('yellow', 'Error'),
        ('red', 'Crit'),
    ]

    NOTIFY_SEVERITY = config.NOTIFY_SEVERITY

    def __init__(
            self, device, info, component, severity,
            url, message, cleared_by, clear=False
    ):
        """
        Setup session and properties
        """
        self.device = device
        self.info = info
        self.component = component
        self.severity = severity
        self.url = url
        self.message = message
        self.cleared_by = cleared_by
        self.clear = clear
        self.time = datetime.datetime.now().isoformat()

        # Setup session
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.session.params = {
            'format': 'json',
            'auth_token': config.HIPCHAT_API_V1_TOKEN
        }
        self.post_url = 'https://{0}/v1/rooms/message'.format(
            config.HIPCHAT_API_V1_ENDPOINT
        )

    def _event_message(self):
        """
        Return templated event notification
        """
        return ('{device}: <a href="{url}">{info}</a><br />'
                '<b>Component</b>: {component}<br />'
                '<b>Time</b>: {time}<br />'
                '<b>Message</b>:'
                '{message}').format(**vars(self))

    def _clear_message(self):
        """
        Return templated clear notification
        """
        return ('<b><i>Cleared!</b></i><br />'
                '{device}:<a href="{url}">{info}</a> Cleared<br />'
                '<b>Cleared By</b>: {cleared_by}<br />'
                '<b>Component</b>: {component}<br />'
                '<b>Time</b>: {time}<br />'
                '<b>Message</b>:'
                '{message}').format(**vars(self))

    def _should_notify(self):
        """
        Determine if we should set the notify flag in HipChat call
        """
        if self.severity >= self.NOTIFY_SEVERITY:
            return 1
        return 0

    def send(self):
        """
        Send off the message to environment room with a nice template
        """

        if not self.clear:
            message = self._event_message()
        else:
            message = self._clear_message()

        from_name = "{0} ({1})".format(
            config.HIPCHAT_FROM, self.SEVERITY_MAP[self.severity][1]
        )

        response = self.session.post(
            url=self.post_url,
            data={
                'room_id': config.HIPCHAT_ROOM_ID,
                'from': from_name,
                'message_format': 'html',
                'notify': self._should_notify(),
                'color': self.SEVERITY_MAP[self.severity][0],
                'message': message
            },
            timeout=config.REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise HipChatEventSendException(response.text)
