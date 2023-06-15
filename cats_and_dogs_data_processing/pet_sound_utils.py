
import pandas as pd
import os
import numpy
import wave


def display_data():
	#extract_dataset('train_test_split.csv')
	i=0
	max_size = 0
	total_frames = 0
	sizes = []
	directory = 'cats_dogs'
	count = 0
	"""
		#code snippets used to make the audio data csv
		import csv
		with open('audio_data.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			field = ["#", "filename", "length"]
			writer.writerow(field)
			writer.writerow([count, filename, audio_as_np_float32.shape[0]])
		file.close()			
	"""
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
				i += 1

				if audio_as_np_float32.shape[0] > max_size:
					max_size = audio_as_np_float32.shape[0]

		except wave.Error:
			print("This file raised a wave.Error error: ", filename)

	#statistics
	print("The maximum size is %d" %  (max_size))
	print("The average size is %.2f" % (total_frames/count))
	print("The standard deviation is %.2f" % (numpy.std(sizes)))
	print(total_frames)

	"""
		# Normalise float32 array so that values are between -1.0 and +1.0                                                      
		max_int16 = 2**15
		audio_normalised = audio_as_np_float32 / max_int16
	"""

def extract_dataset(file):
	dog_tests = []
	cat_tests = []
	dog_train = []
	cat_train = []
	df = pd.read_csv(file)
	




if __name__ == "__main__":
	#main()
	ad = pd.read_csv('audio_data.csv')
	print(ad.head(3))

