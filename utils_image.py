from reportlab.lib import utils
from reportlab.platypus import Image
from reportlab.lib.units import cm

def get_image(path, height=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, height=height, width=(height / aspect))
    
    