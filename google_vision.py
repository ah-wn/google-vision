from requests import Session
from base64 import b64encode
from pprint import pformat

class VisionError(Exception):pass
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class Web:
	def __init__(self, web):
		self.entities = web.pop('webEntities')
		self.match = AttrDict({
			'full':[i['url'] for i in web.pop('fullMatchingImages', [])],
			'partial':[i['url'] for i in web.pop('partialMatchingImages', [])],
			'similar':[i['url'] for i in web.pop('visuallySimilarImages', [])],
			'pages':[AttrDict(i) for i in web.pop('pagesWithMatchingImages', [])]
		})
		self.guess = web.pop('bestGuessLabels')

	def __repr__(self):
		return pformat(vars(self))


URL = 'https://vision.googleapis.com/v1/images:annotate'
MAX_RESULTS = 50
FEATURES = AttrDict({
	"LANDMARK_DETECTION":'',
	"FACE_DETECTION":'',
	"OBJECT_LOCALIZATION":'',
	"LOGO_DETECTION":'logoAnnotations',
	"DOCUMENT_TEXT_DETECTION":'',
	"LABEL_DETECTION":'labelAnnotations', 
	"SAFE_SEARCH_DETECTION":'safeSearchAnnotation',
	"IMAGE_PROPERTIES":'imagePropertiesAnnotation', 
	"CROP_HINTS":'cropHintsAnnotation',
	"WEB_DETECTION":'webDetection'})

http = Session()

def set_key(key):
	http.params['key'] = key

def vision(*args):
	res = http.post(URL, json={'requests':args})
	data = res.json()
	error = data.get('error', None)
	if error:
		raise VisionError(data)
	res.results = data['responses']
	return res

def payload(image):
	if hasattr(image, 'read'):
		image = b64encode(image.read())
	return {'image':{'content':image}, 'features':[]}
