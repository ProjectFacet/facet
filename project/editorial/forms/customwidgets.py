from bootstrap3_datetime.widgets import DateTimePicker
from django import forms




class ArrayFieldSelectMultiple(forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        self.delimiter = kwargs.pop('delimiter', ',')
        super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

    def render_options(self, choices, value):
        if isinstance(value, basestring):
            value = value.split(self.delimiter)
        return super(ArrayFieldSelectMultiple, self).render_options(choices, value)


class OurDateTimePicker(DateTimePicker):
	'''Replaces broken bootstrap 3 widget'''
	def __init__(self, *args, **kwargs):
		'''calls parent's init, replacing "language" option with "locale'''
		super(OurDateTimePicker, self).__init__(*args, **kwargs)
		self.options['locale'] = self.options['language']
		del self.options['language']
