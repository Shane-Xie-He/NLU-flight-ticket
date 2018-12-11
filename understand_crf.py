#!/usr/bin/env python3

import pycrfsuite
import sys

monthname = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
cardinal1 = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
cardinal10 = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
cardinal20 = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
ordinal1 = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
ordinal10 = ["tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth"]
ordinal20 = ["twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"]

#--------------------CRF------------------------

def calc_distance(word_list, i, target_word):
	j = 0
	while True:
		if not (i-j >= 0 or i+j < len(word_list)):
			return 100 # indicating a very long distance (infinity)
		if i-j >= 0:
			if word_list[i-j] == target_word:
				return j
		if i+j < len(word_list):
			if word_list[i+j] == target_word:
				return j
		j += 1

def crf_extract_feature_sequence(utterance):
	word_list = utterance.split()
	feature_sequence = []
	for i in range(len(word_list)):
		features = {}
		features["Word"] = word_list[i]
		if i-1 >= 0:
			features["-1:Word"] = word_list[i-1]
		else:
			features["First_word"] = True
		if i+1 < len(word_list):
			features["+1:Word"] = word_list[i+1]
		else:
			features["Last_word"] = True
		features["Distance_departure"] = calc_distance(word_list, i, "departure")
		features["Distance_return"] = calc_distance(word_list, i, "return")
		features["Distance_origin"] = calc_distance(word_list, i, "origin")
		features["Distance_destination"] = calc_distance(word_list, i, "destination")
		features["Distance_from"] = calc_distance(word_list, i, "from")
		features["Distance_to"] = calc_distance(word_list, i, "to")
		features["Distance_beg"] = i
		features["Distance_end"] = len(word_list)-1-i
		if word_list[i].capitalize() in monthname:
			features["Monthname"] = True
		if word_list[i].lower() in cardinal1:
			features["Cardinal1"] = True
		if word_list[i].lower() in cardinal10:
			features["Cardinal10"] = True
		if word_list[i].lower() in cardinal20:
			features["Cardinal20"] = True
		if word_list[i].lower() in ordinal1:
			features["Ordinal1"] = True
		if word_list[i].lower() in ordinal10:
			features["Ordinal10"] = True
		if word_list[i].lower() in ordinal20:
			features["Ordinal20"] = True
		feature_sequence.append(features)
	return feature_sequence

def crf_train(train_filename):
	train_file = open(train_filename, "r")

	trainer = pycrfsuite.Trainer(verbose=False)

	line = train_file.readline()
	while line != "":
		sentence, tag, info = eval(line)
		feature_sequence = crf_extract_feature_sequence(sentence)
		trainer.append(feature_sequence, tag)
		line = train_file.readline()

	trainer.set_params({
		'c1': 1.0,   # coefficient for L1 penalty
		'c2': 1e-3,  # coefficient for L2 penalty
		'max_iterations': 100,  # stop earlier

		# include transitions that are possible, but not observed
		'feature.possible_transitions': True
	})

	trainer.train("model")

def crf_predict(utterance):
	tagger = pycrfsuite.Tagger()
	tagger.open("model")
	feature_sequence = crf_extract_feature_sequence(utterance)
	predicted_tag_sequence = tagger.tag(feature_sequence)
	if len(predicted_tag_sequence) != len(utterance.split()):
		sys.exit("Error. Number of predicted tags doesn't match the utterance.")
	return predicted_tag_sequence

