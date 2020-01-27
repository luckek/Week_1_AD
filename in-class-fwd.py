import sys
import math

class Dual(object):
  def __init__(self, real=0, epsilon_coef=0):
    self.real = real
    self.epsilon_coef = epsilon_coef
        
  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"

  def __add__(self, other):
    result = Dual(self.real, self.epsilon_coef)
    if type(other) is not Dual: 
      other = Dual(other)
            
    result.real += other.real
    result.epsilon_coef += other.epsilon_coef
    return result
    
  def __sub__(self, other):
    result = Dual(self.real, self.epsilon_coef)
    if type(other) is not Dual:
      other = Dual(other)

    # Subtraction follows the same rules as complex subtraction.
    result.real -= other.real
    result.epsilon_coef -= other.epsilon_coef
    return result
  
  def __mul__(self, other):
    result = Dual(self.real, self.epsilon_coef)
    if type(other) is not Dual:
      other = Dual(other)
    
    # Multiplication follows the same rules as complex multiplication,
    # however because \epsilon^2 = 0 so we exclude calculation of the
    # the last term.
    result.real *= other.real
    result.epsilon_coef = (other.real * result.epsilon_coef ) + (result.real * other.epsilon_coef) 
    return result
    
  def ln(other):
    # Notice the self argument is missing for this function. This is
    # because ln is a uniary operator depending only on its input.
    if type(other) is not Dual:
      other = Dual(other)
            
    real = math.log(other.real)
    epsilon_coef = (1/other.real) * other.epsilon_coef

    # We construct the result using only the input variable called other.
    return Dual(real, epsilon_coef)
    
  def sin(other):
    # Notice the self argument is missing for this function. This is because 
    # sin is a unary operator depending only on its input.
    if type(other) is not Dual:
      other = Dual(other)
            
    real = math.sin(other.real)
    epsilon_coef = math.cos(other.real) * other.epsilon_coef
        
    # We construct the result using only the input variable called other.
    return Dual(real, epsilon_coef)

class DualAdd(object):
  """
  Instantiate the Dual object with a real and dual (epsilon) component. 
  For example, you would create the dual number X1=5 by calling Dual(5, 1) 
  if you wish to find dF/dX1 for the function F. All other input variables X2...Xn
  will be created by not specifying an epsilon component. 
  """

  def __init__(self, real=0, epsilon_coef=0):
    self.real = real
    self.epsilon_coef = epsilon_coef
        
  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"

  def __add__(self, other):
    # Create a copy of this object so that we can return a new instance of Dual
    # instead of mutating our variables.
    result = DualAdd(self.real, self.epsilon_coef)
        
    # Not specifying an epsilon component is the same as setting it to 0. This is
    # useful when other is a scalar.
    if type(other) is not DualAdd: 
      other = DualAdd(other)
            
    # Addition follows the same rules as complex addition.
    result.real += other.real
    result.epsilon_coef += other.epsilon_coef
    return result

class DualSub(object):
  def __init__(self, real=0, epsilon_coef=0):
    self.real = real
    self.epsilon_coef = epsilon_coef
        
  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"
   
  def __sub__(self, other):
    result = DualSub(self.real, self.epsilon_coef)
    if type(other) is not DualSub:
      other = DualSub(other)

    # Subtraction follows the same rules as complex subtraction.
    result.real -= other.real
    result.epsilon_coef -= other.epsilon_coef
    return result

class DualMul(object):
  def __init__(self, real=0, epsilon_coef=0):
    self.real = real
    self.epsilon_coef = epsilon_coef

  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"
    
  def __mul__(self, other):
    result = DualMul(self.real, self.epsilon_coef)
    if type(other) is not DualMul:
      other = DualMul(other)

    # Multiplication follows the same rules as complex multiplication,
    # however because \epsilon^2 = 0 so we exclude calculation of the
    # the last term.
    result.real *= other.real
    result.epsilon_coef = (other.real * result.epsilon_coef ) + (result.real * other.epsilon_coef) 
    return result

class DualLn(object):
  def __init__(self, real=0, epsilon_coef=0):
    self.real = real
    self.epsilon_coef = epsilon_coef
        
  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"
    
  def ln(other):
    # Notice the self argument is missing for this function. This is
    # because ln is a uniary operator depending only on its input.
    if type(other) is not DualLn:
      other = DualLn(other)
            
    real = math.log(other.real)
    epsilon_coef = (1/other.real) * other.epsilon_coef

    # We construct the result using only the input variable called other.
    result = DualLn(real, epsilon_coef)
    return result

class DualSin(object):
  def __init__(self, real=0, epsilon_coef=0):
      self.real = real
      self.epsilon_coef = epsilon_coef

  def __repr__(self):
    return f"Dual({self.real}, {self.epsilon_coef})"

  def sin(other):
    # Notice the self argument is missing for this function. This is
    # because ln is a unary operator depending only on its input.
    if type(other) is not DualSin:
        other = DualSin(other)
        
    real = math.sin(other.real)
    epsilon_coef = math.cos(other.real) * other.epsilon_coef
    
    # We construct the result using only the input variable called other.
    result = DualSin(real, epsilon_coef)
    return result
    
def main(argv):

  print("Addition:")

  x1 = DualAdd(2, 1)
  x2 = DualAdd(5)
  y = x1 + x2
  print(f"y = {y.real}")
  print(f"dy/dx1 = {y.epsilon_coef}")
  
  x1 = DualAdd(5)
  x2 = DualAdd(2, 1)
  y = x1 + x2
  print(f"y = {y.real}")
  print(f"dy/dx2 = {y.epsilon_coef}")
  print()

  print("Subtraction:")
  
  x1 = DualSub(2, 1)
  x2 = DualSub(5)
  y = x1 - x2
  print(f"y = {y.real:.4g}")
  print(f"dy/dx1 = {y.epsilon_coef:.4g}")
  
  x1 = DualSub(5)
  x2 = DualSub(2, 1)
  y = x1 - x2
  print(f"y = {y.real:.4g}")
  print(f"dy/dx2 = {y.epsilon_coef:.4g}")
  print()

  print("Multiplication:")

  x1 = DualMul(2, 1)
  x2 = DualMul(5)
  y = x1 * x2
  print(f"y = {y.real:.4g}")
  print(f"dy/dx1 = {y.epsilon_coef:.4g}")

  x1 = DualMul(5)
  x2 = DualMul(2, 1)
  y = x1 * x2
  print(f"y = {y.real:.4g}")
  print(f"dy/dx2 = {y.epsilon_coef:.4g}")
  print()

  print("Functions:")
  
  x = DualLn(2, 1)
  y = DualLn.ln(x)
  print(f"y = {y.real:.4g}")
  print(f"dy/dx = {y.epsilon_coef:.4g}")
  print()
  
  x = DualSin(2, 1)
  y = DualSin.sin(x)
  print(f"y = {y.real:.4g}")
  print(f"dy/dx = {y.epsilon_coef:.4g}")
  print()

  print("f(x1, x2):")
  
  x1 = Dual(2, 1)
  x2 = Dual(5)

  y1 = Dual.ln(x1)
  y2 = x1 * x2
  y3 = Dual.sin(x2)
  y4 = y1 + y2
  out = y5 = y4 - y3

  print(f"out = {y5.real:.4g}")
  print(f"dout/dx1 = {y5.epsilon_coef:.4g}")

if __name__ == '__main__':
  main(sys.argv[1:])  
