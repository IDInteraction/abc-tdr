import numpy as np
import cv2
import argparse


parser = argparse.ArgumentParser(description='Track an object given an initial bounding box and optional frameskip')
parser.add_argument('--infile', dest = 'infile', type=str, action='store', required = True)
parser.add_argument('--skipframe', dest = 'skipframe', type=int, action='store')
parser.add_argument('--skipms', dest = 'skipms', type=int, action='store')
parser.add_argument('--bbox', type=str, dest='bboxstr', action='store', required = True) # Will split into tuple later
parser.add_argument('--tracker', type=str, dest='tracker', action='store', default='MIL')
parser.add_argument('--showvideo', dest='showvideo', action='store_true')
parser.set_defaults(showvideo=False)

args=parser.parse_args()

if args.showvideo == True:
    cv2.namedWindow("tracking")
camera = cv2.VideoCapture(args.infile)
bbox =tuple(map(int, args.bboxstr.split(',')))
tracker = cv2.Tracker_create(args.tracker)

if(args.skipframe and args.skipms):
    print("Cannot skip frames and time")
    quit()

if(args.skipframe):
    camera.set(cv2.CAP_PROP_POS_FRAMES, args.skipframe)
if(args.skipms):
    camera.set(cv2.CAP_PROP_POS_MSEC, args.skipms)


init_once = False

while camera.isOpened():
    ok, image=camera.read()
    frame = camera.get(cv2.CAP_PROP_POS_FRAMES)
    if not ok:
#        print 'no image read'
        break

    if not init_once:
        ok = tracker.init(image, bbox)
        init_once = True

    ok, newbox = tracker.update(image)
    #print ok, newbox
    print str(frame) + "," +  str(newbox[0]) + "," + str(newbox[1]) + "," + str(newbox[2]) + "," + str(newbox[3])
    if ok:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))
    if args.showvideo == True:
        cv2.imshow("tracking", image)
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break # esc pressed
