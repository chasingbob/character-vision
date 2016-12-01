import os
from os.path import join, isfile, isdir
import errno
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random

random.seed(5)

def get_random_font():
    allowed_fonts = [
        'dejavu',
        'freefont',
    ]
    not_found = True
    for i in range(5):
        base_dir = '/usr/share/fonts/truetype'
        font_dirs = [d for d in os.listdir(base_dir) if isdir(join(base_dir, d)) and d in allowed_fonts]
        font_dir = font_dirs[random.randint(0,len(font_dirs)-1)]
        fonts = [f for f in os.listdir(join(base_dir, font_dir)) if f.endswith('.ttf')]
        if len(fonts) > 0:
            font_name = fonts[random.randint(0, len(fonts)-1)]
            print(font_name)
            font_path = join(join(base_dir, font_dir), font_name)
            font = ImageFont.truetype(font_path, random.randint(12,55))
            not_fount = False
            return font


    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",random.randint(10,45))

    return font


def get_random_color():
	return(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

def get_random_pos():
	return (random.randint(1, 150),random.randint(1, 150))

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
