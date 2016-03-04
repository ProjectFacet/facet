from bootstrap3_datetime.widgets import DateTimePicker


class OurDateTimePicker(DateTimePicker):
	'''Replaces broken bootstrap 3 widget'''
	def __init__(self, *args, **kwargs):
		'''calls parent's init, replacing "language" option with "locale'''
		super(OurDateTimePicker, self).__init__(*args, **kwargs)
		self.options['locale'] = self.options['language']
		del self.options['language']