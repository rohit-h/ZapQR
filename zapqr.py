#!/usr/bin/python3

import sys
import json
import qrcode
import requests
from   PyQt4.QtGui import *

def dmsg(msg):
	#print("[debug] " + msg)
	return

def drawQR(text):
	try:
		qr = qrcode.QRCode()
		qr.add_data(text)
		return qr.make_image()
	except Exception:
		print("Error generating qrcode")
		sys.exit(1)

def shortenURL(url):
	if len(url) < 20:
	    return url

	payload = {'longUrl':url}
	content = {'content-type':'application/json'}
	url = 'https://www.googleapis.com/urlshortener/v1/url'

	resp = requests.post(url, headers=content, data=json.dumps(payload))
	shorturl = resp.json().get('id')

	if shorturl is None:
	    return url

	return shorturl


def capture(app):
	dmsg("Reading clipboard")
	cbtext = app.clipboard().text().strip()
	if cbtext == "" :
		dmsg("Clipboard empty")
		sys.exit(0)

	dmsg("Clipboard contents: " + cbtext)
	return cbtext

def center(self):
	frameGm = self.frameGeometry()
	screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
	centerPoint = QApplication.desktop().screenGeometry(screen).center()
	frameGm.moveCenter(centerPoint)
	self.move(frameGm.topLeft())

def main():
	
	app = QApplication(sys.argv)
	
	txt = capture(app)

	if txt.startswith('http') == True:
	    txt = shortenURL(txt)

	img = drawQR(txt)
	img.save("/tmp/qr.png")

	win = QWidget()
	lbl = QLabel()
	pix = QPixmap("/tmp/qr.png")
	box = QVBoxLayout()
	inf = QLabel("QR Data : " + txt)
	
	lbl.setPixmap(pix)
	box.addWidget(lbl)
	box.addWidget(inf)

	win.resize(img.pixel_size, img.pixel_size)
	win.setLayout(box)
	win.setWindowTitle("ZapQR")
	win.show()

	center(win)

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