def crf_test(test_filename):
	test_file = open(test_filename, "r")

	count_all = 0
	count_correct = 0
	label_count_correct = {}
	label_count_predicted = {}
	label_count_actual = {}
	utterance_correct = 0
	utterance_all = 0

	line = test_file.readline()
	while line != "":
		utterance, tag, info = eval(line)
		predicted_tag = crf_predict(utterance)
		if len(predicted_tag) != len(tag):
			sys.exit("Error. Number of tags doesn't match.")
		if predicted_tag == tag:
			utterance_correct += 1
		#else:
		#	print("Falsely predicted utterance: " + utterance)
		#	print("Actual tag:    " + str(tag))
		#	print("Predicted tag: " + str(predicted_tag))
		utterance_all += 1
		for i in range(len(tag)):
			if predicted_tag[i] == tag[i]:
				count_correct += 1
				if predicted_tag[i] in label_count_correct:
					label_count_correct[predicted_tag[i]] += 1
				else:
					label_count_correct[predicted_tag[i]] = 1
			count_all += 1
			if predicted_tag[i] in label_count_predicted:
				label_count_predicted[predicted_tag[i]] += 1
			else:
				label_count_predicted[predicted_tag[i]] = 1
			if tag[i] in label_count_actual:
				label_count_actual[tag[i]] += 1
			else:
				label_count_actual[tag[i]] = 1

		line = test_file.readline()

	print("Whole utterance accuracy: " + str(utterance_correct / utterance_all))
	print("Overall labeling accuracy: " + str(count_correct / count_all))
	print("label_count_correct: " + str(label_count_correct))
	print("label_count_predicted: " + str(label_count_predicted))
	print("label_count_actual: " + str(label_count_actual))
	all_labels = list(set(label_count_predicted) | set(label_count_actual))
	all_labels.sort()
	for label in all_labels:
		if label in label_count_correct:
			print("Accuracy = " + "{:.4f}".format(label_count_correct[label] / label_count_predicted[label]) + ", Recall = " + "{:.4f}".format(label_count_correct[label] / label_count_actual[label]) + " for " + label)
		elif label in label_count_predicted:
			if label in label_count_actual:
				print("Accuracy = 0.0000, Recall = 0.0000 for " + label)
			else:
				print("Accuracy = 0.0000, Recall = NA     for " + label)
		else:
			print("Accuracy = NA    , Recall = 0.0000 for " + label)

#------------------------- Understanding -----------------------------

def read_month(words):
	if len(words)==1 and words[0].capitalize() in monthname:
		return monthname.index(words[0].capitalize())+1
	return None

def read_date(words):
	if len(words)==2 and words[0] in cardinal20 and words[1] in ordinal1:
		return cardinal20.index(words[0])*10+20 + ordinal1.index(words[1])+1
	if len(words)==1 and words[0] in ordinal20:
		return ordinal20.index(words[0])*10+20
	if len(words)==1 and words[0] in ordinal1+ordinal10:
		return (ordinal1+ordinal10).index(words[0])+1
	return None

def read_year(words):
	if len(words)==5 and words[0:3]==["two", "thousand", "and"] and words[3] in cardinal20 and words[4] in cardinal1:
		return 2000 + cardinal20.index(words[3])*10+20 + cardinal1.index(words[4])+1
	if len(words)==4 and words[0:3]==["two", "thousand", "and"] and words[3] in cardinal20:
		return 2000 + cardinal20.index(words[3])*10+20
	if len(words)==4 and words[0:3]==["two", "thousand", "and"] and words[3] in cardinal1+cardinal10:
		return 2000 + (cardinal1+cardinal10).index(words[3])+1
	if len(words)==4 and words[0:2]==["two", "thousand"] and words[2] in cardinal20 and words[3] in cardinal1:
		return 2000 + cardinal20.index(words[2])*10+20 + cardinal1.index(words[3])+1
	if len(words)==3 and words[0:2]==["two", "thousand"] and words[2] in cardinal20:
		return 2000 + cardinal20.index(words[2])*10+20
	if len(words)==3 and words[0:2]==["two", "thousand"] and words[2] in cardinal1+cardinal10:
		return 2000 + (cardinal1+cardinal10).index(words[2])+1
	if words[0] == "twenty": # Possibly a year number
		if len(words)==3 and words[1] in cardinal20 and words[2] in cardinal1:
			return 2000 + cardinal20.index(words[1])*10+20 + cardinal1.index(words[2])+1
		if len(words)==2 and words[1] in cardinal20:
			return 2000 + cardinal20.index(words[1])*10+20
		if len(words)==2 and words[1] in cardinal10:
			return 2000 + cardinal10.index(words[1])+10
		if len(words)==3 and words[1]=="oh" and words[2] in cardinal1:
			return 2000 + cardinal1.index(words[2])+1
	return None

