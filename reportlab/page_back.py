from pathlib import Path

from reportlab.lib.utils import ImageReader

import os
import sys
import numpy
import scipy
import scipy.stats
import collections
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table, Flowable, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import ListItem, ListFlowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from utils_image import get_image
from six import string_types
from netCDF4 import Dataset
import re
import pandas as pd

def insert_page_back(self):
    logo_h = 2 * cm
    rand = 0.5 * cm  # Abstand der Logos zum Seitenrand

    page_width, page_height = self.c._pagesize

    #self.c.saveState()
    #self.c.setFillColorRGB(0.93, 0.93, 0.93)
    #self.c.rect(0, 0, page_width, page_height, stroke=0, fill=1)
    #self.c.restoreState()

    logo_path = Path(__file__).resolve().parent.parent / "logos" / "Logo_GERICS_BALL-hellgrau.png"
    logo = ImageReader(str(logo_path))
    logo_width, logo_height = logo.getSize()
    draw_width = page_height * logo_width / logo_height
    ball_height = page_height * 1.5
    self.c.drawImage(
        logo,
        (page_width - draw_width) / 2,
        (page_height - ball_height) / 2,
        width=draw_width,
        height=ball_height,
        mask="auto",
    )

    # Logo oben (nach dem Ball zeichnen, sonst wird es überdeckt)
    # Das BMFTR-JPG hat breite weisse Raender: nur den sichtbaren Inhalt (px) auf logo_h skalieren und ausschneiden
    bmftr = ImageReader(self.bmbf_logo)
    img_w, img_h = bmftr.getSize()
    cx0, cy0, cx1, cy1 = 90, 90, 700, 482  # Inhalts-Bbox in px, von oben gemessen (Bild 850x567)
    s = logo_h / (cy1 - cy0)
    content_top = self.height - 0.2 * cm
    self.c.saveState()
    clip = self.c.beginPath()
    clip.rect(rand, content_top - (cy1 - cy0) * s, (cx1 - cx0) * s, (cy1 - cy0) * s)
    self.c.clipPath(clip, stroke=0, fill=0)
    self.c.drawImage(bmftr, rand - cx0 * s, content_top - (img_h - cy0) * s,
                     width=img_w * s, height=img_h * s)
    self.c.restoreState()

    # Logos am ende der Seite (unten    )
    logo_y = 0.5 * cm
    gerics = get_image(self.gerics_logo, height=logo_h)
    gerics.wrapOn(self.c, self.width, self.height)
    gerics.drawOn(self.c, rand, logo_y)
    wascal = get_image(self.wascal_logo, height=logo_h)
    wascal.wrapOn(self.c, self.width, self.height)
    wascal.drawOn(self.c, rand + gerics.drawWidth + self.kleiner_abstand, logo_y)
    hereon = get_image(self.hereon_logo, height=logo_h)
    hereon.wrapOn(self.c, self.width, self.height)
    hereon.drawOn(self.c, self.width - rand - hereon.drawWidth, logo_y)