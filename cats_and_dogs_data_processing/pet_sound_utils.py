
import pandas as pd
import os
import numpy
import wave
import shutil

def write_data_to_csv(csv_file):

	"""
	writes data about the audio dataset to input csv file
	"""

	#code snippets used to make the audio data csv
	import csv
	with open(csv_file, 'w', newline='') as file:
		writer = csv.writer(file)
		field = ["#", "filename", "length"]
		writer.writerow(field)

		for filename in os.listdir('cats_dogs'):

			try:
				if os.path.isfile(directory +'/'+filename):
				
					# Read file to get buffer                                                                                               
					wav_file = wave.open(directory +'/'+filename)

					"""
					An audio frame, or sample, contains amplitude (loudness) information at that particular point in time.
					To produce sound, tens of thousands of frames are played in sequence to produce frequencies.
					"""

					samples = wav_file.getnframes()
					audio = wav_file.readframes(samples)


					# Convert buffer to float32 using NumPy                                                                                 
					audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
					audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

					writer.writerow([count, filename, audio_as_np_float32.shape[0]])
					count +=1
					sizes.append(audio_as_np_float32.shape[0])
					total_frames += audio_as_np_float32.shape[0]
					i += 1

					if audio_as_np_float32.shape[0] > max_size:
						max_size = audio_as_np_float32.shape[0]

			except wave.Error:
				print("This file raised a wave.Error error: ", filename)

	file.close()			
	return

def display_data():

	"""
	Displays data and some accompanying statistics
	"""

	i=0
	max_size = 0
	total_frames = 0
	sizes = []
	directory = 'cats_dogs'
	count = 0

	for filename in os.listdir('cats_dogs'):

		try:
			if os.path.isfile(directory +'/'+filename):
			
				# Read file to get buffer                                                                                               
				wav_file = wave.open(directory +'/'+filename)

				"""
				An audio frame, or sample, contains amplitude (loudness) information at that particular point in time.
				To produce sound, tens of thousands of frames are played in sequence to produce frequencies.
				"""

				samples = wav_file.getnframes()
				audio = wav_file.readframes(samples)

				# Convert buffer to float32 using NumPy                                                                                 
				audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
				audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

				print(count, "\t", filename, "\t", audio_as_np_float32.shape[0])
				count +=1
				sizes.append(audio_as_np_float32.shape[0])
				total_frames += audio_as_np_float32.shape[0]

				if audio_as_np_float32.shape[0] > max_size:
					max_size = audio_as_np_float32.shape[0]

		except wave.Error:
			print("This file raised a wave.Error error: ", filename)

	#statistics
	print("The maximum size is %d" %  (max_size))
	print("The average size is %.2f" % (total_frames/count))
	print("The standard deviation is %.2f" % (numpy.std(sizes)))
	print(total_frames)
	return


def create_normalised_dataset(directory = 'cats_dogs'):

	"""
	Takes the first 100000 frames of each wav file (pads u) and normalizes the data to between -1.0 and +1.0.
	Those normalized 100000 frames are then saved to a directory.

	Returns an array containing a tupleof the format: (numpy array, filename)

	"""

	arrays = []

	for filename in os.listdir('cats_dogs'):

		try:
			if os.path.isfile(directory +'/'+filename):
			
				# Read file to get buffer                                                                                               
				wav_file = wave.open(directory +'/'+filename)

				"""
				An audio frame, or sample, contains amplitude (loudness) information at that particular point in time.
				To produce sound, tens of thousands of frames are played in sequence to produce frequencies.
				"""

				samples = wav_file.getnframes()
				audio = wav_file.readframes(samples)


				# Convert buffer to float32 using NumPy                                                                                 
				audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
				audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

				# Normalise float32 array so that values are between -1.0 and +1.0                                                      
				max_int16 = 2**15
				audio_normalised = audio_as_np_float32 / max_int16


				#Pad data to 100000 elements
				if audio_normalised.shape[0] > 100000:
					audio_array = audio_normalised[0:100000]
					arrays.append((audio_array, filename))
				else:
					audio_array = numpy.zeros(100000)
					audio_array[:audio_normalised.shape[0]] = audio_normalised
					arrays.append((audio_array, filename))

		except wave.Error:
			pass

	return arrays

