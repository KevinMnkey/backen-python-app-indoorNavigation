import svgwrite
import cv2
import numpy as np

def image_to_svg(image_file, svg_file):
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    dwg = svgwrite.Drawing(svg_file, profile='tiny', size=(image.shape[1], image.shape[0]))

    for contour in contours:
        points = [(float(point[0][0]), float(point[0][1])) for point in contour]
        dwg.add(dwg.polygon(points, fill='black'))

    dwg.save()
