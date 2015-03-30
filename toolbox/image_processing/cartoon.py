import cv2

def draw_face(frame, x, y, w, h):
    draw_outline(frame, x, y, w, h)
    # draw_eyes(x, y, w, h)
    # draw_nose(x, y, w, h)
    # draw_mouth(x, y, w, h)
    # draw_hair(x, y, w, h)

def draw_outline(frame, x, y, w, h):
    center = (x + w/ 2, y + h/ 2)
    radius = min(w, h) / 2
    color = (0, 0, 255)
    thickness = 5
    cv2.circle(frame, center, radius, color, thickness)
