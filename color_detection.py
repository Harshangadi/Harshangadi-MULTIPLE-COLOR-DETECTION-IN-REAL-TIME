import cv2
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# Load dataset
csv_path = r'C:\Internship project\Color-Detection-OpenCV-main\colors.csv'
csv = pd.read_csv(csv_path, names=["color", "color_name", "hex", "R", "G", "B"], header=None)

# Train KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(csv[['R', 'G', 'B']], csv['color_name'])

# Function to get color name using KNN
def get_color_name(R, G, B):
    color = knn.predict([[R, G, B]])
    return color[0]

# Callback function for mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        b, g, r = img[y, x]

# Load image
img_path = r"C:\Internship project\Color-Detection-OpenCV-main\.venv\WhatsApp Image 2024-05-30 at 3.20.10 PM.jpeg"
img = cv2.imread(img_path)
clicked = False

# Get screen resolution
screen_resolution = (1920, 1080)  # Change this to match your screen resolution


# Resize image to fit screen resolution
img = cv2.resize(img, screen_resolution)

# Create window and set mouse callback
cv2.namedWindow('image', cv2.WINDOW_NORMAL)  # Allow resizing the window
cv2.setMouseCallback('image', draw_function)

# Main loop
while True:
    cv2.imshow("image", img)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Set to full screen
    if clicked:
        # Ensure color values are integers
        b = int(b)
        g = int(g)
        r = int(r)
        
        # Extract color name
        color_name = get_color_name(r, g, b)
        
        # Draw rectangle and text on the image
        cv2.rectangle(img, (20, 20), (750, 60), (int(b), int(g), int(r)), -1)
        text = f'{color_name} R={r} G={g} B={b}'
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
        
    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break


# Close all windows
cv2.destroyAllWindows()
