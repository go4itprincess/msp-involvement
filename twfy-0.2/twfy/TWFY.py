'''
testTWFY.py v.0.2.1
Author: dorzey@gmail.com

A library that provides a python binding to the TWFY API(http://www.theyworkforyou.com/api/)

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
import datetime
import time
import urllib

#API Spec
API = {'api':{
       'convertURL':[('output', 'url',), ()],
       'getConstituency':[('output', 'postcode',), ()],
       'getConstituencies':[('output',), ('date', 'search', 'latitude', 'longitude', 'distance')],
       'getMP':[('output',), ('postcode', 'constituency', 'id', 'always_return')],
       'getMPInfo':[('output', 'id',), ('fields')],
       'getMPsInfo':[('output', 'id',), ('fields')],
       'getMPs':[('output',), ('date', 'party', 'search')],
       'getLord':[('output', 'id',), ()],
       'getLords':[('output',), ('date', 'party', 'search')],
       'getMLAs':[('output',), ('date', 'party', 'search')],
       'getMSP':[('output',), ('postcode', 'constituency', 'id')],
       'getMSPs':[('output',), ('date', 'party', 'search')],
       'getGeometry':[('output',), ('name',)],
       'getCommittee':[('output', 'name',), ('date',)],
       'getDebates':[('output', 'type',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
       'getWrans':[('output',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
       'getWMS':[('output',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
       'getHansard':[('output',), ('search', 'person', 'order', 'page', 'num')],
       'getComments':[('output',), ('date', 'search', 'user_id', 'pid', 'page', 'num')]} 
        }

OUTPUTS = ['xml', 'php', 'js', 'rabx']
SERVICE_URL = 'http://www.theyworkforyou.com/api/'
TYPES = ['commons', 'westminsterhall', 'lords']

class TWFY():
    """
    Create an instance of this class with an API key to enable python bindings
    """
    def __init__(self, api_key):
        self.api_key = api_key
        # this enables 'twfy.getMP()', for example
        for prefix, methods in API.items():
            setattr(self, prefix, TWFYAPICategory(self, prefix, methods))
       
    def get(self, **params):
        """
        Calls the twfy API
        """
        params['key'] = self.api_key
        method = params['method']
        del params['method']
        params_encoded = urllib.urlencode(params)
        return urllib.urlopen(SERVICE_URL+method+'?'+params_encoded).read()

class TWFYAPICategory:
    """
    TWFYAPICategory is a modified version of RTMAPICategory in pyrtm (http://repo.or.cz/w/pyrtm.git)
    See the `API` structure and `TWFY.__init__`
    """
   
    def __init__(self, twfy, prefix, methods):
        self.twfy = twfy
        self.prefix = prefix
        self.methods = methods

    def __getattr__(self, attr):
        if attr in self.methods:
            rargs, oargs = self.methods[attr]
            return lambda **params: self.call_method(attr, rargs, oargs, **params)
        else:
            raise AttributeError, 'No such attribute: %s' % attr

    def call_method(self, aname, rargs, oargs, **params):
        """
        Checks for errors before calling the API"
        """
        if params['output'] in OUTPUTS:
            for required in rargs:
                if required not in params:
                    raise TypeError, 'Required parameter (%s) missing' % required

            for param in params:
                if param not in rargs + oargs:
                    raise TypeError, 'Invalid parameter (%s)' % param
            
            if 'type' in params:
                if params['type'] not in TYPES:
                    raise TypeError, 'Invalid type given: (%s)' % params['type']
                
            if 'date' in params:
                if not is_valid_date(params['date']):
                    raise TypeError, 'Invalid date given: (%s)' % params['date']
                
            return self.twfy.get(method=aname, **params)
        else:
            raise TypeError, 'Invalid output given: (%s)' % params['output']

def is_valid_date(date):
    """
    Checks to see if the date is valid. dd/mm/yyyy
    """
    if date == '':
        return True
    else:
        try:
            c = time.strptime(date, "%d/%m/%Y")
            if datetime.datetime(*c[:6]).date() <= datetime.datetime.today().date():
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False
