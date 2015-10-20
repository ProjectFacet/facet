from django.db import models





class Story(models.Model):
    """A story contains universal information for a specific story"""
    pass


class WebForm(models.Model):
    """ The web article version of a story."""
    pass


class RadioForm(models.Model):
    """ The radio version of a story."""
    pass

class TvForm(models.Model):
    """ The television version of a story."""
    pass


class PrintForm(models.Model):
    """ The print version of a story."""
    pass


# future thinking: should every iteration of a platform have it's own class?
# OR: subclass newspaper and magazine under PrintForm...

