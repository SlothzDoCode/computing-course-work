import qrcode

img = qrcode.make('https://www.youtube.com/shorts/H7oGB1budc0')
type(img)
img.save('test.png')