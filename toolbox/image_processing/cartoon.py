import cv2

def draw_face(frame, x, y, w, h):
    draw_outline(frame, x, y, w, h)
    draw_eyes(frame, x, y, w, h)
    draw_nose(frame, x, y, w, h)
    draw_mouth(frame, x, y, w, h)
    draw_hair(frame, x, y, w, h)

def draw_outline(frame, x, y, w, h):
    center = (x + w/ 2, y + h/ 2)
    radius = min(w, h) / 2
    color = (0, 0, 255)
    thickness = 5
    cv2.circle(frame, center, radius, color, thickness)

def draw_eyes(frame, x, y, w, h):
    center1 = (x + w / 3, y + h / 3)
    center2 = (x + 2 * w / 3, y + h / 3)
    radius = min(w, h) / 10
    color = (255, 0, 0)
    thickness = 4
        
    cv2.circle(frame, center1, radius, color, thickness)
    cv2.circle(frame, center2, radius, color, thickness)

def draw_nose(frame, x, y, w, h):
    nose_top = (x + w / 2, y + 2 * w / 5)
    nose_bot_left = (int(x + (w / 2) - (0.1 * w)),  y + 2 * w / 3)
    nose_bot_right = (int(x + (w / 2) + (0.1 * w)),  y + 2 * w / 3)
    color = (0, 255, 0)
    thickness = 4
    
    cv2.line(frame, nose_top, nose_bot_left, color, thickness)
    cv2.line(frame, nose_top, nose_bot_right, color, thickness)
    cv2.line(frame, nose_bot_left, nose_bot_right, color, thickness)

def draw_mouth(frame, x, y, w, h):
    center = (x + w / 2, y + 4 * h / 5) 
    width = w / 4
    height = h / 10
    angle = 0
    startAngle = 0
    endAngle = 180
    color = (10, 100, 30)
    thickness = 10

    cv2.ellipse(frame, center, (width, height), angle, startAngle, endAngle, color, thickness)

def draw_hair(frame, x, y, w, h):
    center = (int(x + w/ 2), int(y + h/ 2))
    radius = min(w, h) / 2
    radius = int(radius * 1.1)
    angle = 0
    startAngle = 220
    endAngle = 320
    color = (60, 100, 160)
    thickness = 20

    cv2.ellipse(frame, center, (radius, radius), angle, startAngle, endAngle, color, thickness)