def read_chunk(i, words, tags):
	if tags[i][0:2] == "B-":
		chunk_name = tags[i][2:]
		chunk_words = [words[i]]
		for j in range(i+1, len(tags)):
			if tags[j] != "I-" + chunk_name:
				break
			chunk_words.append(words[j])
		return chunk_words
	else:
		return [words[i]]

def understand(utterance):
	utterance = utterance.lower()
	words = utterance.split()
	tags = crf_predict(utterance)
	if len(tags) != len(words):
		sys.exit("Error. Number of tags doesn't match number of words.")
	info = []

	for i in range(len(tags)):
		if tags[i] == "Yes":
			info.append(("True",))
			continue
		if tags[i] == "No":
			info.append(("False",))
			continue

		if tags[i] == "B-class":
			class_words = read_chunk(i, words, tags)
			if "economy" in class_words:
				info.append(("=", "Class", "Economy"))
			elif "business" in class_words:
				info.append(("=", "Class", "Business"))
			elif "first" in class_words:
				info.append(("=", "Class", "First"))
			continue

		if tags[i] == "B-RoO":
			RoO_words = read_chunk(i, words, tags)
			if "roundtrip" in RoO_words:
				info.append(("=", "RoundTrip", "True"))
			elif "one way" in " ".join(RoO_words):
				info.append(("=", "RoundTrip", "False"))
			continue

		if tags[i] == "month-out":
			month = read_month([words[i]])
			if month != None:
				info.append(("=", "OutDepartureTimeMonth", month))
			continue
		if tags[i] == "month-ret":
			month = read_month([words[i]])
			if month != None:
				info.append(("=", "RetDepartureTimeMonth", month))
			continue
		if tags[i] == "month":
			month = read_month([words[i]])
			if month != None:
				info.append(("=", "DepartureTimeMonth", month))
			continue
		if tags[i] == "B-date-out":
			date_words = read_chunk(i, words, tags)
			date = read_date(date_words)
			if date != None:
				info.append(("=", "OutDepartureTimeDate", date))
			continue
		if tags[i] == "B-date-ret":
			date_words = read_chunk(i, words, tags)
			date = read_date(date_words)
			if date != None:
				info.append(("=", "RetDepartureTimeDate", date))
			continue
		if tags[i] == "B-date":
			date_words = read_chunk(i, words, tags)
			date = read_date(date_words)
			if date != None:
				info.append(("=", "DepartureTimeDate", date))
			continue
		if tags[i] == "B-year-out":
			year_words = read_chunk(i, words, tags)
			year = read_year(year_words)
			if year != None:
				info.append(("=", "OutDepartureTimeYear", year))
			continue
		if tags[i] == "B-year-ret":
			year_words = read_chunk(i, words, tags)
			year = read_year(year_words)
			if year != None:
				info.append(("=", "RetDepartureTimeYear", year))
			continue
		if tags[i] == "B-year":
			year_words = read_chunk(i, words, tags)
			year = read_year(year_words)
			if year != None:
				info.append(("=", "DepartureTimeYear", year))
			continue

		if tags[i] == "B-personname":
			personname_words = read_chunk(i, words, tags)
			personname = " ".join(personname_words)
			info.append(("=", "MyName", personname))
			continue

		if tags[i] == "B-city-ori":
			city_words = read_chunk(i, words, tags)
			city = " ".join(city_words)
			info.append(("=", "OriginCity", city))
			continue
		if tags[i] == "B-city-des":
			city_words = read_chunk(i, words, tags)
			city = " ".join(city_words)
			info.append(("=", "DestinationCity", city))
			continue
		if tags[i] == "B-city":
			city_words = read_chunk(i, words, tags)
			city = " ".join(city_words)
			info.append(("=", "City", city))
			continue

	return info

