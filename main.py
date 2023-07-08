from PIL import Image
import np
from collections import defaultdict


def find_relationships(shapes):
  for shape in shapes:
    for other_shape in shapes:
     
      if shape == other_shape:
        continue
      
      if shape.min_x == other_shape.min_x:
        print("lines up on x with")
        shape.add_column(other_shape)
        other_shape.add_column(shape)
      
      if shape.min_y == other_shape.min_y:
        print("lines up on y with")
      
      if shape.min_x >= other_shape.min_x and shape.max_x <= other_shape.max_x:
        
        shape.add_row(other_shape)
        other_shape.add_row(shape)
        
        print("shape is completely within on x")
        if other_shape not in shape.children:
          other_shape.add_child(shape)
      
      if shape.min_y >= other_shape.min_y and shape.max_y <= other_shape.max_y:
        print("shape is completely within on y")
        if other_shape not in shape.children:
          other_shape.add_child(shape)

class Shape():
  def __init__(self, x, y):
    self.x = [x]
    self.y = [y]
    self.children = []
    self.next = []
    self.previous = []
    self.above = []
    self.left = []
    self.right = []
    self.below = []
    self.row = []
    self.column = []
    
  def extend(self, x, y):
    self.x.append(x)
    self.y.append(y)
    
  def burn(self):
    self.min_x = min(self.x)
    self.max_x = max(self.x)
    self.min_y = min(self.y)
    self.max_y = max(self.y)

  def add_child(self, shape):
    self.children.append(shape)

  def add_next(self, shape):
    self.next.append(shape)

  def add_previous(self, shape):
    self.previous.append(shape)

  def add_left(self, shape):
    self.left.append(shape)

  def add_right(self, shape):
    self.right.append(shape)

  def add_above(self, shape):
    self.above.append(shape)

  def add_below(self, shape):
    self.below.append(shape)

  def add_row(self, shape):
    self.row.append(shape)

  def add_column(self, shape):
    self.column.append(shape)
    
  def shapeid(self):
    return "x: {}-{} y: {}-{}".format(self.min_x, self.max_x, self.min_y, self.max_y)
    
  def __repr__(self):
    children = "\n".join(list(map(lambda x: "\t{}\n".format(x.shapeid()), self.children)))
    return "x: {}-{} y: {}-{}\n({})\n".format(self.min_x, self.max_x, self.min_y, self.max_y, children)

images = ["squaresquare.bmp", "interactionmap.bmp", "interactionmap2.bmp", "interactionmap3.bmp", "mvccdiagram.bmp"]

def process_image(image):
  img = np.array(Image.open(image))
  
  print(img.shape)
  
  data = np.array(img).reshape((img.shape[0],img.shape[1],3))
  
  
  
  shapes = []
  shape_index = defaultdict(dict)
  
  for x_pixel_no in range(0, img.shape[0]):
    x_pixel = data[x_pixel_no]
    for y_pixel_no in range(0, img.shape[1]):
      y_pixel = x_pixel[y_pixel_no]
      #print(data[x_pixel][y_pixel][0])
      if y_pixel[0] != 255:
        
       if data[x_pixel_no - 1][y_pixel_no][0] != 255:
         # connected
        shape_index[x_pixel_no][y_pixel_no] = shape_index[x_pixel_no - 1][y_pixel_no]
        shape_index[x_pixel_no - 1][y_pixel_no].extend(x_pixel_no, y_pixel_no)
         
       elif data[x_pixel_no][y_pixel_no - 1][0] != 255:
         shape_index[x_pixel_no][y_pixel_no] = shape_index[x_pixel_no][y_pixel_no - 1]
         shape_index[x_pixel_no][y_pixel_no - 1].extend(x_pixel_no, y_pixel_no)
       elif data[x_pixel_no][y_pixel_no][0] != 255:
         shape_index[x_pixel_no][y_pixel_no] = Shape(x_pixel_no, y_pixel_no)
         shapes.append( shape_index[x_pixel_no][y_pixel_no])
         print("Creating shape at {} {}".format(x_pixel_no, y_pixel_no))
  
  
  
  
  for shape in shapes:
    shape.burn()
  find_relationships(shapes)
  print(shapes)


  

  

for image in images:
  process_image(image)
  