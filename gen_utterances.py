#!/usr/bin/env python3

import sys
import random

city_list = ["New York", "Los Angeles", "Beijing", "Hongkong", "Hong Kong", "London", "Paris", "Moscow", "Sydney", "Rio", "Cairo"]
personname_list = ["Sue Law", "Julian Tyler", "Dave Wood", "Phil Lee", "Steve Young", "Robot Duke", "Shawn Smith", "Adrian Bryan", "Louise Plant", "Tom Wesley"]

monthname = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
cardinal1 = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
cardinal10 = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
cardinal20 = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
ordinal1 = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
ordinal10 = ["tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth"]
ordinal20 = ["twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"]

def gen_month():
	month = random.randint(1, 12)
	return monthname[month-1], ["month"], [("=", "DepartureTimeMonth", month)]

def gen_date():
	if random.randrange(2)==0:
		the_word = "the "
		the_tag = ["the"]
	else:
		the_word = ""
		the_tag = []

	date = random.randint(1, 31)
	if date < 10:
		return the_word + ordinal1[date-1], the_tag + ["B-date"], [("=", "DepartureTimeDate", date)]
	elif date < 20:
		return the_word + ordinal10[date-10], the_tag + ["B-date"], [("=", "DepartureTimeDate", date)]
	elif date%10 == 0:
		return the_word + ordinal20[(date-20)//10], the_tag + ["B-date"], [("=", "DepartureTimeDate", date)]
	else:
		return the_word + cardinal20[(date-20)//10] + " " + ordinal1[date%10-1], the_tag + ["B-date", "I-date"], [("=", "DepartureTimeDate", date)]

def gen_year():
	if random.randrange(2)==0:
		if random.randrange(2)==0:
			first_half = "two thousand and "
			first_half_tag = ["B-year", "I-year", "I-year"]
		else:
			first_half = "two thousand "
			first_half_tag = ["B-year", "I-year"]

		year_2_digit = random.randint(1, 40) # 2001 ~ 2040
		if year_2_digit < 10:
			return first_half + cardinal1[year_2_digit-1], first_half_tag + ["I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		elif year_2_digit < 20:
			return first_half + cardinal10[year_2_digit-10], first_half_tag + ["I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		elif year_2_digit%10 == 0:
			return first_half + cardinal20[(year_2_digit-20)//10], first_half_tag + ["I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		else:
			return first_half + cardinal20[(year_2_digit-20)//10] + " " + cardinal1[year_2_digit%10-1], first_half_tag + ["I-year", "I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
	else:
		first_half = "twenty "
		first_half_tag = ["B-year"]

		year_2_digit = random.randint(1, 40) # 2001 ~ 2040
		if year_2_digit < 10:
			return first_half + "oh " + cardinal1[year_2_digit-1], first_half_tag + ["I-year", "I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		elif year_2_digit < 20:
			return first_half + cardinal10[year_2_digit-10], first_half_tag + ["I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		elif year_2_digit%10 == 0:
			return first_half + cardinal20[(year_2_digit-20)//10], first_half_tag + ["I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]
		else:
			return first_half + cardinal20[(year_2_digit-20)//10] + " " + cardinal1[year_2_digit%10-1], first_half_tag + ["I-year", "I-year"], [("=", "DepartureTimeYear", 2000+year_2_digit)]

def gen_month_date_year():
	month, month_tag, month_info = gen_month()
	date, date_tag, date_info = gen_date()
	if random.randrange(2)==0:
		year, year_tag, year_info = gen_year()
		return month + " " + date + " " + year, month_tag + date_tag + year_tag, month_info + date_info + year_info
	else:
		return month + " " + date, month_tag + date_tag, month_info + date_info

def gen_city():
	city = random.choice(city_list)
	city_tag = ["B-city"]
	for i in range(len(city.split())-1):
		city_tag.append("I-city")
	return city, city_tag, [("=", "City", city.lower())]

def gen_city_origin():
	city, city_tag, city_info = gen_city()
	return city, [tag + "-ori" for tag in city_tag], [("=", "OriginCity", city.lower())]

def gen_city_destination():
	city, city_tag, city_info = gen_city()
	return city, [tag + "-des" for tag in city_tag], [("=", "DestinationCity", city.lower())]

def gen_time_outbound():
	time, time_tag, time_info = gen_month_date_year()
	return time, [tag + "-out" for tag in time_tag], [("=", "Out"+info_tuple[1], info_tuple[2]) for info_tuple in time_info]

def gen_time_return():
	time, time_tag, time_info = gen_month_date_year()
	return time, [tag + "-ret" for tag in time_tag], [("=", "Ret"+info_tuple[1], info_tuple[2]) for info_tuple in time_info]

def gen_personname():
	personname = random.choice(personname_list)
	personname_tag = ["B-personname"]
	for i in range(len(personname.split())-1):
		personname_tag.append("I-personname")
	return personname, personname_tag, [("=", "MyName", personname.lower())]

def gen_travel_class():
	travel_class = random.choice(["Economy", "Business", "First"])
	return travel_class.lower() + " class", ["B-class", "I-class"], [("=", "Class", travel_class)]

def gen_oneway_or_roundtrip():
	roundtrip = random.choice([False, True])
	if roundtrip == True:
		return "roundtrip", ["B-RoO"], [("=", "RoundTrip", "True")]
	else:
		return "one way trip", ["B-RoO", "I-RoO", "I-RoO"], [("=", "RoundTrip", "False")]

#--------------------------------------------------------------------

def gen_sentence1():
	sentence = "I want "
	tag = ["O", "O"]
	info = []

	choice = random.randrange(5)
	if choice==0:
		pass
	elif choice==1:
		sentence += "to buy "
		tag += ["O", "O"]
	elif choice==2:
		sentence += "to book "
		tag += ["O", "O"]
	elif choice==3:
		sentence += "to reserve "
		tag += ["O", "O"]
	elif choice==4:
		sentence += "to get "
		tag += ["O", "O"]

	choice = random.randrange(3)
	if choice==0:
		sentence += "a ticket "
		tag += ["O", "O"]
	elif choice==1:
		sentence += "an air ticket "
		tag += ["O", "O", "O"]
	elif choice==2:
		sentence += "a flight ticket "
		tag += ["O", "O", "O"]

	origin, origin_tag, origin_info = gen_city_origin()
	destination, destination_tag, destination_info = gen_city_destination()
	sentence += "from " + origin + " to " + destination
	tag += ["O"] + origin_tag + ["O"] + destination_tag
	info += origin_info + destination_info

	if random.randrange(2)==0:
		out_time, out_time_tag, out_time_info = gen_time_outbound()
		sentence += " departing on " + out_time
		tag += ["O", "O"] + out_time_tag
		info += out_time_info

	return sentence, tag, info

def gen_sentence2():
	sentence = random.choice(["Yes", "Yeah", "Right", "Correct", "Confirm"])
	tag = ["Yes"]
	info = [("True",)]
	
	return sentence, tag, info

def gen_sentence3():
	sentence = ""
	tag = []
	info = []

	if random.randrange(2)==0:
		sentence += "No "
		tag += ["No"]
		info += [("False",)]

	choice = random.randrange(6)
	if choice == 0:
		personname, personname_tag, personname_info = gen_personname()
		choice2 = random.randrange(3)
		if choice2 == 0:
			pass
		elif choice2 == 1:
			sentence += "My name is "
			tag += ["O", "O", "O"]
		else:
			sentence += "The name is "
			tag += ["O", "O", "O"]
		sentence += personname
		tag += personname_tag
		info += personname_info
	elif choice == 1:
		origin, origin_tag, origin_info = gen_city_origin()
		choice2 = random.randrange(4)
		if choice2 == 0:
			sentence += "The origin is "
			tag += ["O", "O", "O"]
		elif choice2 == 1:
			sentence += "My origin is "
			tag += ["O", "O", "O"]
		elif choice2 == 2:
			sentence += "The origin city is "
			tag += ["O", "O", "O", "O"]
		else:
			sentence += "My origin city is "
			tag += ["O", "O", "O", "O"]
		sentence += origin
		tag += origin_tag
		info += origin_info
	elif choice == 2:
		destination, destination_tag, destination_info = gen_city_destination()
		choice2 = random.randrange(4)
		if choice2 == 0:
			sentence += "The destination is "
			tag += ["O", "O", "O"]
		elif choice2 == 1:
			sentence += "My destination is "
			tag += ["O", "O", "O"]
		elif choice2 == 2:
			sentence += "The destination city is "
			tag += ["O", "O", "O", "O"]
		else:
			sentence += "My destination city is "
			tag += ["O", "O", "O", "O"]
		sentence += destination
		tag += destination_tag
		info += destination_info
	elif choice == 3:
		time, time_tag, time_info = gen_month_date_year()
		if random.randrange(2)==0:
			sentence += "On "
			tag += ["O"]
		sentence += time
		tag += time_tag
		info += time_info
	elif choice == 4:
		tclass, tclass_tag, tclass_info = gen_travel_class()
		if random.randrange(2)==0:
			sentence += "I want " + tclass
			tag += ["O", "O"] + tclass_tag
			info += tclass_info
		else:
			sentence += tclass.capitalize()
			tag += tclass_tag
			info += tclass_info
	elif choice == 5:
		RoO, RoO_tag, RoO_info = gen_oneway_or_roundtrip()
		if random.randrange(2)==0:
			sentence += "I want " + RoO
			tag += ["O", "O"] + RoO_tag
			info += RoO_info
		else:
			sentence += RoO.capitalize()
			tag += RoO_tag
			info += RoO_info

	return sentence, tag, info

def gen_sentence4():
	sentence = ""
	tag = []
	info = []

	if random.randrange(2)==0:
		sentence += "I want to change "
		tag += ["O", "O", "O", "O"]
	else:
		sentence += "Change "
		tag += ["O"]

	choice = random.randrange(7)
	if choice == 0:
		personname, personname_tag, personname_info = gen_personname()
		choice2 = random.randrange(2)
		if choice2 == 0:
			sentence += "my name to "
			tag += ["O", "O", "O"]
		else:
			sentence += "the name to "
			tag += ["O", "O", "O"]
		sentence += personname
		tag += personname_tag
		info += personname_info
	elif choice == 1:
		origin, origin_tag, origin_info = gen_city_origin()
		choice2 = random.randrange(2)
		if choice2 == 0:
			sentence += "the origin to "
			tag += ["O", "O", "O"]
		else:
			sentence += "the origin city to "
			tag += ["O", "O", "O", "O"]
		sentence += origin
		tag += origin_tag
		info += origin_info
	elif choice == 2:
		destination, destination_tag, destination_info = gen_city_destination()
		choice2 = random.randrange(2)
		if choice2 == 0:
			sentence += "the destination to "
			tag += ["O", "O", "O"]
		else:
			sentence += "the destination city to "
			tag += ["O", "O", "O", "O"]
		sentence += destination
		tag += destination_tag
		info += destination_info
	elif choice == 3:
		outtime, outtime_tag, outtime_info = gen_time_outbound()
		sentence += "the departure date to "
		tag += ["O", "O", "O", "O"]
		sentence += outtime
		tag += outtime_tag
		info += outtime_info
	elif choice == 4:
		rettime, rettime_tag, rettime_info = gen_time_return()
		sentence += "the return date to "
		tag += ["O", "O", "O", "O"]
		sentence += rettime
		tag += rettime_tag
		info += rettime_info
	elif choice == 5:
		tclass, tclass_tag, tclass_info = gen_travel_class()
		sentence += "the travel class to "
		tag += ["O", "O", "O", "O"]
		sentence += tclass
		tag += tclass_tag
		info += tclass_info
	elif choice == 6:
		RoO, RoO_tag, RoO_info = gen_oneway_or_roundtrip()
		sentence += "it to "
		tag += ["O", "O"]
		sentence += RoO
		tag += RoO_tag
		info += RoO_info

	return sentence, tag, info

def gen_sentence():
	choice = random.random()
	if choice < 0.3:
		sentence, tag, info = gen_sentence1()
	elif choice < 0.6:
		sentence, tag, info = gen_sentence3()
	elif choice < 0.9:
		sentence, tag, info = gen_sentence4()
	else:
		sentence, tag, info = gen_sentence2()

	if len(sentence.split()) != len(tag):
		exit("Internal Error. " + str(sentence, tag, info))

	return sentence.lower(), tag, info


if __name__ == "__main__":
	outfile_name = sys.argv[1]
	out_sentence_num = eval(sys.argv[2])
	if outfile_name != "stdout":
		outfile = open(outfile_name, "w")
		for i in range(out_sentence_num):
			outfile.write(str(gen_sentence()) + "\n")
	else:
		for i in range(out_sentence_num):
			print(str(gen_sentence()))

