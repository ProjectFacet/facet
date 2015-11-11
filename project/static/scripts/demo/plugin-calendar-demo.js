(function(){
  'use strict';

  // basic style
  $('#calendar1').clndr();

  // with inverse bg
  $('#calendar2').clndr();


  // calendar
  var moment = window.moment,
  currentMonth = moment().format('YYYY-MM'),
  nextMonth    = moment().add('month', 1).format('YYYY-MM'),
  myEvents = [{ date: currentMonth + '-' + '10', title: 'Persian Kitten Auction', location: 'Center for Beautiful Cats' },
  { date: currentMonth + '-' + '19', title: 'Cat Frisbee', location: 'Jefferson Park' },
  { date: currentMonth + '-' + '23', title: 'Kitten Demonstration', location: 'Center for Beautiful Cats' },
  { date: nextMonth + '-' + '07',    title: 'Small Cat Photo Session', location: 'Center for Cat Photography' }];

  $('#calendar3').clndr({
    template: $('#full-clndr-template').html(),
    daysOfTheWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    events: myEvents,
    targets: {
      nextButton: 'clndr-next-btn',
      previousButton: 'clndr-prev-btn',
      nextYearButton: 'clndr-next-year-btn',
      previousYearButton: 'clndr-prev-year-btn',
      todayButton: 'clndr-today-btn',
      day: 'day',
      empty: 'empty'
    },
  });
})(window);