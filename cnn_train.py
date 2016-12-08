import time
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.callbacks import History, ModelCheckpoint, Callback
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

img_width, img_height = 64, 64

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 4000
nb_validation_samples = 1600
nb_epoch = 50

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(128, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
				optimizer='rmsprop',
				metrics=['accuracy'])

train_datagen = ImageDataGenerator(
		rescale=1./255,
	        shear_range=0.1,
		zoom_range=0.1,
		horizontal_flip=False)
#train_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
		train_data_dir,
		target_size=(img_width, img_height),
		batch_size=32,
		class_mode='binary')


validation_generator = test_datagen.flow_from_directory(
		validation_data_dir,
		target_size=(img_width, img_height),
		batch_size=32,
		class_mode='binary')

start = time.time()

not_found = True
val_acc = []
acc = []

class Plotter(Callback):
    def on_train_begin(self, logs={}):
        self.acc = []
        self.val_acc = []
        self.loss = []
        self.val_loss = []
        self.epoch_count = 0
        plt.ion()
        plt.show()


    def on_epoch_end(self, epoch, logs={}):
        self.epoch_count += 1
        self.val_acc.append(logs.get('val_acc'))
        self.acc.append(logs.get('acc'))
        self.loss.append(logs.get('loss'))
        self.val_loss.append(logs.get('val_loss'))
        epochs = [x for x in range(self.epoch_count)]

        fig = plt.figure(1)
        plt.subplot(211)
        plt.title('Train vs Validation Accuracy')
        plt.axis([0,50,0,1])
        plt1 = plt.plot(epochs, self.val_acc, color='r')
        plt2 = plt.plot(epochs, self.acc, color='b')
        plt.ylabel('accuracy')

        red_patch = mpatches.Patch(color='red', label='Test')
        blue_patch = mpatches.Patch(color='blue', label='Train')

        plt.legend(handles=[red_patch, blue_patch], loc=4)
        plt.subplot(212)
        plt.title('Train vs Validation Loss')
        plt.axis([0,50,0,1])
        plt3 = plt.plot(epochs, self.val_loss, color='r')
        plt4 = plt.plot(epochs, self.loss, color='b')
        plt.ylabel('loss')

        red_patch = mpatches.Patch(color='red', label='Test')
        blue_patch = mpatches.Patch(color='blue', label='Train')

        plt.legend(handles=[red_patch, blue_patch], loc=1)
        plt.draw()
        plt.pause(0.001)
        
        #plt.savefig(locpath+'training_error.png')
        #plt.close('all')

plotter = Plotter()

hist = model.fit_generator(
	train_generator,
	samples_per_epoch=nb_train_samples,
	nb_epoch=nb_epoch,
	validation_data=validation_generator,
	nb_val_samples=nb_validation_samples,
        callbacks=[plotter])




#plt.plot(hist.history['acc'])
#plt.plot(acc)
#plt.plot(val_acc)
#plt.plot(hist.history['val_acc'])
#plt.title('model accuracy')
#plt.ylabel('accuracy')
#plt.xlabel('epoch')
#plt.legend(['train', 'test'], loc='upper left')
#plt.show()

model.save_weights('weights.hdf5')

end = time.time()
print('Duration: {}'.format(end - start))
input('Press ENTER to continue...')