def create_fft_dataset(directory='cats_dogs'):

	"""
	Takes in a directory and converts all the wav files in it into numpy arrays before taking the fft of each array.
	If the array length is over 100k, only the first 100k elements are taken. If the length is under 100k elements,
	the array is padded to 100k elements. 

	Returns an array containing a tupleof the format: (numpy array, filename)

	"""

	arrays = []

	for filename in os.listdir(directory):

		try:
			if os.path.isfile(directory +'/'+filename):
			
				# Read file to get buffer                                                                                               
				wav_file = wave.open(directory +'/'+filename)

				"""
				An audio frame, or sample, contains amplitude (loudness) information at that particular point in time.
				To produce sound, tens of thousands of frames are played in sequence to produce frequencies.
				"""

				samples = wav_file.getnframes()
				audio = wav_file.readframes(samples)


				# Convert buffer to float32 using NumPy                                                                                 
				audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
				audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)


				"""
				May add this later

				# Normalise float32 array so that values are between -1.0 and +1.0                                                      
				max_int16 = 2**15
				audio_normalised = audio_as_np_float32 / max_int16
				"""


				audio_fft = numpy.fft.fft(audio_as_np_float32)

				#Pad data to 100000 elements
				if audio_fft.shape[0] > 100000:
					audio_array = audio_fft[0:100000]
					arrays.append((audio_array, filename))
				else:
					audio_array = numpy.zeros(100000)
					audio_array[:audio_fft.shape[0]] = audio_fft
					arrays.append((audio_array, filename))

		except wave.Error:
			pass

	return arrays

def format_numpy_complex_num(complex_num):
	"""
	very sorry for the long and complex code. This function is meant to take in 
	a complex number as a string and returns a formated version for storage 
	'(414473.2018680698-168195.3641957787j)' -> '414473.2018680698, -168195.3641957787'
				 actual output	 ->  414473.2018680698, -168195.3641957787
	it is needed because this data will later be read  into a c++ complex data type 
	variable which has real and imaginary parts. There is an easier way to do this (i.e with a lexer or parser)
	The input numbers are from a numpy array and they come in multiple forms.
	"""
	a = complex_num
	d = []
	a_minus = a.split('-')
	a_plus = a.split('+')

	if (len(a_minus) == 2) and (a_minus[0] == ''): #this type of variable -148191
	#	print(1)
		return a + ', 0'

	elif ( (len(a_minus) == 1)  and (len(a_plus) == 1) ): #this type of variable 148191
	#	print(2)
		return a + ', 0'

	elif ( (len(a_minus) == 2 and a[1:-1].split('-')[0] == '') and len(a_minus[1].split('+')) > 1): #this type of variable(-148191+0j)
		d = a[1:-1].split('+')
	#	print(3)
		return d[0] + ', ' + d[1][:-1]

	elif (len(a_plus) == 2 and len(a_minus) == 1) : #this type of variable (27356+0j)
	#	print(4)
		return a_plus[0][1:] + ', ' + a_plus[1][:-2]

	elif (a[-6] == 'e') :
		if len(a[1:-6].split('-')) > 2: # this type of variable (-8576.999999999534-1.8189894035458565e-12j)
			divider = int(a[-4:-2])-1
			c = a[1:-6].split('-')
			zeroes = ''
			for i in range(divider):
				zeroes += '0'
	#		print(5)
			return c[1] + ', ' + '0.' + zeroes + c[2][0]

		elif len(a[1:-6].split('-')) == 2: # this type of variable (8480.99999999997-9.458744898438454e-11j)
			divider = int(a[-4:-2])-1
			c = a[1:-6].split('-')
			zeroes = ''
			for i in range(divider):
				zeroes += '0'
	#		print(6)
			return c[0] + ', ' + '-0.' + zeroes + c[1][0] 

		else:
			#this type of variable (115777760.99999999+4.474713932722807e-09j):
			divider = int(a[-4:-2])-1
			c = a[1:-6].split('+')
			zeroes = ''
			for i in range(divider):
				zeroes += '0'
	#		print(7)
			return c[0] + ', ' + '0.' + zeroes + c[1][0]

	else:

		b = a[1:-1] 
		temp = ''
		var = ''

		if b[0] == '-':
			temp = b[1:].split('+')
			if len(temp) == 1:
				var = b.split('-')
	#			print(8)
				return '-' + var[1] + ', -' + var[2][:-1]
		else:
			temp = b.split('+')
			if len(temp) == 1:
				var = b.split('-')
	#			print(9)
				return var[0] + ', -' + var[1][:-1]


	
def store_created_dataset(dataset_function, save_directory, store_complex=0):

	"""
	Takes in a function like create_fft_dataset or create_normalised_dataset and stores the numpy array in each list element in the correct file.
	The data set functions should return list of the following format:

	a list containing  tuples of the format: (numpy array, filename)

	NOTE: If you want to store variables as complex numbers with real and imaginary parts (real, imaginary) comma delimited set store_complex=true;
	"""

	a = dataset_function()
	for array_element in a:

		#array element format (numpy array, filename)
		np_array = array_element[0]

		#this line accesses each array element's filename and adds a path to save_directory while also replacing the .wav with a .txt extension

		filename = save_directory + '/' + array_element[1].split('.')[0] + '.txt'
		with open(filename, 'w') as file:
			for i in range(np_array.shape[0]):
				try:
					if store_complex:
						file.write(format_numpy_complex_num(str(np_array[i])))
					else:
						file.write(str(np_array[i]))
					file.write('\n')

				except (IndexError, TypeError) as error:
					print(str(np_array[i]) , end=': ')
					print(error)
					break

		file.close()
	return

