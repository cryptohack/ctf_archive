from Crypto.Util.number import bytes_to_long
from secrets import FLAG,p,q

N = p**3 * q
e = 0x10001
c = pow(bytes_to_long(FLAG),e,N)

print(f'Flag: {hex(c)}')

# Hint

w = 25965460884749769384351428855708318685345170011800821829011862918688758545847199832834284337871947234627057905530743956554688825819477516944610078633662855
x = p + 1328
y = p + 1329
z = q - 1

assert w*(x*z + y*z - x*y) == 4*x*y*z