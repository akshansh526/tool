
import base64
from PIL import Image
import io
# image = base64.b64decode(str('stringdata'))       
fileName = "https://www.shutterstock.com/shutterstock/photos/1421446100/display_1500/stock-photo-communication-technology-for-internet-business-global-world-network-and-telecommunication-on-earth-1421446100.jpg"

imagePath = ('E:\\tools\\ai-annotation-backend\\'+fileName)
img = Image.open(io.BytesIO(imagePath))
img.save(imagePath, 'jpg')




aa = {
  "project_name": "iocl",
  "description": "sdfsdfsfsasfaf",
  "industries_name": "sdfasfsfa",
  "start_date": "121212",
  "enddate": "121212",
  "add_classes" : ["car" , "bike", "etc"] 
  "approved_by": "akshansh"
}