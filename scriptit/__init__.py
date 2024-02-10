from scriptit import color, shape, size, RefreshPrinter

# Example usage of color module
print(color.colorize("Hello, Scriptit!", color.Colors.green))

# Example usage of shape module
shape.draw_rectangle(10, 5)

# Example usage of size module
print(size.to_hr(1024))

# Example usage of RefreshPrinter
p = RefreshPrinter()
for i in range(100):
    p.add("Dummy Report:")
    p.add("    iteration: " + str(i))
    p.refresh()
    time.sleep(1)
