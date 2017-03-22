import web
from nltk import ngrams
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.cross_validation import train_test_split
import re
import json

urls = (
	'/', 'Index' 
)

knn = KNeighborsClassifier(n_neighbors = 5)
X_train = None
X_test = None
y_train = None
y_test = None
data = []
target_y = []
data_X = []
properties = []  #array of features
n_of_grams = 3


app = web.application(urls, globals())
render = web.template.render('templates/')
class Index(object):
	"""docstring for index"""
	def GET(self):
		form = web.input(name = "FormContent")
		# greeting = "Check 18+"
		text = ""
		return render.index(pre = text, content = "")
	def POST(self):
		form = web.input(name="FormContent")
		content_predic = form.content
		pre = prediction_data(content_predic)
		return render.index(pre = pre, content = content_predic)

# read data for training
def read_data(file_name):
	f = open(file_name, "r")
	for line in f:
		line = unicode(line, 'utf8')
		data.append(line)
	f.close()

# read label for data training
def read_target_train():
	f_target = open("labels.txt", "r")
	for line in f_target:
		for x in line.split():
			target_y.append(int(x))
	f_target.close()

# training from data
def training():
	global y_test, X_test, knn
	read_data("preprocessor.txt")
	read_target_train()
	# n_grams get similar document
	for i in xrange(len(data)):
		n_grams = [data[i][j:j + n_of_grams] for j in xrange(len(data[i]) - n_of_grams + 1)]
		for grams in n_grams:
			if grams not in properties:
				properties.append(grams)
	print("len properties: %d" % len(properties))
	# Get feature of each other
	for i in xrange(0, len(data)):
		dic = ""
		data_tmp = []
		for j in xrange(0, len(properties)):
			_temp = data[i].count(properties[j])
			dic = dic + str(_temp) + " "
			data_tmp.append(_temp)
		data_X.append(data_tmp)
	# sklean
	X = np.array(data_X)
	y = np.array(target_y)
	knn.fit(X, y)


# predict for new sample
def prediction_data(content):
	print content
	global knn
	data_tmp = []
	test = content.lower()
	test = test.encode("utf-8")
	for j in xrange(0,len(properties)):
		_temp = test.count(properties[j].encode("utf-8"))
		data_tmp.append(_temp)
	pre = np.array(data_tmp)
	x = knn.predict(pre)
	if (x[0] == 1):
		return True
	return False
if __name__ == "__main__":
	training()
	app.run()