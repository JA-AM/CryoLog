import cv2
from pyzbar import pyzbar

def decode_barcode(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect barcodes in the frame
    barcodes = pyzbar.decode(gray)
    
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract the bounding box location of the barcode
        (x, y, w, h) = barcode.rect
        
        # Draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Convert barcode data to string
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        
        # Display the barcode data and type on the frame
        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Print the barcode data to the console
        print(f"Found {barcode_type} barcode: {barcode_data}")
    
    return barcodes, frame

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If the frame was not captured successfully, break the loop
        if not ret:
            break
        
        # Call the function to decode barcodes
        barcodes, frame = decode_barcode(frame)

        print(barcodes)
        
        # Display the resulting frame
        cv2.imshow('Barcode Scanner', frame)
        
        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
