
import pandas as pd
import os
import numpy
import wave


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


def extract_dataset(file):
	dog_tests = []
	cat_tests = []
	dog_train = []
	cat_train = []
	df = pd.read_csv(file)
	

def create_normalised_dataset():

	"""
	Takes the first 100000 frames of each wav file (pads u) and normalizes the data to between -1.0 and +1.0.
	Those normalized 100000 frames are then 
	"""

	directory = 'cats_dogs'
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

def create_fft_dataset():

	"""
	Displays data and some accompanying statistics
	"""

	directory = 'cats_dogs'
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


def store_created_dataset(dataset_function, directory):
	a = dataset_function()
	for array_element in a:
		np_array = array_element[0]
		filename = directory + '/' + array_element[1].split('.')[0] + '.txt'
		with open(filename, 'w') as file:
			for i in range(np_array.shape[0]):
				file.write(str(np_array[i]))
				file.write('\n')
		file.close()



if __name__ == "__main__":
	#main()
	#ad = pd.read_csv('audio_data.csv')
	#print(ad.head(3))
	store_created_dataset(create_fft_dataset, '100k_frames_fft_data')

	



