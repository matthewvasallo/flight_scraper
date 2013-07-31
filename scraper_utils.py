#!/bin/zsh

import time
import dateutil
import calendar
import datetime

from scraper_controller import run_all
from scraper_engine import *

from datetime import *
from mongoengine import *
from dateutil.rrule import *
from dateutil.parser import *


def search_flights(date_pair, origin, dest):

	for d in date_pairs:

		dep_date = d[0].strftime("%Y-%m-%d")
		return_date = d[1].strftime("%Y-%m-%d")

		print "Searching %s -> %s : %s to %s" % (origin, dest, dep_date, return_date)
		run_all(origin, dest, dep_date, return_date)


def generate_date_pairs(frequency, weekdays, start_date, until_date):

	until_date = until_date.strftime('%m-%d-%Y')

	dates = list(rrule(frequency, byweekday=weekdays, dtstart=start_date, until=parse(until_date)))

	date_pairs = list()

	i = 1
	for d in dates:
		#For first date in pair - DEPARTURE DATE
		if (i%2 != 0):
			p = list()
			p.append(d)
		#For second date in pair - RETURN DATE
		else:
			p.append(d)
			date_pairs.append(p)
		i += 1

	return date_pairs

#This method returns a dict of all queried prices and query_date for a specific date_pair
def get_all_prices_for_date_pair(date_pair):

	result = dict()
	solutions = Solution.objects(depart_date=date_pair[0], return_date=date_pair[1])

	for sol in solutions:
		query_date = sol.query_date.strftime('%m-%d-%Y')
		min_price = sol.min_price[3:] #get rid of USD
		
		if (not result.has_key(query_date)):
			prices = list()
			prices.append(min_price)
			result[query_date] = prices
		else:
			result[query_date].append(min_price) 

	return result

















