import math
import numpy as np
import matplotlib.pyplot as plt

# Define the SECP256K1 curve parameters
curve = {
    'p': 2**256 - 2**32 - 977,
    'a': 0,
    'b': 7
}

# Define the base point G on the elliptic curve
G_x = int('0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16)
G_y = int('0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16)

def ecdlp_solver(curve, G, public_key):
    """
    Solve the Elliptic Curve Discrete Logarithm Problem (ECDLP) using the Baby-step Giant-step algorithm.
    
    Parameters:
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).
    - G (tuple): The base point G on the elliptic curve as a tuple (x, y).
    - public_key (tuple): The public key point on the elliptic curve as a tuple (x, y).

    Returns:
    - k (int or None): The discrete logarithm k such that k*G = public_key, or None if no solution is found.
    """
    p = curve['p']
    m = math.isqrt(p) + 1  # Calculate the step size

    # Precompute baby steps
    baby_steps = {}
    for j in range(m):
        P = multiply_point(G, j, curve)
        baby_steps[P] = j

    # Compute the giant steps
    mG = multiply_point(G, m, curve)
    Q = public_key

    for i in range(m):
        if Q in baby_steps:
            return i * m + baby_steps[Q]
        Q = add_points(Q, (-mG[0] % p, -mG[1] % p), curve)  # Q - mG

    return None

def multiply_point(P, k, curve):
    """
    Multiply a point P by an integer k on the given elliptic curve using the double-and-add method.
    
    Parameters:
    - P (tuple): The point on the elliptic curve as a tuple (x, y).
    - k (int): The integer multiplier.
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).

    Returns:
    - Q (tuple): The resulting point after multiplication.
    """
    if k == 0:
        return (0, 0)
    elif k == 1:
        return P
    else:
        Q = multiply_point(P, k // 2, curve)
        Q = add_points(Q, Q, curve)
        if k % 2:
            Q = add_points(Q, P, curve)
        return Q

def add_points(P, Q, curve):
    """
    Add two points P and Q on the given elliptic curve.
    
    Parameters:
    - P (tuple): The first point on the elliptic curve as a tuple (x, y).
    - Q (tuple): The second point on the elliptic curve as a tuple (x, y).
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).

    Returns:
    - R (tuple): The resulting point after addition.
    """
    p = curve['p']
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        # Point doubling
        s = (3 * x1 * x1 + curve['a']) * pow(2 * y1, p-2, p) % p
    else:
        # Point addition
        s = (y2 - y1) * pow(x2 - x1, p-2, p) % p

    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)

# Input the uncompressed public key as a string
public_key = "03c822d9f64d40a6027e6f05bad423b6dbd3db3b7ebd67170996d241f43ded1325"

# Parse the public key
x = int(public_key[2:], 16)
y = pow(x**3 + curve['a']*x + curve['b'], (curve['p'] + 1)//4, curve['p'])

# Call the ECDLP solver with the parsed public key
k = ecdlp_solver(curve, (G_x, G_y), (x, y))
print(f"Discrete logarithm: {k}")

# Create a demo to visualize the ECDLP solver
plt.scatter(np.arange(0, 256), [multiply_point((G_x, G_y), i, curve)[1] % curve['p'] for i in np.arange(0, 256)])
plt.xlabel('x-coordinate')
plt.ylabel('y-coordinate')
plt.title('ECDLP Solver Demo')

# Show the plot
plt.show()
