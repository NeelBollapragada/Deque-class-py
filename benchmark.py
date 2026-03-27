from time import perf_counter
from collections import deque as PyDeque

from deque import Deque
from linked_list import LLQueue


def ll_get_kth(queue, k):
    curr = queue.head
    steps = 0

    while curr is not None and steps < k:
        curr = curr.nxt
        steps += 1

    if curr is None:
        raise IndexError(f"k={k} out of range")

    return curr.val


def pydeque_get_kth(d, k):
    return d[k]


def customdeque_get_kth(d, k):
    return d[k]


def bench_bulk_append_pop(queue_factory, n, pop_fn_name="pop"):
    q = queue_factory()

    start = perf_counter()

    for i in range(n):
        q.append(i)

    pop_fn = getattr(q, pop_fn_name)
    for _ in range(n):
        pop_fn()

    end = perf_counter()
    return end - start


def bench_alternating(queue_factory, n, pop_fn_name="pop"):
    q = queue_factory()
    start = perf_counter()

    for i in range(n):
        q.append(i)
        getattr(q, pop_fn_name)()

    end = perf_counter()
    return end - start


def bench_churn(queue_factory, initial_size, ops, pop_fn_name="pop"):
    q = queue_factory()

    for i in range(initial_size):
        q.append(i)

    start = perf_counter()

    x = initial_size
    for _ in range(ops):
        q.append(x)
        getattr(q, pop_fn_name)()
        x += 1

    end = perf_counter()
    return end - start


def bench_single_access(queue_factory, size, access_fn, index):
    q = queue_factory()

    for i in range(size):
        q.append(i)

    start = perf_counter()
    value = access_fn(q, index)
    end = perf_counter()

    return end - start, value


def bench_repeated_access(queue_factory, size, access_fn, index, repeats):
    q = queue_factory()

    for i in range(size):
        q.append(i)

    start = perf_counter()

    checksum = 0
    for _ in range(repeats):
        checksum += access_fn(q, index)

    end = perf_counter()
    return end - start, checksum


def bench_mixed_accesses(queue_factory, size, access_fn, indices, repeats):
    q = queue_factory()

    for i in range(size):
        q.append(i)

    start = perf_counter()

    checksum = 0
    m = len(indices)
    for i in range(repeats):
        checksum += access_fn(q, indices[i % m])

    end = perf_counter()
    return end - start, checksum


def make_pydeque():
    return PyDeque()


def run_benchmarks():
    bulk_n = 200_000
    alternating_n = 100_000
    churn_initial = 10_000
    churn_ops = 100_000

    access_size = 50_000
    repeated_accesses = 50_000

    access_indices = {
        "10th": 9,
        "middle": access_size // 2,
        "near_end": access_size - 10,
    }

    queue_types = [
        {
            "name": "LLQueue",
            "factory": LLQueue,
            "pop_name": "pop",
            "access_fn": ll_get_kth,
        },
        {
            "name": "CustomDeque",
            "factory": Deque,
            "pop_name": "pop",
            "access_fn": customdeque_get_kth,
        },
        {
            "name": "collections.deque",
            "factory": make_pydeque,
            "pop_name": "popleft",
            "access_fn": pydeque_get_kth,
        },
    ]

    print("=" * 70)
    print("QUEUE BENCHMARKS")
    print("=" * 70)

    print("\n1. Bulk append then bulk pop")
    for q in queue_types:
        t = bench_bulk_append_pop(q["factory"], bulk_n, q["pop_name"])
        print(f"{q['name']:<20} {t:.6f} sec")

    print("\n2. Alternating append/pop")
    for q in queue_types:
        t = bench_alternating(q["factory"], alternating_n, q["pop_name"])
        print(f"{q['name']:<20} {t:.6f} sec")

    print("\n3. Steady-state churn")
    for q in queue_types:
        t = bench_churn(q["factory"], churn_initial, churn_ops, q["pop_name"])
        print(f"{q['name']:<20} {t:.6f} sec")

    print("\n4. Single access timings")
    for label, idx in access_indices.items():
        print(f"\n   Access: {label} element (index {idx})")
        for q in queue_types:
            t, value = bench_single_access(q["factory"], access_size, q["access_fn"], idx)
            print(f"{q['name']:<20} {t:.9f} sec   value={value}")

    print("\n5. Repeated access timings")
    for label, idx in access_indices.items():
        print(f"\n   Repeated access: {label} element (index {idx}) x {repeated_accesses}")
        for q in queue_types:
            t, checksum = bench_repeated_access(
                q["factory"], access_size, q["access_fn"], idx, repeated_accesses
            )
            print(f"{q['name']:<20} {t:.6f} sec   checksum={checksum}")

    print("\n6. Mixed access timings")
    mixed_indices = [0, 9, access_size // 4, access_size // 2, access_size - 10]
    print(f"   Indices cycled: {mixed_indices}, repeats={repeated_accesses}")
    for q in queue_types:
        t, checksum = bench_mixed_accesses(
            q["factory"], access_size, q["access_fn"], mixed_indices, repeated_accesses
        )
        print(f"{q['name']:<20} {t:.6f} sec   checksum={checksum}")

    print("\n" + "=" * 70)
    print("Done")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmarks()
