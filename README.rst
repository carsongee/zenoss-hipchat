zenoss-hipchat
==============

Command suitable in use for Zenoss notification commands for sending events to hipchat.


Installation
------------

Simply install using your preferred python package manager with
either: 

``pip install zenoss-hipchat``

for the latest release, or

``pip install -e git+https://github.com/pdxmaverick/zenoss-hipchat#egg=zenoss-hipchat``

for the latest development version.


Configuration
-------------

In Zenoss go to ``Events`` -> ``Triggers`` and create a trigger with
the rules for which you want to send events to hipchat.  Of course you
can use an existing trigger as well.  For more detailed guide on
triggers and notifications see the `community documentation
<http://wiki.zenoss.org/Notify_Me_of_Important_Events>`_.

After you have a trigger you wish to use, go to ``notifications`` and
create a new notification.  Set the ``Id`` to something memorable like
`HipChatErrors` or similar and choose ``Command`` as the action.

After creating the notification, edit it.  On the ``Notification`` tab
configure it as you see fit, but you are generally going to want to
make sure it is enabled, and that you have added the Trigger you
created earlier.  The command does support clear messages, so go ahead
and check that option if you like.

Now on the ``Content`` tab of the notification paste the following
into the ``Command`` field:

.. code-block:: bash

    zenoss-hipchat --device="${evt/device}" --info=${evt/summary} --component="${evt/component}" --severity=${evt/severity} --url="${urls/eventUrl}" --message=${evt/message}

And if you want to use the clear option, for the clear command:

.. code-block:: bash

    zenoss-hipchat --device="${evt/device}" --info=${evt/summary} --component="${evt/component}" --severity=${evt/severity} --url="${urls/eventUrl}" --message=${evt/message} --cleared-by="${evt/clearid}" --clear

You also need to provide the room and API token using the
``Environment variables`` field with something like:

.. code-block:: bash

    HIPCHAT_TOKEN=<APIv2 Token>;HIPCHAT_ROOM=<Room Name (or ID) to post to>

replacing the values with ones appropriate for you.


Additional Environment Variables
--------------------------------

In addition to ``HIPCHAT_TOKEN`` and ``HIPCHAT_ROOM`` which are
required, you can also override other options with the following
optional environment variables:

- ``HIPCHAT_API_V2_ENDPOINT`` - Allows you to override the API
  endpoint if you are using private HipChat
- ``HIPCHAT_FROM`` - Defaults to Zenoss, and determines who the
  messages appear to be coming from.
- ``HIPCHAT_TIMEOUT`` - Defaults to 3 seconds, but if you have a slow
  connection to the HipChat server it can be increased or decreased.
- ``HIPCHAT_NOTIFY_SEVERITY`` - Defaults to Error and above (4), but
  can raised or lowered and determines which events trigger the
  HipChat notification.
