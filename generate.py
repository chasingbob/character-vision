import os
import errno
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random

random.seed(5)

def get_random_font():
	return ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf",random.randint(10,45))

def get_random_color():
	return(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

def get_random_pos():
	return (random.randint(1, 180),random.randint(1, 180))

def generate_random_img(filename, text):
	font = get_random_font()
	background = get_random_color()
	colour = get_random_color()
	img = Image.new("RGBA", (200,200), background)
	draw = ImageDraw.Draw(img)
	draw.text(get_random_pos(), text, colour , font=font)
	draw = ImageDraw.Draw(img)
	img.save(filename)

def generate_batch(directory, basename, nb_images=1000):
	path = os.path.join(directory, basename)

	make_sure_path_exists(path)

	for i in range(0,nb_images):
		filename = '{}.{}.jpg'.format(basename, i);
		filename = os.path.join(path, filename)
		generate_random_img(filename, basename)

def make_sure_path_exists(path):
	try:
	    os.makedirs(path)
	except OSError as exception:
	    if exception.errno != errno.EEXIST:
		    raise
		

def main():
	
	generate_batch('data/train','a',1000)
	generate_batch('data/train','b',1000)

	generate_batch('data/validation','a',400)
	generate_batch('data/validation','b',400)


if __name__ == '__main__':
	main()
