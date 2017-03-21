# I added the color to the already existing chords dictionary based on www.flutopedia.com/sound_color.htm
# Since the chart is based on frequencies and here I'm working with chords, I decided to reduce the saturation for the minor chords
# Added the return

"""
Pitch functions
- Chroma
Last updated: 15 December 2012
"""
from __future__ import division

import math

import numpy

# Dictionary of major and minor chords
chords = [ {'name': "C", 'vector' :[1,0,0,0,1,0,0,1,0,0,0,0], 'key': 0, 'mode': 1, 'color': "rgb(40, 255, 0)" },
			{'name': "Cm", 'vector':[1,0,0,1,0,0,0,1,0,0,0,0], 'key': 0, 'mode': 0, 'color': "rgb(184, 255, 171)" },
			{'name': "C#", 'vector' :[0,1,0,0,0,1,0,0,1,0,0,0], 'key': 1, 'mode': 1, 'color': "rgb(0, 255, 232)" },
			{'name': "C#m", 'vector':[0,1,0,0,1,0,0,0,1,0,0,0], 'key': 1, 'mode': 0, 'color': "rgb(173, 254, 246)" },
			{'name': "D", 'vector' :[0,0,1,0,0,0,1,0,0,1,0,0],  'key': 2, 'mode': 1, 'color': "rgb(0, 124, 255)" },
			{'name': "Dm", 'vector':[0,0,1,0,0,1,0,0,0,1,0,0],  'key': 2, 'mode': 0, 'color': "rgb(145, 200, 255)" },
			{'name': "Eb", 'vector' :[0,0,0,1,0,0,0,1,0,0,1,0],  'key': 3, 'mode': 1, 'color': "rgb(5, 0, 255)" },
			{'name': "Ebm", 'vector':[0,0,0,1,0,0,1,0,0,0,1,0],  'key': 3, 'mode': 0, 'color': "rgb(171, 170, 255)" },
			{'name': "E", 'vector' :[0,0,0,0,1,0,0,0,1,0,0,1],  'key': 4, 'mode': 1, 'color': "rgb(69, 0, 234)" },
			{'name': "Em", 'vector':[0,0,0,0,1,0,0,1,0,0,0,1],  'key': 4, 'mode': 0, 'color': "rgb(196, 173, 255)" },
			{'name': "F", 'vector' :[1,0,0,0,0,1,0,0,0,1,0,0],  'key': 5, 'mode': 1, 'color': "rgb(87, 0, 158)" },
			{'name': "Fm", 'vector':[1,0,0,0,0,1,0,0,1,0,0,0],  'key': 5, 'mode': 0, 'color': "rgb(255, 170, 170)" },
			{'name': "F#", 'vector' :[0,1,0,0,0,0,1,0,0,0,1,0],  'key': 6, 'mode': 1, 'color': "rgb(116, 0, 0)" },
			{'name': "F#m", 'vector':[0,1,0,0,0,0,1,0,0,1,0,0],  'key': 6, 'mode': 0, 'color': "rgb(116, 0, 0)" },
			{'name': "G", 'vector' :[0,0,1,0,0,0,0,1,0,0,0,1],  'key': 7, 'mode': 1, 'color': "rgb(179, 0, 0)" },
			{'name': "Gm", 'vector':[0,0,1,0,0,0,0,1,0,0,1,0],  'key': 7, 'mode': 0, 'color': "rgb(187, 0, 0)" },
			{'name': "Ab", 'vector' :[1,0,0,1,0,0,0,0,1,0,0,0],  'key': 8, 'mode': 1, 'color': "rgb(238, 0, 0)" },
			{'name': "Abm", 'vector':[0,0,0,1,0,0,0,0,1,0,0,1],  'key': 8, 'mode': 0, 'color': "rgb(238, 0, 0)" },
			{'name': "A", 'vector' :[0,1,0,0,1,0,0,0,0,1,0,0],  'key': 9, 'mode': 1, 'color': "rgb(255, 99, 0)" },
			{'name': "Am", 'vector':[1,0,0,0,1,0,0,0,0,1,0,0],  'key': 9, 'mode': 0, 'color': "rgb(255, 187, 143)" },
			{'name': "Bb", 'vector' :[0,0,1,0,0,1,0,0,0,0,1,0],  'key': 10, 'mode': 1, 'color': "rgb(255, 236, 0)" },
			{'name': "Bbm", 'vector':[0,1,0,0,0,1,0,0,0,0,1,0],  'key': 10, 'mode': 0, 'color': "rgb(255, 245, 120)" },
			{'name': "B", 'vector' :[0,0,0,1,0,0,1,0,0,0,0,1],  'key': 11, 'mode': 1, 'color': "rgb(153, 255, 0)" },
			{'name': "Bm", 'vector':[0,0,1,0,0,0,1,0,0,0,0,1],  'key': 11, 'mode': 0, 'color': "rgb(163, 255, 23)" }]

def chroma(spectrum):
	"""
	Compute the 12-ET chroma vector from this spectrum
	"""
	chroma = [0] * 12
	for index in range(0, len(spectrum)):

		# Assign a frequency value to each bin
		f = index * (spectrum.sampleRate / 2.0) / len(spectrum)

		# Convert frequency to pitch to pitch class
		if f != 0:
			pitch = frequencyToMidi(f)
		else:
			pitch = 0
		pitchClass = pitch % 12

		chroma[pitchClass] = chroma[pitchClass] + abs(spectrum[index])

	# Normalize the chroma vector
	maxElement = max(chroma)
	chroma = [c / maxElement for c in chroma]

	return chroma

def cosineSimilarity(a, b):
	"""
	Compute the similarity between two vectors using the cosine similarity metric
	"""
	dotProduct = 0
	aMagnitude = 0
	bMagnitude = 0
	for i in range(len(a)):
		dotProduct += (a[i] * b[i])
		aMagnitude += math.pow(a[i], 2)
		bMagnitude += math.pow(b[i], 2)

	aMagnitude = math.sqrt(aMagnitude)
	bMagnitude = math.sqrt(bMagnitude)

	return dotProduct / (aMagnitude * bMagnitude)

def frequencyToMidi(frequency):
	"""
	Convert a given frequency in Hertz to its corresponding MIDI pitch number (60 = Middle C)
	"""
	return int(round(69 + 12 * math.log(frequency / 440.0, 2)))

def getChord(chroma):
	"""
	Given a chroma vector, return the best chord match using naive dictionary-based method
	"""
	maxScore = 0
	chordName = ""
	chordColor = ""
	chordMode = ""
	for chord in chords:
		score = cosineSimilarity(chroma, chord['vector'])
		if score > maxScore:
			maxScore = score
			chordName = chord['name']
			chordColor = chord['color']
			chordMode = chord['mode']

	return chordName, chordColor, chordMode

def naivePitch(spectrum):
	"""
	Compute the pitch by using the naive pitch estimation method, i.e. get the pitch name for the most
	prominent frequency.
	Only returns MIDI pitch number
	"""
	maxFrequencyIndex = numpy.argmax(spectrum)
	maxFrequency = maxFrequencyIndex * (spectrum.sampleRate / 2.0) / len(spectrum)
	return frequencyToMidi(maxFrequency)
