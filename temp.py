# Mask off top 100 pixels for both masks
green_mask[:100, :] = 0
# Keep only bottom 100 pixels (frame height is 480)
red_mask[:FRAME_HEIGHT - 100, :] = 0

# Draw horizontal lines showing masked regions
# Top green mask line at y=100
cv.line(frame, (0, 100), (native_width, 100), (0, 255, 0), 2)
# Bottom red mask line at y=380
cv.line(frame, (0, native_height - 100),
         (native_width, native_height - 100), (0, 0, 255), 2)

 # Find green pixels
 green_pixels = np.where(green_mask > 0)
  # Find red pixels
  red_pixels = np.where(red_mask > 0)

   if len(green_pixels[1]) > 0:  # If any green pixels are found
        # Get leftmost (min x) and rightmost (max x) green points
        green_left_x = np.min(green_pixels[1])
        green_right_x = np.max(green_pixels[1])

        # Get highest (min y) and lowest (max y) green points
        green_top_y = np.min(green_pixels[0])
        green_bottom_y = np.max(green_pixels[0])

        # Draw vertical green lines at min and max x values
        cv.line(frame, (green_left_x, 0), (green_left_x,
                frame.shape[0]), (0, 255, 0), 2)  # Left line in green
        cv.line(frame, (green_right_x, 0), (green_right_x,
                frame.shape[0]), (0, 255, 0), 2)  # Right line in green

        #     print(f"Leftmost green x: {green_left_x}, Rightmost green x: {green_right_x}")
        #     print(f"Highest green y: {green_top_y}, Lowest green y: {green_bottom_y}")
        # else:
        #     print("No green pixels found in frame")

    if len(red_pixels[1]) > 0:  # If any red pixels are found
        # Get leftmost (min x) and rightmost (max x) red points
        red_left_x = np.min(red_pixels[1])
        red_right_x = np.max(red_pixels[1])

        # Draw vertical red lines at min and max x values
        cv.line(frame, (red_left_x, 0), (red_left_x,
                frame.shape[0]), (0, 0, 255), 2)  # Left line in red
        cv.line(frame, (red_right_x, 0), (red_right_x,
                frame.shape[0]), (0, 0, 255), 2)  # Right line in red
