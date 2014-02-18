'''
An example that uses the python interface to the TWFY API(http://www.theyworkforyou.com/api/)

   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from twfy import TWFY
import json

twfy = TWFY.TWFY('B7Ben2G9Zu2kCnRUEwFzJLea')
#Get list of all MPs
#A date between '01/05/1997' and todays date.

##boundary=json.loads(twfy.api.getBoundary(name="East Lothian"), 'iso-8859-1')
##print boundary

mp_list = json.loads(twfy.api.getMSPs(output='js',date='01/08/2012'), 'iso-8859-1')
results = {}

#Count the number of MPs for each party.
for mp in mp_list:
    print mp
    party =  mp['party']
    if party in results.keys():
        results[party] += 1
    else:
        results[party] = 1

total_seats = float(sum(results.values()))

#Print the results.
for k, v in results.iteritems():
    print k, ' = ', (v/total_seats)*100, '%'



