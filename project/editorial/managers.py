""" """

# FIXME: this is seriously under-documented

from datetime import datetime
from actstream.managers import ActionManager, stream


class MyActionManager(ActionManager):
    @stream
    def mystream(self, obj, verb='posted', time=None):
        if time is None:
            # FIXME from Joel: this probably should be TZ-aware
            time = datetime.now()
        return obj.actor_actions.filter(verb=verb, timestamp__lte=time)
