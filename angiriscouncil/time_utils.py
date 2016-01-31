import time
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

