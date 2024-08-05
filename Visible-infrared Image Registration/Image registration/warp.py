import numpy as np
import cv2

# Load infrared and visible light images
ir_image = cv2.imread('ir_test.png')
rgb_image = cv2.imread('vi_test.png')

R_prime = np.array  ([[0.3848,    0.0041, -30.9282],
                     [-0.0064,    0.3880, 31.5561],
                     [ 0,         0,    1.0000]])

t_prime = np.array  ([-0.054, -0.6325, 0])

# Input scale factor d
d = float(input("Enter the scale factor d: "))

# Calculate the inverse matrix
R_prime_inv = np.linalg.inv(R_prime)

# Calculate the mapping matrix
M = R_prime_inv

# Handle the translation component and integrate it into the mapping matrix
M[:, 2] -= (1 / d) * t_prime

# Use OpenCV's warpPerspective to perform perspective transformation
warped_ir_image = cv2.warpPerspective(ir_image, M, (rgb_image.shape[1], rgb_image.shape[0]))

# Adjust the transparency parameter
alpha = 0.6  # Transparency of the infrared image (0.0 - 1.0)
beta = 1 - alpha  # Transparency of the RGB image

# Blend the two images
blended_image = cv2.addWeighted(rgb_image, alpha, warped_ir_image, beta, 0)
cv2.imwrite('blended_image.png', blended_image)
# Display the results
# cv2.imshow("Warped IR Image", warped_ir_image)
# cv2.imshow("RGB Image", rgb_image)
cv2.imshow("Blended Image", blended_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
