import requests
from bottle import get, post, request, run, request, response
import json


class MasterRender(object):

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
	

	def json(self, url):

		req = requests.get("http://" + self.ip + ":" + str(self.port) + url)
		r = req.json()

		return r


	def getSalves(self):

		r = self.json("/html/slaves")
		return r


	def getRules(self):

		r = self.json("/html/rules")
		return r


	def getJobs(self):

		r = self.json("/html/jobs")
		return r


class MasterRenderPost(object):
	

	def __init__(self):

		self.lastFrame = -1
		self.maxFrame = -1
		self.minFrame = -1


	def request(self, url, data):
		
		req = requests.posts(url, data = data)


	def edit(self, id, info):

		self.request("/edit_" + id, info)


	def clear_jobs(self, r):

		if r:
			self.request("/clear", '{"clear":true}')
		else:
			self.request("/clear", '{"clear":false}')


	def cancel_jobs(self, id, r):

		if r:
			self.request("/cancel_", '{"clear":true}')
		else:
			self.request("/cancel_", '{"clear":false}')


	def balance_edit(self, id, old_value, new_value):

		if new_value != 0 and new_value != 0:
			self.request("/balance_enable", '{"' + id + '":' + new_value + "}")


	def balance_enable(self, id, value):

		self.request("/balance_enable", '{"' + id + '":' + value + "}")

	def showThumb(self, job, frame):

		if self.lastFrame != -1:

			if self.maxFrame != -1 and self.minFrame != -1:
				
				if frame >= self.minFrame and frame <= self.maxFrame:
					
					i = self.minFrame

					for i in range(self.maxFrame):
						self.toggleThumb(job, i)
						i += 1

					self.minFrame = -1
					self.maxFrame = -1
					self.lastFrame = -1

				elif frame > self.maxFrame:

					i = self.maxFrame +1
					for i in range(frame):
						self.toggleThumb(job, i)
						i += 1
					
					self.maxFrame = frame
					self.lastFrame = frame

				else:
					i = frame
					for i in range(self.minFrame -1):
						self.toggleThumb(job, i)
						i += 1
					self.minFrame = frame
					self.lastFrame = frame

			elif frame == self.lastFrame:
				self.toggleThumb(job, frame)

			elif frame < self.lastFrame:
				self.minFrame = frame
				self.maxFrame = self.lastFrame

				i = self.minFrame

				for i in range(self.maxFrame -1):
					self.toggleThumb(job, i)
					i += 1

				self.lastFrame = frame

			else:
				self.minFrame = self.lastFrame
				self.maxFrame = frame

				i = self.minFrame
				for i in range(self.maxFrame):
					self.toggleThumb(job, i)
					i += 1

				self.lastFrame = frame
		else:
			self.toggleThumb(job, frame)

	def toggleThumb(self, job, frame):

		url = "/tumb_" + job + "_" + frame + ".jpg"
		r = requests.get(url)

		if r.status_code == 200:
			return url
		else:
			return False
def dico(param):
	d = {}
	m = MasterRender("localhost", "8000")

	if param == "Slaves":
		return m.getSalves()
		
	elif param == "Rules":
		return m.getRules()
		
	elif param == "Jobs":
		return m.getJobs()

	elif param == "All":
		d['Salves'] = m.getSalves()
		d['Rules'] = m.getRules()
		d['Jobs'] = m.getJobs()
		
		return d
	


@get('/<param>')
def get(param):
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET'
	response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
	d = dico(param)
	
	return json.dumps(d)


if __name__ == '__main__':
	
	run(host="localhost", port=24116)