from deque import Deque
import random


def check_equal(d, ref, label=""):
    assert d.total_elements == len(ref), (
        f"{label}: total_elements mismatch, deque={d.total_elements}, ref={len(ref)}"
    )

    for i in range(len(ref)):
        actual = d[i]
        expected = ref[i]
        assert actual == expected, (
            f"{label}: mismatch at index {i}, deque={actual}, ref={expected}"
        )


def test_1_single_block_partial_fill():
    d = Deque()
    ref = []

    for i in range(5):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_1")
    print("test_1 passed")


def test_2_exactly_one_full_block():
    d = Deque()
    ref = []

    for i in range(10):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_2")
    print("test_2 passed")


def test_3_just_over_one_block():
    d = Deque()
    ref = []

    for i in range(11):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_3")
    print("test_3 passed")


def test_4_several_blocks_exact_comparison():
    d = Deque()
    ref = []

    for i in range(45):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_4")
    print("test_4 passed")


def test_5_pop_from_front_then_index_everything():
    d = Deque()
    ref = []

    for i in range(45):
        d.append(i)
        ref.append(i)

    for _ in range(13):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_5: pop mismatch, deque={actual}, ref={expected}"
        )

    check_equal(d, ref, "test_5")
    print("test_5 passed")


def test_6_pop_exactly_to_block_boundary():
    d = Deque()
    ref = []

    for i in range(30):
        d.append(i)
        ref.append(i)

    for _ in range(10):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_6: pop mismatch, deque={actual}, ref={expected}"
        )

    check_equal(d, ref, "test_6")
    print("test_6 passed")


def test_7_pop_across_block_boundary_then_index():
    d = Deque()
    ref = []

    for i in range(30):
        d.append(i)
        ref.append(i)

    for _ in range(11):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_7: pop mismatch, deque={actual}, ref={expected}"
        )

    check_equal(d, ref, "test_7")
    print("test_7 passed")


def test_8_many_pops_then_more_appends():
    d = Deque()
    ref = []

    for i in range(25):
        d.append(i)
        ref.append(i)

    for _ in range(17):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_8: pop mismatch, deque={actual}, ref={expected}"
        )

    for i in range(100, 115):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_8")
    print("test_8 passed")


def test_9_repeated_alternating_operations():
    d = Deque()
    ref = []

    for i in range(20):
        d.append(i)
        ref.append(i)

    for _ in range(5):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_9a: pop mismatch, deque={actual}, ref={expected}"
        )

    for i in range(20, 30):
        d.append(i)
        ref.append(i)

    for _ in range(7):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_9b: pop mismatch, deque={actual}, ref={expected}"
        )

    for i in range(30, 40):
        d.append(i)
        ref.append(i)

    check_equal(d, ref, "test_9")
    print("test_9 passed")


def test_10_emptying_completely_and_empty_pop():
    d = Deque()
    ref = []

    for i in range(15):
        d.append(i)
        ref.append(i)

    while ref:
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_10a: pop mismatch, deque={actual}, ref={expected}"
        )

    assert d.total_elements == 0, "test_10b: deque should be empty"

    try:
        d.pop()
        raise AssertionError("test_10c: expected IndexError on empty pop")
    except IndexError:
        pass

    print("test_10 passed")


def test_11_indexing_boundaries_only():
    d = Deque()
    ref = []

    for i in range(37):
        d.append(i)
        ref.append(i)

    for _ in range(8):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_11a: pop mismatch, deque={actual}, ref={expected}"
        )

    indices = [0, 1, 5, 9, 10, len(ref) - 2, len(ref) - 1]
    for i in indices:
        actual = d[i]
        expected = ref[i]
        assert actual == expected, (
            f"test_11b: mismatch at index {i}, deque={actual}, ref={expected}"
        )

    print("test_11 passed")


def test_12_randomized_against_list():
    random.seed(0)

    d = Deque()
    ref = []

    for step in range(1000):
        op = random.choice(["append", "pop"])

        if op == "append" or not ref:
            x = random.randint(0, 100000)
            d.append(x)
            ref.append(x)
        else:
            actual = d.pop()
            expected = ref.pop(0)
            assert actual == expected, (
                f"test_12: pop mismatch at step {step}, deque={actual}, ref={expected}"
            )

        check_equal(d, ref, f"test_12 step {step}")

    print("test_12 passed")


def test_13_multi_block_backward_indexing_stress():
    d = Deque()
    ref = []

    for i in range(60):
        d.append(i)
        ref.append(i)

    for _ in range(7):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_13a: pop mismatch, deque={actual}, ref={expected}"
        )

    for i in range(len(ref) // 2, len(ref)):
        actual = d[i]
        expected = ref[i]
        assert actual == expected, (
            f"test_13b: mismatch at index {i}, deque={actual}, ref={expected}"
        )

    print("test_13 passed")


def test_14_zero_as_real_value():
    d = Deque()
    ref = [0, 1, 0, 2, 0, 3, 0]

    for x in ref:
        d.append(x)

    check_equal(d, ref, "test_14a")

    for _ in range(3):
        actual = d.pop()
        expected = ref.pop(0)
        assert actual == expected, (
            f"test_14b: pop mismatch, deque={actual}, ref={expected}"
        )

    check_equal(d, ref, "test_14c")
    print("test_14 passed")


def run_all_tests():
    test_1_single_block_partial_fill()
    test_2_exactly_one_full_block()
    test_3_just_over_one_block()
    test_4_several_blocks_exact_comparison()
    test_5_pop_from_front_then_index_everything()
    test_6_pop_exactly_to_block_boundary()
    test_7_pop_across_block_boundary_then_index()
    test_8_many_pops_then_more_appends()
    test_9_repeated_alternating_operations()
    test_10_emptying_completely_and_empty_pop()
    test_11_indexing_boundaries_only()
    test_12_randomized_against_list()
    test_13_multi_block_backward_indexing_stress()
    test_14_zero_as_real_value()
    print("\nAll tests passed")


if __name__ == "__main__":
    run_all_tests()
