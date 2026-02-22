class Shape:
    def __init__(self, color,area,is_filled):
        self.color = color
        self.area = area
        self.is_filled = is_filled
    def discribe(self):
        fill_status = "filled" if self.is_filled else "not filled"
        return f"A {self.color} shape with an area of {self.area} that is {fill_status}."
class Circle(Shape):
    def __init__(self, color, area, is_filled, radius):
        super().__init__(color, area, is_filled)
        self.radius = radius
    def discribe(self):
        base_description = super().discribe()
        return f"{base_description} It is a circle with a radius of {self.radius}."
    print()
class Rectangle(Shape):
    def __init__(self, color, area, is_filled, width, height):
        super().__init__(color, area, is_filled)
        self.width = width
        self.height = height
    def discribe(self):
        base_description = super().discribe()
        return f"{base_description} It is a rectangle with a width of {self.width} and a height of {self.height}."
class Triangle(Shape):
    def __init__(self,color,area,is_filled, height, base):  
        super(). __init__(color,area , is_filled)
        self.height = height
        self.base = base
    def discribe(self):
        base_description = super().discribe()
        return f"{base_description} It is a triangle with a height of {self.height} and a base of {self.base}."

Circle.discribe()