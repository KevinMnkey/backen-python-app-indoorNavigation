import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(image_path: str, output_path: str = 'uploads/contour_image_filled.png'):
    """
    Procesa una imagen de plano arquitectónico para detectar y rellenar contornos de paredes exteriores.

    :param image_path: Ruta del archivo de imagen de entrada.
    :param output_path: Ruta del archivo de imagen de salida (procesada).
    :return: Ruta del archivo de imagen procesada.
    """

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    
    filtered_image = cv2.medianBlur(image, 5)

   
    _, binary_image = cv2.threshold(filtered_image, 128, 255, cv2.THRESH_BINARY)

   
    kernel = np.ones((5, 5), np.uint8)
    cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    
    edges = cv2.Canny(cleaned_image, threshold1=50, threshold2=150)

   
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

 
    contour_image_filled = np.zeros_like(image)


    for i, contour in enumerate(contours):

        if hierarchy[0][i][3] == -1:

            cv2.drawContours(contour_image_filled, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)


    cv2.imwrite(output_path, contour_image_filled)

    # Mostrar la imagen rellena (opcional, solo para depuración)
    # plt.figure(figsize=(10, 10))
    # plt.imshow(contour_image_filled, cmap='gray')
    # plt.title('Contornos Rellenos de Paredes Exteriores')
    # plt.axis('off')
    # plt.show()

    return output_path