def create_test_train_split(csv_file, data_directory):

	"""
	takes in a csv_file conttaining the testing and training splits of the files in the data directory.

	The following setup is needed for the classification to work
	 -data_directory
	|
	|-files
	|-test
	|-------|-cats
	|-------|-dogs
	|-train
	|-------|-cats
	|-------|-dogs
	

	"""
	df = pd.read_csv(csv_file)

	test_cat_file = ''
	test_dog_file = ''
	train_cat_file = ''
	train_dog_file = ''



	for i in df.index:
		test_cat_file = df['test_cat'][i]

		if pd.isna(test_cat_file):
			pass
		else:
			src_path = data_directory + "/" + test_cat_file.split('.')[0] + '.txt'
			dest_path =data_directory + "/test/cats/" + test_cat_file.split('.')[0] + '.txt'

			if not os.path.exists(dest_path):
				fp = open(dest_path, 'x')
				fp.close()

			shutil.copy(src_path, dest_path)

		test_dog_file = df['test_dog'][i]

		if pd.isna(test_dog_file):
				pass
		else:
			src_path = data_directory + "/" + test_dog_file.split('.')[0] + '.txt'
			dest_path =data_directory + "/test/dogs/" + test_dog_file.split('.')[0] + '.txt'

			if not os.path.exists(dest_path):
				fp = open(dest_path, 'x')
				fp.close()

			shutil.copy(src_path, dest_path)

		train_cat_file = df['train_cat'][i]

		if pd.isna(train_cat_file):
			pass
		else:
			src_path = data_directory + "/" + train_cat_file.split('.')[0] + '.txt'
			dest_path = data_directory + "/train/cats/" + train_cat_file.split('.')[0] + '.txt'

			if not os.path.exists(dest_path):
				fp = open(dest_path, 'x')
				fp.close()

			shutil.copy(src_path, dest_path)


		train_dog_file = df['train_dog'][i]

		if pd.isna(train_dog_file):
			pass
		else:
			src_path = data_directory + "/" + train_dog_file.split('.')[0] + '.txt'
			dest_path = data_directory + "/train/dogs/" + train_dog_file.split('.')[0] + '.txt'

			if not os.path.exists(dest_path):
				fp = open(dest_path, 'x')
				fp.close()

			shutil.copy(src_path, dest_path)


def format_numpy_nums_in_file(filename):
	"""
	Reads through the lines in a file and if they end with an exponent, formats the data to a c++ readable version
	i.e. -6.1035156e-05 ->  -0.000061035156
	"""

	file_lines = []
	temp = ''
	divider = 0

	with open(filename, 'r') as file:
		lines = file.readlines()
		for line in lines:
			#NOTE: Each line ends with an escape character "\n"
			if (len(line) >= 5) and (line[-5] == 'e'): 
				divider = int(line[-3:-1])
				if line[0] == '-':
					temp = line[1:-5]
					parts = temp.split('.')
					zeros = ''
					result_num = ''
					for i in range(divider-1):
						zeros += '0'
					result_num = '-0.' + zeros + parts[0] + parts[1]
					file_lines.append(result_num)
				else:
					temp = line[:-5]
					parts = temp.split('.')
					zeros = ''
					for i in range(divider-1):
						zeros += '0'
					result_num = '-0.' + zeros + parts[0] + parts[1]
					file_lines.append(result_num)
			else:
				file_lines.append(line[:-1])
	file.close

	with open(filename, 'w') as file:
		for i in range(len(file_lines)):
			file.write(file_lines[i])
			file.write('\n')
	file.close()

	return



if __name__ == "__main__":
	#main()
	#ad = pd.read_csv('audio_data.csv')
	#print(ad.head(3))
	#store_created_dataset(create_fft_dataset, '100k_frames_fft_data', 1)
	#print(format_numpy_complex_num('(-142115.5487254858+20712.812030166184j)'))
	create_test_train_split('train_test_split.csv', '100k_frames_normalised_data')
	"""
	for filename in os.listdir('100k_frames_normalised_data'):

		if filename == '.DS_Store':
			pass
		else:
			cur_path = os.path.dirname(__file__)
			file_path = os.path.relpath(os.path.join('100k_frames_normalised_data', filename), cur_path)
			if os.path.isfile(file_path):
				format_numpy_nums_in_file(file_path)
	"""
	
