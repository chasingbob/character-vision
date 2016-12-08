import os
from os.path import join, isfile, isdir
import errno
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random

random.seed(5)

class Options:
    light, dark, none = range(3)

def get_random_font():
    allowed_fonts = [
        'dejavu',
        'freefont',
    ]
    for i in range(5):
        base_dir = '/usr/share/fonts/truetype'
        font_dirs = [d for d in os.listdir(base_dir) if isdir(join(base_dir, d)) and d in allowed_fonts]
        font_dir = font_dirs[random.randint(0,len(font_dirs)-1)]
        fonts = [f for f in os.listdir(join(base_dir, font_dir)) if f.endswith('.ttf')]
        if len(fonts) > 0:
            font_name = fonts[random.randint(0, len(fonts)-1)]
            font_path = join(join(base_dir, font_dir), font_name)
            font = ImageFont.truetype(font_path, random.randint(12,55))
            return font


    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",random.randint(10,45))

    return font

def get_random_options():
    if random.randint(0,1) == 0:
        return Options.light, Options.dark
    return Options.dark, Options.light

def get_random_color(option=Options.none):
    if option == Options.none:
        return(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    elif option == Options.light:
        return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
    return (random.randint(0,105), random.randint(0,105), random.randint(0,105))

def get_random_pos():
    return (random.randint(1, 150),random.randint(1, 150))

def get_random_line():
    return (get_random_pos(), get_random_pos())

def generate_random_img(filename, text):
    font = get_random_font()
    back_option, front_option = get_random_options()
    back_colour = get_random_color(option=back_option)
    front_colour = get_random_color(option=front_option)
    img = Image.new("RGBA", (200,200), back_colour)
    draw = ImageDraw.Draw(img)
    
    nb_lines = random.randint(0, 5)
    
    for i in range(nb_lines):
        x1 = random.randint(1,200)
        x2 = random.randint(1,200)
        y1 = random.randint(1,200)
        y2 = random.randint(1,200)
        draw.line((x1, y1, x2, y2), fill=get_random_color(option=back_option),width=random.randint(1,20))

    nb_circles = random.randint(0, 5)

    for i in range(nb_circles):
        x1 = random.randint(1,150)
        x2 = random.randint(x1, 200)
        y1 = random.randint(1,150)
        y2 = random.randint(y1, 200)
        draw.ellipse((x1, y1, x2, y2), fill=get_random_color(option=back_option))


    draw.text(get_random_pos(), text, front_colour , font=font)
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
	
	generate_batch('data/train','0',10000)
	generate_batch('data/train','1',10000)
	#generate_batch('data/train','2',10000)
	#generate_batch('data/train','3',10000)
	#generate_batch('data/train','4',10000)
	#generate_batch('data/train','5',10000)
	#generate_batch('data/train','6',10000)
	#generate_batch('data/train','7',10000)
	#generate_batch('data/train','8',10000)
	#generate_batch('data/train','9',10000)

	generate_batch('data/validation','0',1000)
	generate_batch('data/validation','1',1000)
	#generate_batch('data/validation','2',2000)
	#generate_batch('data/validation','3',2000)
	#generate_batch('data/validation','4',2000)
	#generate_batch('data/validation','5',2000)
	#generate_batch('data/validation','6',2000)
	#generate_batch('data/validation','7',2000)
	#generate_batch('data/validation','8',2000)
	#generate_batch('data/validation','9',2000)


if __name__ == '__main__':
	main()
