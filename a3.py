#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Abram Hindle <hindle1@ualberta.ca>, Leif Johnson <leif@lmjohns3.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# first off we load up some modules we want to use
import theanets
import scipy
import math
import numpy as np
import numpy.random as rnd
import logging
import sys
import collections
import theautil

# setup logging
logging.basicConfig(stream = sys.stderr, level=logging.INFO)

mupdates = 1000
data = np.loadtxt("winequality-red.csv",delimiter=";")
inputs  = data[0:,0:11].astype(np.float32)
outputs = data[0:,11:12].astype(np.int32)
for i in range(len(outputs)):
	if outputs[i]<=5:
		outputs[i]=0
	else:
		outputs[i]=1

theautil.joint_shuffle(inputs,outputs)

train_and_valid, test = theautil.split_validation(90, inputs, outputs)
train, valid = theautil.split_validation(90, train_and_valid[0], train_and_valid[1])

def linit(x):
    return x.reshape((len(x),))

train = (train[0],linit(train[1]))
valid = (valid[0],linit(valid[1]))
test  = (test[0] ,linit(test[1]))

########################################################################
# Part 3. Let's start using neural networks!
########################################################################

# try different combos here
archi=1;
print "Architecture 1: [11,15,15,15,2]"
print "Architecture 2: [11,30,30,30,2]"
print "Architecture 3: [11,30,30,30,30,30,30,2]"
archi = input('choose one of these three architecture(input 1, 2 or 3):')
if archi==2:
	architecture = '[11,30,30,30,2]'
	net = theanets.Classifier([11,30,30,30,2])
elif archi==3:
	architecture = '[11,30,30,30,30,30,30,2]'
	net = theanets.Classifier([11,30,30,30,30,30,30,2])
else:
	architecture = '[11,15,15,15,2]'
	net = theanets.Classifier([11,15,15,15,2])

net.train(train, valid, algo='layerwise', max_updates=mupdates, patience=1)
#net.train(train, valid, algo='rprop',     max_updates=mupdates, patience=1)
print architecture
print "Learner on the test set"
classify = net.classify(test[0])
print "%s / %s " % (sum(classify == test[1]),len(test[1]))
print collections.Counter(classify)
print theautil.classifications(classify,test[1])

