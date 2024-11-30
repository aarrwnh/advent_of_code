```python
# math.lcm
def gcd(a: int, b: int) -> int:
    if a == b:
        return a
    if b > a:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    c = gcd(a, b)
    return a // c * b
```
