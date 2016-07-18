import os
import numpy as np
import sys
if os.getcwd() == '/home/keeda/Documents/scientist/demo/cv/scientist_demoes/objectrecognition':
    caffe_root = '/home/keeda/caffe/'
    serverPath = "/home/keeda/Documents/scientist/demo/cv/scientist_demoes/"
    mypath ='/home/keeda/Documents/scientist/demo/cv/scientist_demoes/media/documents/'
else:
    caffe_root = '/home/ubuntu/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
    serverPath = "/home/ubuntu/scientist_demoes/"
    mypath ='/home/ubuntu/scientist_demoes/media/documents/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import os
from subprocess import call
import ipdb
import json
import re

if os.path.isfile(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
    print 'CaffeNet found.'
else:
    print 'Downloading pre-trained CaffeNet model...'
    call(['python',caffe_root+'scripts/download_model_binary.py', caffe_root+'models/bvlc_reference_caffenet'])


# ### 2. Load net and set up input preprocessing

caffe.set_mode_cpu()

model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)



# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values


# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR


# classification
# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227

# load ImageNet labels
labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'

if not os.path.exists(labels_file):
    call(['python',caffe_root+'data/ilsvrc12/get_ilsvrc_aux.sh'])


labels = np.loadtxt(labels_file, str, delimiter='\t')

# * Load an image (that comes with Caffe) and perform the preprocessing we've set up.

# In[91]:
while(True):
    userInput = raw_input('enter "run" to predict: ')
    if userInput=="run":
        mypath = mypath
        logdir=mypath# path to your log directory
        logfiles = sorted([ f for f in os.listdir(logdir)])
        fileswpath = [mypath+logfile for logfile in logfiles]
        fileswpath.sort(key=lambda x: os.path.getmtime(x))
        print "Most recent file = %s" % (fileswpath[-1],)
        #image = caffe.io.load_image(caffe_root + 'examples/images/test.jpg')
        image = caffe.io.load_image(fileswpath[-1])
        transformed_image = transformer.preprocess('data', image)
        
        # copy the image data into the memory allocated for the net
        net.blobs['data'].data[...] = transformed_image
        
        ### perform classification
        output = net.forward()
        
        output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
        
        print 'predicted class is:', output_prob.argmax()
        print 'output label:', labels[output_prob.argmax()]
        
        
        # sort top five predictions from softmax output
        top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take five largest items
        
        print 'probabilities and labels:'
        #ipdb.set_trace()
        print(labels[top_inds])
        result = labels[top_inds].tolist()
        result = [re.sub(r'^(.*?) ','',i) for i in result]
        with open(serverPath+'result.json', 'w') as outfile:
            json.dump(result, outfile)
