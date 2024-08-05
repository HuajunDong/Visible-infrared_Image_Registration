import cv2
import pandas as pd

# Load the image
image_path = 'ir.png'
image = cv2.imread(image_path)
points = []

# Magnifier size
mag_size = 100
mag_factor = 5

# Mouse click event
def get_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point: ({x}, {y})")
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", image)
    if event == cv2.EVENT_MOUSEMOVE or event == cv2.EVENT_LBUTTONDOWN:
        if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
            # Get the region for the magnifier
            x1 = max(0, x - mag_size // 2)
            y1 = max(0, y - mag_size // 2)
            x2 = min(image.shape[1], x + mag_size // 2)
            y2 = min(image.shape[0], y + mag_size // 2)

            mag_region = image[y1:y2, x1:x2]
            mag_region = cv2.resize(mag_region, (mag_size * mag_factor, mag_size * mag_factor))

            # Add a red dot at the center of the magnifier
            center_x = mag_size * mag_factor // 2
            center_y = mag_size * mag_factor // 2
            cv2.circle(mag_region, (center_x, center_y), 5, (0, 0, 255), -1)

            cv2.imshow("Magnifier", mag_region)

# Display the image and set the mouse callback function
cv2.imshow("Image", image)
cv2.setMouseCallback("Image", get_points)

# Create the magnifier window
cv2.namedWindow("Magnifier", cv2.WINDOW_NORMAL)

# Wait for the user to complete the selection
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the selected points to an Excel file
if points:
    df = pd.DataFrame(points, columns=["X", "Y"])
    df.to_excel("points_coordinates.xlsx", index=False)
    print("Coordinates have been saved to points_coordinates.xlsx")

    # Save the image with marked points
    marked_image_path = 'marked_vi.png'
    cv2.imwrite(marked_image_path, image)
    print(f"The marked image has been saved to {marked_image_path}")
else:
    print("No points selected.")
