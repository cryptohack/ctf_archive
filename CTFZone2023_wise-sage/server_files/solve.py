import os
import random as rnd
import re
import socket
import sys
from Crypto.Cipher import AES
from hashlib import blake2b
from py_ecc.fields import optimized_bn128_FQ
from py_ecc.utils import prime_field_inv
from multiprocessing import Pool, cpu_count
from py_ecc.optimized_bn128.optimized_curve import (
    Optimized_Point3D,
    normalize,
    G1,
    multiply,
    curve_order,
    add,
    neg,
)
from sage.all import (
    EllipticCurve,
    GF,
    factor,
    discrete_log,
    CRT,
    QQ,
    Matrix,
    inverse_mod,
)


def egcd_step(prev_row, current_row):
    (s0, t0, r0) = prev_row
    (s1, t1, r1) = current_row
    q_i = r0 // r1
    return (s0 - q_i * s1, t0 - q_i * t1, r0 - q_i * r1)


def full_egcd(a, b):
    egcd_trace = [(1, 0, a), (0, 1, b)]
    while egcd_trace[-1][2] != 0:
        egcd_trace.append(egcd_step(egcd_trace[-2], egcd_trace[-1]))
    return egcd_trace


def isqrt(value):
    stop = 1
    while (stop * stop) < value:
        stop *= 2
    start = stop // 2
    while (stop - start) > 1:
        middle = (stop + start) // 2
        if middle * middle < value:
            start = middle
        else:
            stop = middle
    return start


def find_decomposers(lmbda, modulus):
    mod_root = isqrt(modulus)

    egcd_trace = [(1, 0, modulus), (0, 1, lmbda)]
    while egcd_trace[-2][2] >= mod_root:
        egcd_trace.append(egcd_step(egcd_trace[-2], egcd_trace[-1]))

    (_, t_l, r_l) = egcd_trace[-3]
    (_, t_l_plus_1, r_l_plus_1) = egcd_trace[-2]
    (_, t_l_plus_2, r_l_plus_2) = egcd_trace[-1]
    (a_1, b_1) = (r_l_plus_1, -t_l_plus_1)
    if (r_l**2 + t_l**2) <= (r_l_plus_2**2 + t_l_plus_2**2):
        (a_2, b_2) = (r_l, -t_l)
    else:
        (a_2, b_2) = (r_l_plus_2, -t_l_plus_2)

    return (a_1, b_1, a_2, b_2)


lmbda = 4407920970296243842393367215006156084916469457145843978461
beta = 2203960485148121921418603742825762020974279258880205651966

(a_1, b_1, a_2, b_2) = find_decomposers(lmbda, curve_order)


def compute_balanced_representation(scalar, modulus):
    c_1 = (b_2 * scalar) // modulus
    c_2 = (-b_1 * scalar) // modulus
    k_1 = scalar - c_1 * a_1 - c_2 * a_2
    k_2 = -c_1 * b_1 - c_2 * b_2
    return (k_1, k_2)


def multiply_with_endomorphism(x: int, y: int, scalar: int):
    assert scalar >= 0 and scalar < curve_order
    point = (optimized_bn128_FQ(x), optimized_bn128_FQ(y), optimized_bn128_FQ.one())
    endo_point = (
        optimized_bn128_FQ(x) * optimized_bn128_FQ(beta),
        optimized_bn128_FQ(y),
        optimized_bn128_FQ.one(),
    )
    (k1, k2) = compute_balanced_representation(k, curve_order)
    print(k1, k2)
    if k1 < 0:
        point = neg(point)
        k1 = -k1
    if k2 < 0:
        endo_point = neg(endo_point)
        k2 = -k2
    return normalize(add(multiply(point, k1), multiply(endo_point, k2)))


def multiply_without_endomorphism(x: int, y: int, scalar: int):
    assert scalar >= 0 and scalar < curve_order
    point = (optimized_bn128_FQ(x), optimized_bn128_FQ(y), optimized_bn128_FQ.one())
    return normalize(multiply(point, scalar))


print(normalize(multiply(G1, lmbda)))
print(curve_order)
print(optimized_bn128_FQ.field_modulus)
k = rnd.randint(1, curve_order - 1)
print(multiply_with_endomorphism(1, 2, k))
print(normalize(multiply(G1, k)))


Fp = GF(optimized_bn128_FQ.field_modulus)


