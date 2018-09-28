import os
import urllib
import urllib2
#import graphlab
import turicreate as tc
import xml.etree.ElementTree as ET

def label_maker(label_original):
	switcher = {
		'strongbowA': "Strongbow",
		'strongbowR': "Strongbow",
		'heineken6': "Heineken",
		'heineken': "Heineken",
		'indioC': "Indio",
		'indio': "Indio",
		'sol': "Sol",
		'xx': "XX",
		'bohemiaP': "Bohemia",
		'miller': "Miller",
		'tecateC': "Tecate",
		'tecate': "Tecate"
	}
	return switcher.get(label_original, 'ERROR')

def drop_alpha(image):
    return tc.Image(_image_data=image.pixel_data[..., :3].tobytes(),
                    _width=image.width,
                    _height=image.height,
                    _channels=3,
                    _format_enum=2,
                    _image_data_size=image.width * image.height * 3)

imagesList = []
pic = tc.Image('imagesOld/train/IMG_1206.JPG')
pic = drop_alpha(pic)
imagesList.append(pic)

annotationList = []
tree = ET.parse('imagesOld/train/IMG_1206.xml')
root = tree.getroot()
children = root.getchildren()
anotation = []
for object in root.iter('object'):
	label = object[0].text
	label = label_maker(label)
	if label == 'ERROR':
		continue
	height = int(object[4][2].text)-int(object[4][0].text)
	width = int(object[4][3].text)-int(object[4][1].text)
	x = (int(object[4][2].text)+int(object[4][0].text)) / 2
	y = (int(object[4][3].text)+int(object[4][1].text)) / 2
	print label, x, y
	anotation.append({'coordinates': {'height': height, 'width': width, 'x': x, 'y': y}, 'label': label})
	annotationList.append(anotation)

print imagesList
print annotationList
test = tc.SFrame({'image': imagesList, 'annotation':annotationList})
test['image_with_boxes'] = tc.object_detector.util.draw_bounding_boxes(test['image'], test['annotation'])
test.explore()
