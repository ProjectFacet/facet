""" A Calendar to display editorial content."""

from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


# class EditorialCalendar(HTMLCalendar):
#     """Create a month calendar view of content."""
#
#     def __init__(self, content):
#         super(EditorialCalendar, self).__init__()
#         self.content = self.group_by_day(content)
#
#     def formattime(self, day, time):
#         #TODO complete time
#         pass
#
#     def formatday(self, day, weekday):
#         if day !=0:
#             cssclass = self.cssclasses[weekday]
#             if date.today() == date(self.year, self.month, day):
#                 cssclass += 'today'
#             if day in self.content:
#                 cssclass += 'filled'
#                 body = ['<ul>']
#                 for facet in self.content[day]:
#                     body.append('<li>')
#                     body.append('<a href="%s">' % facet.get_absolute_url())
#                     body.append(esc(facet.title))
#                     body.append('</a></li>')
#                 body.append('</ul>')
#                 return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
#             return self.day_cell(cssclass, day)
#         return self.day_cell('noday', '&nbsp;')
#
#     def formatmonth(self, year, month):
#         self.year, self.month = year, month
#         return super (EditorialCalendar, self).formatmonth(year, month)
#
#     def group_by_day(self, workouts):
#         field = lambda content: content.due_edit.day
#         return dict(
#             [(day, list(items)) for day, items in groupby(content, field)]
#         )
#
#     def day_cell(self, cssclass, body):
#         return '<td class="%s">%s</td>' % (cssclass, body)
