(function() {
  'use strict';

  // X-EDITABLE
  //defaults
  $.fn.editable.defaults.inputclass = 'form-control';
  // $.fn.editable.defaults.url = '/post';

  //enable / disable
  $('input[name="enable"]').on('change', function() {
    $('#user .editable').editable('toggleDisabled');
  });

  // mode
  if (window.location.href.match(/mode=inline/i)) {
    $.fn.editable.defaults.mode = 'inline';
    $('#editinline').attr('checked', true);
  } else {
    $('#editinline').attr('checked', false);
  }
  $('#editinline').on('change', function() {
    var location = 'frm-xeditable.html';
    if ($(this).is(':checked')) {
      window.location.href = location + '?mode=inline';
    } else {
      window.location.href = location;
    }
  });


  //editables
  $('#username').editable();

  $('#firstname').editable({
    validate: function(value) {
      if ($.trim(value) === '') {
        return 'This field is required';
      }
    }
  });

  $('#sex').editable({
    inputclass: 'select',
    prepend: 'not selected',
    source: [{
      value: 1,
      text: 'Male'
    }, {
      value: 2,
      text: 'Female'
    }],
    display: function(value, sourceData) {
      var colors = {
        '': '#AAB2BD',
        1: '#4FC1E9',
        2: '#AC92EC'
      },
      elem = $.fn.editableutils.itemsByValue(value, sourceData);

      if (elem.length) {
        $(this).text(elem[0].text).css('color', colors[value]);
      } else {
        $(this).empty();
      }
    }
  });

  $('#vacation').editable({
    datepicker: {
      todayBtn: 'linked'
    }
  });

  $('#dob').editable();

  $('#event').editable({
    placement: 'right',
    combodate: {
      firstItem: 'name'
    }
  });

  $('#comments').editable({
    showbuttons: 'bottom'
  });

  // Single dataset
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substrRegex;

      // an array that will be populated with substring matches
      matches = [];

      // regex used to determine if a string contains the substring `q`
      substrRegex = new RegExp(q, 'i');

      // iterate through the pool of strings and for any string that
      // contains the substring `q`, add it to the `matches` array
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          // the typeahead jQuery plugin expects suggestions to a
          // JavaScript object, refer to typeahead docs for more info
          matches.push({
            value: str
          });
        }
      });

      cb(matches);
    };
  },
  typeaheadData = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Dakota', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'];

  $('#state').editable({
    value: 'California',
    typeahead: {
      name: 'state',
      displayKey: 'value',
      source: substringMatcher(typeaheadData)
    }
  });

  $('#fruits').editable({
    inputclass: 'chk_editable', // this use for attr name on chekbox, so you can get value manually with this selector. example => $( '[name="chk_editable"]' ).val()
    pk: 1,
    limit: 3,
    source: [
    {value: 1, text: 'banana'},
    {value: 2, text: 'peach'},
    {value: 3, text: 'apple'},
    {value: 4, text: 'watermelon'},
    {value: 5, text: 'orange'}
    ]
  });

  var countries = [];
  $.each({ 'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'WF': 'Wallis and Futuna', 'BL': 'Saint Bartelemey', 'BM': 'Bermuda', 'BN': 'Brunei Darussalam', 'BO': 'Bolivia', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BT': 'Bhutan', 'JM': 'Jamaica', 'BV': 'Bouvet Island', 'BW': 'Botswana', 'WS': 'Samoa', 'BR': 'Brazil', 'BS': 'Bahamas', 'JE': 'Jersey', 'BY': 'Belarus', 'O1': 'Other Country', 'LV': 'Latvia', 'RW': 'Rwanda', 'RS': 'Serbia', 'TL': 'Timor-Leste', 'RE': 'Reunion', 'LU': 'Luxembourg', 'TJ': 'Tajikistan', 'RO': 'Romania', 'PG': 'Papua New Guinea', 'GW': 'Guinea-Bissau', 'GU': 'Guam', 'GT': 'Guatemala', 'GS': 'South Georgia and the South Sandwich Islands', 'GR': 'Greece', 'GQ': 'Equatorial Guinea', 'GP': 'Guadeloupe', 'JP': 'Japan', 'GY': 'Guyana', 'GG': 'Guernsey', 'GF': 'French Guiana', 'GE': 'Georgia', 'GD': 'Grenada', 'GB': 'United Kingdom', 'GA': 'Gabon', 'SV': 'El Salvador', 'GN': 'Guinea', 'GM': 'Gambia', 'GL': 'Greenland', 'GI': 'Gibraltar', 'GH': 'Ghana', 'OM': 'Oman', 'TN': 'Tunisia', 'JO': 'Jordan', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HM': 'Heard Island and McDonald Islands', 'VE': 'Venezuela', 'PR': 'Puerto Rico', 'PS': 'Palestinian Territory', 'PW': 'Palau', 'PT': 'Portugal', 'SJ': 'Svalbard and Jan Mayen', 'PY': 'Paraguay', 'IQ': 'Iraq', 'PA': 'Panama', 'PF': 'French Polynesia', 'BZ': 'Belize', 'PE': 'Peru', 'PK': 'Pakistan', 'PH': 'Philippines', 'PN': 'Pitcairn', 'TM': 'Turkmenistan', 'PL': 'Poland', 'PM': 'Saint Pierre and Miquelon', 'ZM': 'Zambia', 'EH': 'Western Sahara', 'RU': 'Russian Federation', 'EE': 'Estonia', 'EG': 'Egypt', 'TK': 'Tokelau', 'ZA': 'South Africa', 'EC': 'Ecuador', 'IT': 'Italy', 'VN': 'Vietnam', 'SB': 'Solomon Islands', 'EU': 'Europe', 'ET': 'Ethiopia', 'SO': 'Somalia', 'ZW': 'Zimbabwe', 'SA': 'Saudi Arabia', 'ES': 'Spain', 'ER': 'Eritrea', 'ME': 'Montenegro', 'MD': 'Moldova, Republic of', 'MG': 'Madagascar', 'MF': 'Saint Martin', 'MA': 'Morocco', 'MC': 'Monaco', 'UZ': 'Uzbekistan', 'MM': 'Myanmar', 'ML': 'Mali', 'MO': 'Macao', 'MN': 'Mongolia', 'MH': 'Marshall Islands', 'MK': 'Macedonia', 'MU': 'Mauritius', 'MT': 'Malta', 'MW': 'Malawi', 'MV': 'Maldives', 'MQ': 'Martinique', 'MP': 'Northern Mariana Islands', 'MS': 'Montserrat', 'MR': 'Mauritania', 'IM': 'Isle of Man', 'UG': 'Uganda', 'TZ': 'Tanzania, United Republic of', 'MY': 'Malaysia', 'MX': 'Mexico', 'IL': 'Israel', 'FR': 'France', 'IO': 'British Indian Ocean Territory', 'FX': 'France, Metropolitan', 'SH': 'Saint Helena', 'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands (Malvinas)', 'FM': 'Micronesia, Federated States of', 'FO': 'Faroe Islands', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NA': 'Namibia', 'VU': 'Vanuatu', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NZ': 'New Zealand', 'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'CK': 'Cook Islands', 'CI': 'Cote dIvoire', 'CH': 'Switzerland', 'CO': 'Colombia', 'CN': 'China', 'CM': 'Cameroon', 'CL': 'Chile', 'CC': 'Cocos (Keeling) Islands', 'CA': 'Canada', 'CG': 'Congo', 'CF': 'Central African Republic', 'CD': 'Congo, The Democratic Republic of the', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'CX': 'Christmas Island', 'CR': 'Costa Rica', 'CV': 'Cape Verde', 'CU': 'Cuba', 'SZ': 'Swaziland', 'SY': 'Syrian Arab Republic', 'KG': 'Kyrgyzstan', 'KE': 'Kenya', 'SR': 'Suriname', 'KI': 'Kiribati', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 'KM': 'Comoros', 'ST': 'Sao Tome and Principe', 'SK': 'Slovakia', 'KR': 'Korea, Republic of', 'SI': 'Slovenia', 'KP': 'Korea, Democratic Peoples Republic of', 'KW': 'Kuwait', 'SN': 'Senegal', 'SM': 'San Marino', 'SL': 'Sierra Leone', 'SC': 'Seychelles', 'KZ': 'Kazakhstan', 'KY': 'Cayman Islands', 'SG': 'Singapore', 'SE': 'Sweden', 'SD': 'Sudan', 'DO': 'Dominican Republic', 'DM': 'Dominica', 'DJ': 'Djibouti', 'DK': 'Denmark', 'VG': 'Virgin Islands, British', 'DE': 'Germany', 'YE': 'Yemen', 'DZ': 'Algeria', 'US': 'United States', 'UY': 'Uruguay', 'YT': 'Mayotte', 'UM': 'United States Minor Outlying Islands', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LA': 'Lao Peoples Democratic Republic', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TT': 'Trinidad and Tobago', 'TR': 'Turkey', 'LK': 'Sri Lanka', 'LI': 'Liechtenstein', 'A1': 'Anonymous Proxy', 'TO': 'Tonga', 'LT': 'Lithuania', 'A2': 'Satellite Provider', 'LR': 'Liberia', 'LS': 'Lesotho', 'TH': 'Thailand', 'TF': 'French Southern Territories', 'TG': 'Togo', 'TD': 'Chad', 'TC': 'Turks and Caicos Islands', 'LY': 'Libyan Arab Jamahiriya', 'VA': 'Holy See (Vatican City State)', 'VC': 'Saint Vincent and the Grenadines', 'AE': 'United Arab Emirates', 'AD': 'Andorra', 'AG': 'Antigua and Barbuda', 'AF': 'Afghanistan', 'AI': 'Anguilla', 'VI': 'Virgin Islands, U.S.', 'IS': 'Iceland', 'IR': 'Iran, Islamic Republic of', 'AM': 'Armenia', 'AL': 'Albania', 'AO': 'Angola', 'AN': 'Netherlands Antilles', 'AQ': 'Antarctica', 'AP': 'Asia/Pacific Region', 'AS': 'American Samoa', 'AR': 'Argentina', 'AU': 'Australia', 'AT': 'Austria', 'AW': 'Aruba', 'IN': 'India', 'AX': 'Aland Islands', 'AZ': 'Azerbaijan', 'IE': 'Ireland', 'ID': 'Indonesia', 'UA': 'Ukraine', 'QA': 'Qatar', 'MZ': 'Mozambique' }, function(k, v) {
    countries.push({
      id: k,
      text: v
    });
  });

  // select2
  $('#country').editable({
    inputclass: 'select2-select',
    source: countries,
    select2: {
      width: 200,
      placeholder: 'Select country'
    }
  });

  $('#address').editable({
    // url: '/post',
    value: {
      city: 'Pekalongan',
      street: 'Central Java',
      building: '25'
    },
    validate: function(value) {
      if (value.city === '') {
        return 'city is required!';
      }
    },
    display: function(value) {
      if (!value) {
        $(this).empty();
        return;
      }
      var html = '<b>' + $('<div>').text(value.city).html() + '</b>, ' + $('<div>').text(value.street).html() + ' st., bld. ' + $('<div>').text(value.building).html();
      $(this).html(html);
    }
  });


  // auto open
  $('#user .editable').on('hidden', function(e, reason) {
    if (reason === 'save' || reason === 'nochange') {
      var $next = $(this).closest('tr').next().find('.editable');
      if ($('#autoopen').is(':checked')) {
        setTimeout(function() {
          $next.editable('show');
        }, 300);
      } else {
        $next.focus();
      }
    }
  });
})(window);