#----------------------- Test understanding ----------------------------

def infotype_counter(info, infotype_count):
	for info_tuple in info:
		if len(info_tuple) == 1:
			if info_tuple[0] in infotype_count:
				infotype_count[info_tuple[0]] += 1
			else:
				infotype_count[info_tuple[0]] = 1
		elif len(info_tuple) == 3 and info_tuple[0] == "=":
			if "=" + info_tuple[1] in infotype_count:
				infotype_count["=" + info_tuple[1]] += 1
			else:
				infotype_count["=" + info_tuple[1]] = 1
		else:
			sys.exit("info_tuple not recognized.")

def understand_test(test_filename):
	test_file = open(test_filename, "r")

	count_correct = 0
	count_predicted = 0
	count_actual = 0
	infotype_count_correct = {}
	infotype_count_predicted = {}
	infotype_count_actual = {}
	utterance_correct_count = 0
	utterance_all_count = 0

	line = test_file.readline()
	while line != "":
		utterance, tag, info = eval(line)
		if len(info) != len(set(info)):
			sys.exit("Error. There are duplicate actual info tuples.")
		predicted_info = understand(utterance)

		if set(info) == set(predicted_info):
			utterance_correct_count += 1
		#else:
		#	print("Falsely predicted utterance: " + utterance)
		#	print("Actual Info:    " + str(info))
		#	print("Predicted info: " + str(predicted_info))
		utterance_all_count += 1

		correct_info = list(set(info) & set(predicted_info)) # Since info can't have duplicates, correct_info can't have duplicates too. So it's legitimate to generate correct_info this way.

		count_correct += len(correct_info)
		infotype_counter(correct_info, infotype_count_correct)
		count_predicted += len(predicted_info)
		infotype_counter(predicted_info, infotype_count_predicted)
		count_actual += len(info)
		infotype_counter(info, infotype_count_actual)

		line = test_file.readline()

	print("Whole utterance accuracy: " + str(utterance_correct_count / utterance_all_count))
	print("Overall info accuracy: " + str(count_correct / count_predicted))
	print("Overall info recall: " + str(count_correct / count_actual))
	print("infotype_count_correct: " + str(infotype_count_correct))
	print("infotype_count_predicted: " + str(infotype_count_predicted))
	print("infotype_count_actual: " + str(infotype_count_actual))
	if not set(infotype_count_correct) <= set(infotype_count_predicted) | set(infotype_count_actual):
		sys.exit("Internal error. The keys in infotype_count_correct is not a subset of the keys in infotype_count_predicted and infotype_count_actual.")
	all_infotypes = list(set(infotype_count_predicted) | set(infotype_count_actual))
	all_infotypes.sort()
	for infotype in all_infotypes:
		if infotype in infotype_count_correct:
			print("Accuracy = " + "{:.4f}".format(infotype_count_correct[infotype] / infotype_count_predicted[infotype]) + ", Recall = " + "{:.4f}".format(infotype_count_correct[infotype] / infotype_count_actual[infotype]) + " for " + infotype)
		elif infotype in infotype_count_predicted:
			if infotype in infotype_count_actual:
				print("Accuracy = 0.0000, Recall = 0.0000 for " + infotype)
			else:
				print("Accuracy = 0.0000, Recall = NA     for " + infotype)
		else:
			print("Accuracy = NA    , Recall = 0.0000 for " + infotype)


#---------------------------------------------------------------------

if __name__ == "__main__":
	if sys.argv[1] == "crf-train":
		crf_train(sys.argv[2])
	elif sys.argv[1] == "crf-predict":
		utterance = input()
		print(crf_predict(utterance))
	elif sys.argv[1] == "crf-test":
		crf_test(sys.argv[2])
	elif sys.argv[1] == "und-predict":
		utterance = input()
		print(crf_predict(utterance))
		print(understand(utterance))
	elif sys.argv[1] == "und-test":
		understand_test(sys.argv[2])