def get_next_curve():
    b = 4
    while True:
        order = EllipticCurve(Fp, [0, b]).order()
        # if order % 3 == 1:
        yield (b, order)
        b += 1


def get_point_hash_from_server(sock, x, y):
    sock.sendall(f"ecdh ({x},{y})\n".encode())
    session_info = sock.recv(2048)
    session_hash = re.search(r"(?<=check: ).*(?=\n)", session_info.decode()).group(0)
    return session_hash


def get_public_point_from_server(sock, x, y):
    sock.sendall(f"ecdh ({x},{y})\n".encode())
    session_info = sock.recv(2048).decode()
    (p_x, p_y) = map(
        int,
        re.search(r"\((\d+),(\d+)\)", session_info.replace(" ", ""))
        .group()[1:-1]
        .split(","),
    )
    return (p_x, p_y)


def hash_point(point):
    return blake2b((str(point) + "0").encode()).hexdigest()


def compute_sequential_projective_points(starting_point, step_point, num_points):
    """Including the first point"""
    accumulator = starting_point
    point = step_point
    variants = [starting_point]
    for i in range(num_points - 1):
        accumulator = add(point, accumulator)
        variants.append(accumulator)
    return variants


def search_in_interval(
    starting_point, step_point, interval_size, point_hash, offset, subgroup_size
):
    cache_file_name = blake2b(
        (
            str(normalize(starting_point))
            + str(normalize(step_point))
            + str(interval_size)
        ).encode()
    ).hexdigest()
    full_filename = os.path.join("cache/", cache_file_name)
    if os.path.exists(full_filename):
        with open(full_filename, "rb") as f:
            cache = f.read()
        index = cache.find(bytes.fromhex(point_hash)[:16])
        if index == -1:
            return None
        else:
            if (index // 16) % 2 == 0:
                return offset + (index // 32)
            else:
                return subgroup_size - offset - ((index - 16) // 32)

    accumulator = starting_point
    point = step_point
    variants = [starting_point]
    for i in range(interval_size - 1):
        accumulator = add(point, accumulator)
        variants.append(accumulator)
    prod = [optimized_bn128_FQ(1)]
    for i in range(interval_size):
        prod.append(prod[-1] * variants[i][2])
    running_inverse = optimized_bn128_FQ(
        prime_field_inv(prod[-1].n, optimized_bn128_FQ.field_modulus)
    )
    for i in range(interval_size - 1, -1, -1):
        prod[i] = prod[i] * running_inverse
        running_inverse *= variants[i][2]
    new_variants = []
    with open(full_filename, "wb") as f:
        for i in range(interval_size):
            new_variants.append(
                ((variants[i][0] * prod[i]).n, (variants[i][1] * prod[i]).n)
            )
            f.write(bytes.fromhex(hash_point(new_variants[i]))[:16])
            f.write(
                bytes.fromhex(
                    hash_point(
                        (
                            new_variants[i][0],
                            optimized_bn128_FQ.field_modulus - new_variants[i][1],
                        )
                    )
                )[:16]
            )

    for i in range(interval_size):
        if hash_point(new_variants[i]) == point_hash:
            print("Found", offset + i)
            return offset + i
    for i in range(interval_size):
        if (
            hash_point(
                (
                    new_variants[i][0],
                    optimized_bn128_FQ.field_modulus - new_variants[i][1],
                )
            )
            == point_hash
        ):
            print("Found", subgroup_size - (offset + i))
            return subgroup_size - (offset + i)
    return None


def get_point_from_point_hash(original_x, original_y, point_hash, subgroup_order):
    pool_size = cpu_count()
    if subgroup_order < (1 << 10):
        pool_size = 1
    chunk = (subgroup_order + 2) // (pool_size * 2)
    while chunk > (1 << 20):
        pool_size *= 2
        chunk = (subgroup_order + 2) // (pool_size * 2)
    pool_starting_offsets = [(chunk * i) + 1 for i in range(pool_size)]

    point = (
        optimized_bn128_FQ(original_x),
        optimized_bn128_FQ(original_y),
        optimized_bn128_FQ.one(),
    )
    starting_points = [point]

    if pool_size > 1:
        scaled_point = multiply(point, chunk)
        for i in range(pool_size - 1):
            starting_points.append(add(starting_points[-1], scaled_point))

    if pool_size == 1:
        chunk_sizes = [chunk]
    else:
        chunk_sizes = [chunk] * (pool_size - 1) + [(subgroup_order - 1) % chunk]

    inputs = [
        (start, point, chunk_size, point_hash, offset, subgroup_order)
        for (start, chunk_size, offset) in zip(
            starting_points, chunk_sizes, pool_starting_offsets
        )
    ]

    if pool_size > cpu_count():
        for i in range(0, pool_size, cpu_count()):
            with Pool() as p:
                results = p.starmap(
                    search_in_interval,
                    inputs[i : i + cpu_count()],
                )
            print(results)
            for result in results:
                if result != None:
                    return result

    else:
        with Pool(min(cpu_count(), pool_size)) as p:
            results = p.starmap(
                search_in_interval,
                inputs,
            )
        print("Here", results)
        for result in results:
            if result != None:
                return result

    print(point_hash)
    print(hash_point((0, 0)))
    exit()


def batch_normalize(variants):
    prod = [optimized_bn128_FQ(1)]
    for i in range(len(variants)):
        prod.append(prod[-1] * variants[i][2])
    running_inverse = optimized_bn128_FQ(
        prime_field_inv(prod[-1].n, optimized_bn128_FQ.field_modulus)
    )
    for i in range(len(variants) - 1, -1, -1):
        prod[i] = prod[i] * running_inverse
        running_inverse *= variants[i][2]
    new_variants = []
    for i in range(len(variants)):
        new_variants.append(
            ((variants[i][0] * prod[i]).n, (variants[i][1] * prod[i]).n)
        )
    return new_variants


def batch_add(point_list, point):
    return [add(cur_point, point) for cur_point in point_list]


def add_normalize_hash(sequence, point, point_hash):
    blocksize = len(bytes.fromhex(point_hash))
    cache_file_name = blake2b(
        (str(sequence[0]) + str(sequence[-1]) + str(point)).encode()
    ).hexdigest()
    full_filename = os.path.join("cache/", cache_file_name)
    if os.path.exists(full_filename):
        with open(full_filename, "rb") as f:
            cache = f.read()
        index = cache.find(bytes.fromhex(point_hash))
        if index == -1:
            return -1
        else:
            return index // blocksize
    try:
        all_hashes = list(map(hash_point, batch_normalize(batch_add(sequence, point))))
        with open(full_filename, "wb") as f:
            for h in all_hashes:
                f.write(bytes.fromhex(h))
        return all_hashes.index(point_hash)
    except:
        return -1


def get_complex_point_from_point_hash(
    first_gen_x, first_gen_y, second_gen_x, second_gen_y, point_hash, subgroup_order
):
    first_gen = (
        optimized_bn128_FQ(first_gen_x),
        optimized_bn128_FQ(first_gen_y),
        optimized_bn128_FQ(1),
    )
    second_gen = (
        optimized_bn128_FQ(second_gen_x),
        optimized_bn128_FQ(second_gen_y),
        optimized_bn128_FQ(1),
    )
    first_sequence = compute_sequential_projective_points(
        first_gen, first_gen, subgroup_order - 1
    )
    second_sequence = compute_sequential_projective_points(
        second_gen, second_gen, subgroup_order - 1
    )
    step = max(cpu_count() - 1, 1)
    for i in range(0, subgroup_order - 1, step):
        print(subgroup_order, i)
        with Pool() as p:
            results = p.starmap(
                add_normalize_hash,
                [
                    (second_sequence, single_element, point_hash)
                    for single_element in first_sequence[i : i + step]
                ],
            )
        for k in range(len(results)):
            if results[k] != -1:
                print("Found", i + k + 1, results[k] + 1)

                return (i + k + 1, results[k] + 1)


def solve(sock):
    curve_it = get_next_curve()

    all_collected = set()
    unique_moduli = set()
    running_product = 1
    known_product = 1
    fixed_collected = set()
    while running_product * known_product < curve_order:
        (current_b, order) = next(curve_it)
        print("B:", current_b)
        print("CRT:", running_product)
        print("Scalar modulus:", curve_order)
        ec = EllipticCurve(Fp, [0, current_b])
        for generator in ec.gens():
            gen_order = generator.order()
            # print("Generator order:", gen_order)
            order_factors = gen_order.factor()
            for ftor, power in order_factors:
                if ftor < (1 << 28) and ftor > 7 and ftor not in unique_moduli:
                    print("Unique: ", unique_moduli)

                    new_gen = generator * (gen_order // ftor)
                    side_gen = ec(new_gen.xy()[0] * beta, new_gen.xy()[1])
                    try:
                        side_by_new = discrete_log(
                            side_gen, new_gen, ftor, operation="+"
                        )
                    except ValueError:
                        print("Failed on ", ftor)
                        point_hash = get_point_hash_from_server(
                            sock, int(new_gen.xy()[0]), int(new_gen.xy()[1])
                        )
                        (k1_cof, k2_cof) = get_complex_point_from_point_hash(
                            int(new_gen.xy()[0]),
                            int(new_gen.xy()[1]),
                            int(side_gen.xy()[0]),
                            int(side_gen.xy()[1]),
                            point_hash,
                            ftor,
                        )
                        fixed_collected.add((ftor, k1_cof, k2_cof))
                        unique_moduli.add(ftor)
                        known_product *= ftor
                        continue
                        pass
                    point_hash = get_point_hash_from_server(
                        sock, int(new_gen.xy()[0]), int(new_gen.xy()[1])
                    )
                    print("Point hash: ", point_hash, "order:", ftor, new_gen)
                    lg = get_point_from_point_hash(
                        int(new_gen.xy()[0]), int(new_gen.xy()[1]), point_hash, ftor
                    )
                    point_check = multiply_without_endomorphism(
                        int(new_gen.xy()[0]), int(new_gen.xy()[1]), lg
                    )
                    hash_check = hash_point(point_check)
                    assert hash_check == point_hash
                    multiplied_by_new = lg
                    try:
                        if (
                            ftor,
                            side_by_new,
                            multiplied_by_new,
                        ) not in all_collected and ftor not in unique_moduli:
                            running_product *= ftor
                            print(running_product)
                            print(curve_order)
                            all_collected.add((ftor, side_by_new, multiplied_by_new))
                            unique_moduli.add(ftor)
                    except ValueError:
                        pass
    product = 1
    print(all_collected)
    print(fixed_collected)
    for ft, side, ml in list(all_collected):
        product *= ft
    print(curve_order)
    print(product)
    lall = list(all_collected)
    fall = list(fixed_collected)
    side_crt = CRT([x for (_, x, _) in lall], [p for (p, _, _) in lall])
    muld_crt = CRT([x for (_, _, x) in lall], [p for (p, _, _) in lall])
    fixed_k1_crt = CRT([x for (_, x, _) in fall], [p for (p, _, _) in fall])
    fixed_k2_crt = CRT([x for (_, _, x) in fall], [p for (p, _, _) in fall])
    print(product, side_crt, muld_crt)

    new_muld = (
        (muld_crt - fixed_k1_crt - fixed_k2_crt * side_crt)
        * inverse_mod(known_product, product)
    ) % product

    print(new_muld)

    M = Matrix(
        [
            [1, 1 / QQ(1 << 127), 0, 0],
            [int(side_crt), 0, 1 / QQ(1 << 127), 0],
            [int(product), 0, 0, 0],
            [int(new_muld), 0, 0, 1 / QQ(known_product)],
        ]
    ).LLL()
    print(M)
    for entry in list(M):
        if entry[-1] == 1 / QQ(known_product):
            entry *= -1
        if entry[-1] == -1 / QQ(known_product):
            k1 = entry[1] * known_product * (1 << 127) + fixed_k1_crt
            k2 = entry[2] * known_product * (1 << 127) + fixed_k2_crt
            print("Possibly: ", k1, k2)
            return (k1 + k2 * lmbda) % curve_order


def run_client(host, port):
    port = int(port)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((host, port))
    print("Connected to server")
    print(serverSocket.recv(2048).decode())
    k = solve(serverSocket)
    (p_x, p_y) = get_public_point_from_server(serverSocket, 1, 2)
    print(multiply_without_endomorphism(1, 2, k))
    print(p_x, p_y)
    key = blake2b((str((p_x, p_y)) + "1").encode()).digest()[: AES.key_size[-1]]

    aes = AES.new(key, AES.MODE_CBC, bytes([0] * 16))
    k_str = str(k) + " " * (16 - len(str(k)) % 16)
    ct = bytes([0] * 16) + aes.encrypt(k_str.encode())
    serverSocket.sendall(b"answer " + ct.hex().encode() + b"\n")
    print(serverSocket.recv(2048).decode())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <hostname> <port>")
        exit()

    run_client(sys.argv[1], sys.argv[2])
