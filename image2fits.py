"""
image2fits.py - Convert an RGB image to 3 FITS channels

Author: William Henney 
Version 0.1 - 07 Apr 2011
Version 0.2 - 24 Feb 2017 - Update for python3 and astropy
Version 0.3 - 23 Nov 2017 - Add support for RGBA (but we ignore the alpha channel)
Version 0.4 - 08 Aug 2018 - Track astropy API changes
"""
from __future__ import print_function
import numpy
try:
    # Default to using astropy
    from astropy.io import fits as pyfits
except:
    # Fall-back for older installations
    import pyfits
from PIL import Image
import argparse

def add_comments(hdu):
    hdu.header.add_comment("Written by image2fits.py, Will Henney 2011-2018")
    hdu.header.add_comment("Converted from  %s" % (args.file.name))
    

parser = argparse.ArgumentParser(description="Convert an RGB or Grayscale image to FITS format")
parser.add_argument("file", type=argparse.FileType('rb'),  help='Image file to convert')
parser.add_argument("--wcs", action="store_true", 
                    help='Add WCS info to FITS file header (NOT IMPLEMENTED YET)')

args = parser.parse_args()

im = Image.open(args.file)           # read the image
assert im.mode in ["RGBA", "RGB", "L" ], \
    "File %s is of type '%s', which is not supported" % (args.file, im.mode)
a = numpy.array(im)                  # convert to array

filestem = args.file.name.split('.')[0] 

if im.mode.startswith("RGB"):
    # split out the channels, flipping the y-axis
    r, g, b = [a[::-1,:,i] for i in [0, 1, 2]]   
    # Write each channel to a FITS file: XXX-red.fits, XXX-green.fits, XXX-blue.fits
    for chan, color in zip([r, g, b], ["red", "green", "blue"]):
        hdu =  pyfits.PrimaryHDU(chan)
        # Use the OBJECT keyword to describe this channel
        hdu.header['OBJECT'] = "%s channel" % (color)
        add_comments(hdu)
        hdu.writeto("%s-%s.fits" % (filestem, color), overwrite=True)
else:
    hdu =  pyfits.PrimaryHDU(a[::-1,:])
    add_comments(hdu)
    hdu.writeto("%s.fits" % (filestem), overwrite=True)



