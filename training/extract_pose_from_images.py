import os
import mediapipe as mp
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Apply MediaPipe pose on images and write pose images to disk.')


parser.add_argument('--in', dest='in_dir', default='./in', type=str)
parser.add_argument('--out', dest='out_dir', default='./out', type=str)
parser.add_argument('--width', dest='w', type=int)
parser.add_argument('--height', dest='h', type=int)
parser.add_argument('--bg', dest='bg', action='store_true')
parser.add_argument('--centercrop', dest='centercrop', action='store_true')

args = parser.parse_args()
# print(args.tmp, args.tmp1)



files = []


for r, d, f in os.walk(args.in_dir):
    basename = os.path.basename(os.path.normpath(r))
    if basename == "tmp":
        continue
    for e in f:
        if e[0] == ".":
            continue
        files.append((os.path.join(r, e), e.replace(
            '.jpg', '{suffix}.jpg'.format(suffix=basename))))
# print(files)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=5)


for file in files:
    img = cv2.imread(file[0])
    with mp_pose.Pose(static_image_mode=True, upper_body_only=True) as pose:
        R = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_h, img_w, img_c = img.shape
        if R.pose_landmarks:
            # print(R.pose_landmarks)

            class customLandmarks:
                landmark = []

            class emptyLandmark:
                visibility = 0
                presence = 0
                x = 0
                y = 0
                z = 0

                def HasField(self, x):
                    return False

                def setvals(self, l):
                    self.x = l.x
                    self.y = l.y
                    self.z = l.z
                    self.visibility = l.visibility

            tmpl = [emptyLandmark() for _ in range(32)]
            tmpl[11:] = R.pose_landmarks.landmark[11:]
            # import web_pdb
            # web_pdb.set_trace()
            customLandmarks.landmark = tmpl
            PoseLandmark = mp_pose.PoseLandmark
            tmpconnections = frozenset([
                # (PoseLandmark.NOSE, PoseLandmark.RIGHT_EYE_INNER),
                # (PoseLandmark.RIGHT_EYE_INNER, PoseLandmark.RIGHT_EYE),
                # (PoseLandmark.RIGHT_EYE, PoseLandmark.RIGHT_EYE_OUTER),
                # (PoseLandmark.RIGHT_EYE_OUTER, PoseLandmark.RIGHT_EAR),
                # (PoseLandmark.NOSE, PoseLandmark.LEFT_EYE_INNER),
                # (PoseLandmark.LEFT_EYE_INNER, PoseLandmark.LEFT_EYE),
                # (PoseLandmark.LEFT_EYE, PoseLandmark.LEFT_EYE_OUTER),
                # (PoseLandmark.LEFT_EYE_OUTER, PoseLandmark.LEFT_EAR),
                # (PoseLandmark.MOUTH_RIGHT, PoseLandmark.MOUTH_LEFT),
                (PoseLandmark.RIGHT_SHOULDER, PoseLandmark.LEFT_SHOULDER),
                (PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW),
                (PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_WRIST),
                (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_PINKY),
                (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_INDEX),
                (PoseLandmark.RIGHT_WRIST, PoseLandmark.RIGHT_THUMB),
                (PoseLandmark.RIGHT_PINKY, PoseLandmark.RIGHT_INDEX),
                (PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW),
                (PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_WRIST),
                (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_PINKY),
                (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_INDEX),
                (PoseLandmark.LEFT_WRIST, PoseLandmark.LEFT_THUMB),
                (PoseLandmark.LEFT_PINKY, PoseLandmark.LEFT_INDEX),
                (PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_HIP),
                (PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_HIP),
                (PoseLandmark.RIGHT_HIP, PoseLandmark.LEFT_HIP),
            ])

            tmpimg = img

            if args.bg:
            	if args.h and args.w:
            		tmpimg = cv2.resize(img, (args.h, args.w), interpolation=cv2.INTER_LINEAR)
            else:
            	tmpimg = np.zeros((args.h or img_h, args.w or img_w, img_c), dtype="uint8")

            mp_drawing.draw_landmarks(image=tmpimg, landmark_list=customLandmarks,
                                      connections=tmpconnections, landmark_drawing_spec=drawing_spec, connection_drawing_spec=drawing_spec)
            if not args.bg:
            	_, tmpimg, _ = cv2.split(tmpimg)

            if args.centercrop:
            	if img_h > img_w:
            		tmpimg = tmpimg[ (img_h - img_w) // 2 : (img_h - img_w) // 2 + img_w, :]
            	else:
            		tmpimg = tmpimg[:, (img_w - img_h) // 2 : (img_w - img_h) // 2 + img_h]
            	pass

            cv2.imwrite("{out_dir}/{file}".format(out_dir=args.out_dir, file=file[1]), tmpimg)
