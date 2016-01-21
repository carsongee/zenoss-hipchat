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
        ('red', 'Critical'),
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
            'auth_token': config.HIPCHAT_API_V2_TOKEN
        }
        self.post_url = 'https://{0}/v2/room/{1}/notification'.format(
            config.HIPCHAT_API_V2_ENDPOINT, config.HIPCHAT_ROOM_ID
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
            return True
        return False

    def send(self):
        """
        Send off the message to environment room with a nice template
        """
        if not self.clear:
            message = self._event_message()
        else:
            message = self._clear_message()

        if config.HIPCHAT_FROM == '':
            from_name = "{0}".format(
            self.SEVERITY_MAP[self.severity][1]
        )
        else:
            from_name = "{0} ({1})".format(
            config.HIPCHAT_FROM, self.SEVERITY_MAP[self.severity][1]
        )
        
        response = self.session.post(
            url=self.post_url,
            data={
                'from': from_name,
                'message_format': 'html',
                'notify': self._should_notify(),
                'color': self.SEVERITY_MAP[self.severity][0],
                'message': message
            },
            timeout=config.REQUEST_TIMEOUT
        )
        if response.status_code != 204:
            raise HipChatEventSendException(response.text)
