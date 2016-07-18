import time
import pytz
from datetime import datetime
from collections import OrderedDict

def time_ago(unix_timestamp):
	"""
	Returns the length of time specified in seconds formatted to replicate
	how Reddit does it. Example: 1 day ago
	"""
	now = time.time()
	units = OrderedDict()
	units['year']   = 60 * 60 * 24 * 365
	units['month']  = 60 * 60 * 24 * 30
	units['week']   = 60 * 60 * 24 * 7
	units['day']    = 60 * 60 * 24
	units['hour']   = 60 * 60
	units['minute'] = 60
	units['second'] = 1

	for unit, seconds in units.items():
		n = int((now - unix_timestamp) / seconds) 
		if n:
			return "%d %s%s" % (n, unit, "s" if n > 1 else "")
	return 'just now'

def pacific_time_now():
	"""
	Returns the current time in L.A.
	"""
	tz = pytz.timezone('America/Los_Angeles')
	return datetime.now(tz)

def weekday_word():
	"""
	Returns the English name for the current weekday in America/Los_Angeles
	"""
	return pacific_time_now().strftime("%A")

def us_date():
	"""
	Returns the US formatted date string for the current time in
	America/Los_Angeles
	Example: 12/8/92 for Dec 8th 1992
	"""
	return pacific_time_now().strftime("%m/%d/%y")	