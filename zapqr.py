#!/usr/bin/python3

import sys
import qrcode
from   PyQt4.QtGui import *

def dmsg(msg):
	print("[debug] " + msg)
	return

def drawQR(text):
	try:
		image = qrcode.make(text)
		return image
	except Exception:
		print("Error generating qrcode")
		sys.exit(1)


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
