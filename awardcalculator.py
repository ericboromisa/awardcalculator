
from sys import argv
from os.path import exists
import csv

chart_file_list = ['ASChart.csv', 'UAChart.csv', 'ACChart.csv']
region_file = 'regionlist.csv'
airport_file = 'Airports.csv'

def is_empty(any_structure):
    if any_structure:
        print('Structure is not empty.')
        return False
    else:
        print('Structure is empty.')
        return True

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False	
	
class RegionList:
	def __init__(self, keys, line):
		self.airport_code = line[0]
		self.unique_region_name = line[2]
		self.region_mapping = dict(zip(keys, line[3:17]))
		

class Airport:
	def __init__(self, line):
		self.airport_name = line[1]
		self.city = line[2]
		self.country = line[3]
		self.airport_code = line[4]
		self.latitude = line[6]
		self.longitude = line[7]
		self.utc_offset = line[9]
		self.region_mapping = dict()

	def setRegionLists(self, region_database):
		print "enter region assignment"
		
		for x in region_database:
			if self.airport_code ==  x.airport_code:
				self.region_mapping = x.region_mapping
				print "Matched based on airport code"

				break

		if(is_empty(self.region_mapping)):
			for x in region_database:
				#print self.country
				#print x.unique_region_name
				if self.country == x.unique_region_name:
					self.region_mapping = x.region_mapping
					print "matched based on country"
					break

	
		
		





class PriceList:
	def __init__(self, prices):
		#print prices
		if is_number(prices[0]):
			self.economy = int(prices[0])
		else:
			self.economy = None
		if is_number(prices[1]):
			self.business = int(prices[1])
		else:
			self.business = None
		if is_number(prices[2]):
			self.first = int(prices[2])
		else:
			self.first = None
		if is_number(prices[3]):
			self.off_peak = int(prices[3])
		else:
			self.off_peak = None
		

	def __repr__(self):
	    return "PriceList()"

	def __str__(self):
	
		return "From str method of PriceList: economy is %s, business is %s, first is %s" % (self.economy, self.business, self.first)

class Redemption:
	def __init__(self, line):
		self.operating_carrier = line[1]
		self.origin = line[2]
		self.destination = line[3]
		self.price_list = PriceList(line[4:])
		#print self.price_list

	@classmethod
	def fromReverseRedemption(self,redemption):
		self.operating_carrier = redemption.operating_carrier
		self.destination = redemption.origin
		self.origin = redemption.destination
		self.price_list = redemption.price_list
		
		return self

	def __repr__(self):
	    return "From str method of Redemption: \noperating carrier is: %s, \norigin is: %s, \ndestination is: %s, \nprice_list is %s \n\n" % (self.operating_carrier, self.origin, self.destination, self.price_list)

	def __str__(self):
		return "From str method of Redemption: operating carrier is: %s, origin is: %s, destination is: %s, price_list is %s \n" % (operating_carrier, origin, destination, price_list)

class Program:
	def __init__(self, csv):

		self.name = ""
		self.partner_chart_list = []
		self.redemptions = []
		csv.next()
		for row in csv:
			
			if self.name == "":
				self.name = row[0]
				print self.name

			if row[1] not in self.partner_chart_list:
				self.partner_chart_list.append(row[1])

			redemption = Redemption(row)
			
			#print redemption.origin
			self.redemptions.append(redemption)
			
			reverse_redemption = Redemption.fromReverseRedemption(redemption)
			self.redemptions.append(reverse_redemption)
		#print self.redemptions

	def isOffpeak(self, date):
		return True

	def findCheapestRedemption(self, origin, destination, cabin, date):
		price_list = []
		return_list = []
		for row in self.redemptions:
			#print row.destination 
			#print destination
			if(row.destination == destination and row.origin == origin):
				if(cabin == "Economy"):
					if(row.price_list.off_peak is not None and self.isOffpeak(date)):
						price_list.append([row.price_list.off_peak, row.operating_carrier])
					else:
						price_list.append([row.price_list.economy, row.operating_carrier])
					
				elif (cabin == "Business"):
					price_list.append([row.price_list.business, row.operating_carrier])
					
				elif (cabin == "First"):
					price_list.append([row.price_list.first, row.operating_carrier])
		
		valid_redemptions = list(x for x in price_list if x[0] is not None)
		print valid_redemptions
		#return_list = list(x for x in valid_redemptions if x[0] == min(valid_redemptions))
		
		if(valid_redemptions):
			prices = [x[0] for x in valid_redemptions]
			print prices
			min_price = min(prices)
			for item in valid_redemptions:
				if item[0] == min_price:
					return_list.append(item)
			print return_list
			#for item in valid_redemptions:
			#	if item[0] == min(valid_redemptions, key=lambda x: x[0]):
			#		return_list.append(item)	
			
			#return_list = map(lambda x : min(x[0]), valid_redemptions)
			return return_list
		else:
			return "No Valid Redemptions"

	def __repr__(self):
	    return "Program()"

	def __str__(self):
		return "member of Program"

