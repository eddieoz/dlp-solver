# README

## ECDLP Solver

This project provides a Python implementation of an Elliptic Curve Discrete Logarithm Problem (ECDLP) solver using the Baby-step Giant-step algorithm. The code is designed to work with the SECP256K1 elliptic curve, commonly used in cryptographic applications such as Bitcoin.

### Requirements

- Python 3.x
- `numpy`
- `matplotlib`

You can install the required packages using pip:

```bash
pip install numpy matplotlib
```

### Files

- `ecdlp_solver.py`: Contains the implementation of the ECDLP solver and associated functions.

### Usage

1. **Define the Elliptic Curve Parameters:**

   The SECP256K1 curve parameters are defined in the code as follows:

   ```python
   curve = {
       'p': 2**256 - 2**32 - 977,
       'a': 0,
       'b': 7
   }
   ```

2. **Define the Base Point G:**

   The base point \( G \) on the elliptic curve is defined as:

   ```python
   G_x = int('0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16)
   G_y = int('0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16)
   ```

3. **ECDLP Solver Function:**

   The main function to solve the ECDLP is `ecdlp_solver`, which uses the Baby-step Giant-step algorithm:

   ```python
   def ecdlp_solver(curve, G, public_key):
       ...
   ```

   **Parameters:**
   - `curve`: Dictionary containing the parameters of the elliptic curve (`p`, `a`, `b`).
   - `G`: Tuple representing the base point \( G \) on the elliptic curve (`x`, `y`).
   - `public_key`: Tuple representing the public key point on the elliptic curve (`x`, `y`).

   **Returns:**
   - `k`: The discrete logarithm \( k \) such that \( k . G = {public\_key} \), or `None` if no solution is found.

4. **Helper Functions:**

   - `multiply_point(P, k, curve)`: Multiplies a point \( P \) by an integer \( k \) on the given elliptic curve using the double-and-add method.
   - `add_points(P, Q, curve)`: Adds two points \( P \) and \( Q \) on the given elliptic curve.

5. **Example Usage:**

   To solve for the discrete logarithm given an uncompressed public key:

   ```python
   public_key = "03c822d9f64d40a6027e6f05bad423b6dbd3db3b7ebd67170996d241f43ded1325"
   x = int(public_key[2:], 16)
   y = pow(x**3 + curve['a']*x + curve['b'], (curve['p'] + 1)//4, curve['p'])
   k = ecdlp_solver(curve, (G_x, G_y), (x, y))
   print(f"Discrete logarithm: {k}")
   ```

6. **Visualization:**

   A demonstration to visualize the ECDLP solver:

   ```python
   plt.scatter(np.arange(0, 256), [multiply_point((G_x, G_y), i, curve)[1] % curve['p'] for i in np.arange(0, 256)])
   plt.xlabel('x-coordinate')
   plt.ylabel('y-coordinate')
   plt.title('ECDLP Solver Demo')
   plt.show()
   ```

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments

This project uses the SECP256K1 elliptic curve parameters and the Baby-step Giant-step algorithm for solving the ECDLP. The implementation of the elliptic curve operations follows standard cryptographic practices.
