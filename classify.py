import os
import sys
import PIL
import pathlib
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

train = False # ligue para treinar novos dados (inseridos no ./data/)
plot = True # ligue com o train para mostrar os resultados do treino
t_seed = 77777 # mude caso a taxa esteja muito baixa mesmo com os dados certos (linha amarela)

epochs = 15
batch_size = 25
num_classes = 3
size = (120, 120)

data_dir = pathlib.Path('data')
image_count = len(list(data_dir.glob('*/*.jpg')))
print('Tamanho do dataset: %d' % image_count)

# Dataset - Trainar
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset='training',
	seed=t_seed,
	image_size=size,
	batch_size=batch_size)

# Dataset - Validar
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset='validation',
	seed=t_seed,
	image_size=size,
	batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

if not train:
	model = keras.models.load_model('bbb_model')
else:
	#normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)	
	#normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
	#image_batch, labels_batch = next(iter(normalized_ds))

	# Modelo
	model = Sequential([
  		layers.experimental.preprocessing.Rescaling(1./255, input_shape=(size[0], size[1], 3)),
  		layers.Conv2D(16, 3, padding='same', activation='relu'),
  		layers.MaxPooling2D(),

  		#layers.Conv2D(32, 3, padding='same', activation='relu', input_shape=(size[0], size[1], 3)),
  		#layers.MaxPooling2D(),
  		layers.Conv2D(32, 3, padding='same', activation='relu'),
  		layers.MaxPooling2D(),
  		layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
  		layers.MaxPooling2D(),

  		layers.Dropout(0.1),
  		layers.Flatten(),
		layers.Dense(64, activation='relu'),
  		layers.Dense(num_classes, activation='softsign')
	])
	
	model.compile(optimizer='adam',
				  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
				  metrics=['accuracy'])
	
	history = model.fit(
		train_ds,
		validation_data=val_ds,
		epochs=epochs
	)
	
	model.save('bbb_model')
	
	# Visualizar resultados
	acc = history.history['accuracy']
	val_acc = history.history['val_accuracy']
	
	loss = history.history['loss']
	val_loss = history.history['val_loss']
	
	epochs_range = range(epochs)
	
	if (plot):
		plt.figure(figsize=(8, 8))
		plt.subplot(1, 2, 1)
		plt.plot(epochs_range, acc, label='Training Accuracy')
		plt.plot(epochs_range, val_acc, label='Validation Accuracy')
		plt.legend(loc='lower right')
		plt.title('Training and Validation Accuracy')
	
		plt.subplot(1, 2, 2)
		plt.plot(epochs_range, loss, label='Training Loss')
		plt.plot(epochs_range, val_loss, label='Validation Loss')
		plt.legend(loc='upper right')
		plt.title('Training and Validation Loss')
		plt.show()
	
def classify(path):
		img = keras.preprocessing.image.load_img(
				path, target_size = size
		)
		img_array = keras.preprocessing.image.img_to_array(img)
		img_array = tf.expand_dims(img_array, 0)

		predictions = model.predict(img_array)
		score = tf.nn.softmax(predictions[0])
		return (class_names[np.argmax(score)], 100 * np.max(score))
sys.modules[__name__] = classify # exportar classificador