class AwardDatabase:
	def __init__(self, chart_file_list):
		self.airlines = []
		for file in chart_file_list:
			f = open(file)
			raw_chart = csv.reader(f)
			program = Program(raw_chart)
			self.airlines.append(program)


### BUILD AWARD CHART DATABASE ###
response_list = []
region_database = []
airport_database = []
award_database = AwardDatabase(chart_file_list)

### BUILD REGION MAPPING DATABASE ###
# Turn into RegionDatabase Object like Award Database - stick file i/o into constructor

keys = []
r = open(region_file)
raw_region_reader = csv.reader(r)
rownum = 0
for row in raw_region_reader:
	if (rownum == 0):
		keys = row[3:17]
		rownum += 1
	else:
		region_database.append(RegionList(keys, row))

#for row in region_database:
#	print row.airport_code
#	print row.region_mapping

#print keys

### BUILD AIRPORT DATABASE ###

#Turn into Airport Database - stick file i/o into constructor

a = open(airport_file)
raw_airport_reader = csv.reader(a)

raw_airport_reader.next()
for row in raw_airport_reader:
	airport_database.append(Airport(row))

for i in range(0,len(airport_database)):
	airport_database[i].setRegionLists(region_database)
	#print airport_database[i].region_mapping.get("UA Region")

#for row in airport_database:
#	print row.airport_code
#	print row.latitude

#print keys



#print award_database.airlines[0].redemptions
#print award_database.airlines[0].partner_chart_list

### STATIC INPUTS ### - For now

dept_date = 7/7/2015
#"raw_input("Origin?: ")"

valid_Origin = False
while (valid_Origin is False):
	origin = raw_input("Origin?: ")
	for row in airport_database:
		if(row.airport_code == origin or row.city == origin or row.airport_name == origin):
			origin_region_dict = row.region_mapping
			valid_Origin = True
			break



valid_Destination = False
while (valid_Destination is False):
	destination = raw_input("Destination?: ")
	for row in airport_database:
		if(row.airport_code == destination or row.city == destination or row.airport_name == destination):
			dest_region_dict = row.region_mapping
			valid_Destination = True
			break


#destination_regions = getRegionLists(x, destination) for x in airport_database
print dest_region_dict.get("United")
print dest_region_dict.get("Alaska")

#acceptable_destinations = ["Australia / New Zealand", "Korean", "China", "Rest of Asia", "Middle East", "Europe", "Fiji", "Africa"]
#while destination not in acceptable_destinations:
#	destination = raw_input("Destination?: ")

class_of_service = raw_input("Class of Service?: (Economy, Business or First?) ")
acceptable_cabins = ["Economy", "Business", "First"]
while class_of_service not in acceptable_cabins:
	class_of_service = raw_input("Destination?: ")


print "So you want %s to %s in %s class?" % (origin, destination, class_of_service)


# Remember to clean up the region mapping headings to match the airline names
for airline in award_database.airlines:
	response = airline.name, airline.findCheapestRedemption(origin_region_dict.get(airline.name), dest_region_dict.get(airline.name), class_of_service, dept_date)
	response_list.append(response)

print response_list