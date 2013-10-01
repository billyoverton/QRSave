#!/usr/bin/env python

# Copyright (c) 2013 Billy Overton
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PyQRNative import *
import optparse

def main():
    usage = "usage: %prog [options] FILE"
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option('--qrversion', '-q', type="int", dest="ver", default=10,
                      help="QR version 1-40.[Default: %default]")
    parser.add_option('--errorlevel', '-e', dest='errLvl', default="L",
                      help="QR Error Level: L,M,Q, or H [default: %default]")
    
    parser.add_option('--prefix', '-p', dest="prefix", default="qr",
                      help="Prefix to append infront of the file name. [default: %default]")
    (options, args) = parser.parse_args()
    
    qrError = QRErrorCorrectLevel.L

    if(options.errLvl == "L"):
        qrError = QRErrorCorrectLevel.L
    elif(options.errLvl == "M"):
        qrError = QRErrorCorrectLevel.M
    elif(options.errLvl == "Q"):
        qrError = QRErrorCorrectLevel.Q
    elif(options.errLvl == "H"):
        qrError = QRErrorCorrectLevel.H
    else:
        print "Invalid QR error correction level. Valid values are L, M, Q, or H."
        exit(1)

    if(options.ver < 1 or options.ver > 40):
        print "Invalid QR Version number. Valid numbers are between 1 and 40."
        exit(1)

    if(len(args) < 1):
        print "No filename was provided."
        exit(1)
    elif(len(args) > 1):
        print "More than one file name provided."
        print "Check that your file name is escaped if it contains spaces."
        exit(1)


    rsBlocks = QRRSBlock.getRSBlocks(options.ver, qrError)
    maxDataCountPerCode = 0
    for i in range(len(rsBlocks)):
        maxDataCountPerCode += rsBlocks[i].dataCount
    maxDataCountPerCode -= 3


    try:
        f = open(args[0], 'r');

        content = f.read(maxDataCountPerCode);
        i=0
        while(content != ""):
            qr = QRCode(options.ver, qrError)
            qr.addData(content)
            qr.make()
            im = qr.makeImage()
            im.save(options.prefix + str(i) + ".png")
            i += 1
            content = f.read(maxDataCountPerCode)
        f.close()
    except IOError:
        print "Unable to open file. Check your file name."
        exit(1)
if __name__ == '__main__':
    main()
