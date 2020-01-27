import sys
import math

class Constant:
    
  def __init__(self, a):
    # Initialize the value of this variable with the value passed in
    self.a_value = a

    # to make sure our children don't throw an exception when they access our grad variable 
    # as in backward() in the BinaryAdd()
    self.grad = 0
    
  def forward(self):
      
    # what should this return?
    # Remember this is the last node of the graph.
    return self.a_value
    
  def backward(self):

    # What should go here if it's a constant?
    # Nothing. We want the backpropagation to stop here. 
    # In python, we use pass as shorthand for "return None".
    # Doing this means we can inject constants at any point in the computational graph.
    pass

class BinaryAdd:
    
  def __init__(self, a, b):
    # record the two parents of the binary add
    self.a = a
    self.b = b

    # initialize the gradient to 0.
    self.grad = 0
        
  def forward(self):

    # a _value and b_value
    # are intermediate values in the computational graph
    # like v4 in Table 3 in the paper.
    # We don't have to store the value of a or b, 
    # but caching them now means we don't have to recompute them on the backward pass.
    self.a_value = self.a.forward()
    self.b_value = self.b.forward()

    return self.a_value + self.b_value
    
  def backward(self):
    # z = a + b

    # FIXME: check that this is right
    # dz/da = a'

    # Remember, a and b are the parents of this object. 
    dzda = 1.0
    dzdb = 1.0

    self.a.grad += dzda*self.grad
    self.b.grad += dzdb*self.grad

class BinarySub:
    
  def __init__(self, a, b):
    # record the two parents of the binary subtract
    self.a = a
    self.b = b

    # initialize the gradient to 0.
    self.grad = 0
        
  def forward(self):
    self.a_value = self.a.forward()
    self.b_value = self.b.forward()
    
    return self.a_value - self.b_value
    
  def backward(self):
    # z = a - b

    # FIXME: check that this is right
    # dz/da = a'

    # Remember, a and b are the parents of this object. 
    dzda = 1
    dzdb = -1

    self.a.grad += dzda*self.grad
    self.b.grad += dzdb*self.grad  # Why is this a += operator?

class BinaryMul:
    
  def __init__(self, a, b):
    self.a = a
    self.b = b
    
    # init gradient
    self.grad = 0
    
  def forward(self):
    # again, we don't have to cache self.a_value or self.b_value but
    # it makes the backward pass not have to call a.forward() or
    # b.forward()
    self.a_value = self.a.forward()
    self.b_value = self.b.forward()

    return self.a_value * self.b_value

  def backward(self):

    # z = a*b
    
    # dz/da =  a' * b + a * b'
    dzda = self.b.a_value
    dzdb = self.a.a_value

    self.a.grad += dzda*self.grad
    self.b.grad += dzdb*self.grad

class Ln:
    
  def __init__(self, a):
    self.a = a
    self.grad = 0
    
  def forward(self):
   
    self.a_value = self.a.forward()
      
    return math.log(self.a_value)

  def backward(self):

    # z = ln(a)

    # dz/da = a' = 1/a
    dzda = 1/self.a.a_value
    
    self.a.grad += dzda*self.grad

class Sin:
    
  def __init__(self, a):
    self.a = a
    self.grad = 0
        
  def forward(self):

    self.a_value = self.a.forward()
    return math.sin(self.a_value)
    
  def backward(self):

    # z = sin(a)
    # dz/da = a' = cos(a)
    dzda = math.cos(self.a_value)
    self.a.grad += dzda * self.grad

def main(argv):

  print("Addition:")
  
  a = Constant(2)
  b = Constant(3)
  z = BinaryAdd(a, b)

  y = z.forward()
  print(f'y: {y:.4g}') # y should be 5.
  print()

  print("Multiplication:")
  
  a = Constant(2)
  b = Constant(3)
  z = BinaryMul(a, b)

  y = z.forward()
  # y should equal 6.
  print(f'y: {y:.4g}')

  z.grad = 1.0
  z.backward()

  # dz/da should be 3, and dz/db 2.
  print(f'dz/da: {a.grad:.4g}', f'dz/db: {b.grad:.4g}')
  print()

  print("f(x1, x2):")
  
  x1 = Constant(2)
  x2 = Constant(5)

  v1 = Ln(x1)
  v2 = BinaryMul(x1, x2)
  v3 = Sin(x2)
  v4 = BinaryAdd(v1, v2)
  v5 = BinarySub(v4, v3)

  # Does the answer agree with the paper? y should be 11.65.
  y = v5.forward()
  print(f'y: {y:.4g}')
  
  # Instead of calling backward() on each node by hand, put the nodes
  # in a list and iterate over it backwards.
  ls = [x1, x2, v1, v2, v3, v4, v5]
  v5.grad = 1.0
  for node in ls[::-1]:
      node.backward()

  # should be 1.716 and 5.5
  print(f'dy/dx2: {x2.grad:.4g}',f'dy/dx1: {x1.grad:.4g}')
  
if __name__ == '__main__':
  main(sys.argv[1:])
