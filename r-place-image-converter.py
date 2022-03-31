from PIL import Image, ImageEnhance
import sys
import getopt
import numpy as np

def closestColor(color):
    palette = np.array([[255,255,255],[218,94,56],[244,171,60],[243,215,109],[254,247,192],[171,231,124],[121,198,134],[96,158,113],[91,201,191],[151,228,239],[212,176,245],[241,158,171],[215,87,128],[145,68,167],[99,96,237],[201,203,205],[138,141,143],[81,82,82],[0,0,0]])
    d = np.sum(np.abs(palette-color)**(1.2),axis=1)
    return palette[np.argmin(d)] 

def main(argv):
    try:
        o, a = getopt.getopt(argv,"i:o:s:b:")
    except getopt.GetoptError:
        print('Usage: r-place-image-converter.py -i <inputfile> -o <outputfile> -s <maximum size> -b <brightness (optional)>')
        sys.exit(0)
    if "-i" not in dict(o):
        print('Usage: r-place-image-converter.py -i <inputfile> -o <outputfile> -s <maximum size> -b <brightness (optional)>')
        sys.exit(0)
    infile = dict(o)["-i"]
    outfile = "OUT"+infile.split(".")[0]+".png"
    if "-o" in dict(o):
        outfile = dict(o)["-o"]
    image = Image.open(infile)
    maxdim = max(image.size)
    target = 20
    if "-s" in dict(o):
        target = dict(o)["-s"]
    scale = round(maxdim/20)
    image = image.resize((round(max(image.size[0]/scale,1)),round(max(image.size[1]/scale,1))))
    if "-b" in dict(o):
        image = ImageEnhance.Brightness(image).enhance(float(dict(o)["-b"]))
    else:
        image = ImageEnhance.Brightness(image).enhance(1.3)
    w, h = image.size
    pix = list(image.getdata())
    newimg = Image.new('RGB', [w,h])
    data = newimg.load()
    for x in range(w):
        for y in range(h):
            if len(pix[y*w+x])>3 and pix[y*w+x][3]==0:
                data[x,y]=(255,255,255)
            else:
                data[x,y] = tuple(closestColor(np.asarray(pix[y*w+x][0:3])))
    newimg.save(outfile)

if __name__ == "__main__":
    main(sys.argv[1:])


