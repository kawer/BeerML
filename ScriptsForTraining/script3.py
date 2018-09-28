import json
import os
import urllib
import urllib2
#import graphlab
import turicreate as tc
import xml.etree.ElementTree as ET
#from turicreate import  SFrame

# from pprint import pprint

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
		'tecate': "Tecate",
		'carta': "Carta Blanca"

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
annotationList = []
imageIndex = 0;

pic_path='imagesOld/train/'
for filename in os.listdir('imagesOld/train'):
	if(filename.split('.')[1]=='xml'):
		tree = ET.parse(pic_path + filename)
		root = tree.getroot()
		children = root.getchildren()
		for filename_jpg in os.listdir('imagesOld/train'):
			if(filename_jpg.split('.')[1] != 'xml' and filename_jpg.split('.')[0] == filename.split('.')[0]):
				pic = tc.Image(pic_path+filename_jpg)
				pic = drop_alpha(pic)
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
					anotation.append({'coordinates': {'height': height, 'width': width, 'x': x, 'y': y}, 'label': label})
				if len(anotation) != 0:
					annotationList.append(anotation)
					imagesList.append(pic)
				print "AnnotationList Addition Successful" + filename_jpg

with open('Cervezas.json') as cervezas:
	for line in cervezas: 
		cervezas_json = json.loads(line)
		if cervezas_json["content"][-4:] != ".jpg" and cervezas_json["content"][-4:] != ".png":
			continue
		imageIndex += 1
		print(imageIndex)
            	pic = tc.Image(cervezas_json["content"])
		pic = drop_alpha(pic)
		imagesList.append(pic)
		anotation = []
		for annot in cervezas_json["annotation"]:
			first_point = annot["points"][0]
			width = annot["imageWidth"]
			height = annot["imageHeight"]
			annotWidth = 0
			annotHeight = 0 
			for point in annot["points"]:
				if point[0] < first_point[0] and point[1] < first_point[1]:
					first_point = point
				elif point[0] == first_point[0]:
					annotHeight = abs(point[1] - first_point[1])
				elif point[1] == first_point[1]:
					annotWidth = abs(point[0] - first_point[0])
			annotHeight = annotHeight * height
			annotWidth = annotWidth * width
			anotation.append({'coordinates': {'height': int(annotHeight), 'width': int(annotWidth), 'x': int(first_point[0]*width + annotWidth/2), 'y': int(first_point[1]*height + annotHeight/2)}, 'label': annot["label"]})
		annotationList.append(anotation)
	imagesSArray = tc.SArray(imagesList)
	anotsSArray = tc.SArray(annotationList)
	imagesSFrame = tc.SFrame([imagesSArray, anotsSArray])
	imagesSFrame.rename({'X1':'image', 'X2': 'annotations'}, True)
	print(imagesSFrame)
	print(annotationList[0])
	train_data, test_data = imagesSFrame.random_split(0.8)

	# Create a model
	model = tc.object_detector.create(train_data, feature='image', max_iterations=5000)

	# Save predictions to an SArray
	#predictions = model.predict(test_data)

	# Evaluate the model and save the results into a dictionary
	#metrics = model.evaluate(test_data)

	#TestImages = []
	#for x in range(41, 50):
	#	TestImages.append(tc.Image('Fotos/' + str(imageIndex) + '.jpg'))
	#test = tc.SFrame({'image': TestImages})
	#test['predictions'] = model.predict(test)
	#print(test['predictions'])
	#test['image_with_predictions'] = tc.object_detector.util.draw_bounding_boxes(test['image'], test['predictions'])
	#test[['image', 'image_with_predictions']].explore()

	# Save the model for later use in Turi Create
	model.save('mymodel.model')

	# Export for use in Core ML
	model.export_coreml('MyCustomObjectDetector.mlmodel')

	imagesSFrame.save('imagesSFrame')
	#imagesSFrame.rename()
	#sf = tc.SFrame({'image': [imagesList], 'annotations': [annotationList]})
	#imagesSArray = SArray(data=[imagesList])
	#anotsSArray = SArray(annotationList)
	#sf = SFrame([imagesSArray, anotsSArray])
	#print(sf)

