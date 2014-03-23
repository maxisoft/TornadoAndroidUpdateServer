from pathlib import Path
import os

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")


class ApkUpdate(tornado.web.RequestHandler):
	def post(self):
		pkgname = self.get_argument("pkgname")
		version = self.get_argument("version")
		md5 = self.get_argument("md5")
		id = self.get_argument("id")
		print(pkgname, version, md5, id)
		self.write("""have update
/Test.apk
2
		""")

class ApkFileHandler(tornado.web.StaticFileHandler):
	def initialize(self, path):
		self.dirname, self.filename = os.path.split(path)
		super(ApkFileHandler, self).initialize(self.dirname)

	def get(self, path=None, include_body=True):
		super(ApkFileHandler, self).get(self.filename, include_body)

	def get_content_type(self):
		return "application/vnd.android.package-archive"


p = Path('Test.apk')

application = tornado.web.Application([
	(r"/", MainHandler),
	(r'/apkupdate', ApkUpdate),
	(r'/Test.apk', ApkFileHandler, {'path': str(p.resolve())})
])

if __name__ == "__main__":
	application.listen(8123)
	tornado.ioloop.IOLoop.instance().start()