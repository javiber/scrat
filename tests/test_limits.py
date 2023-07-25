def test_size_limit(patched_decorator):
    import os

    # Function returns a random string so the only
    # we get the same result is that the result was cached
    @patched_decorator(max_size=29)
    def size_limit_test_func(a):
        return os.urandom(10)

    # Add 3 entries
    r1 = size_limit_test_func(1)  # resulting stash: 1
    r2 = size_limit_test_func(2)  # resulting stash: 1, 2
    # The size should not be enough to hold 3 results so the last call
    # should have removed the result for 1 (oldest)
    r3 = size_limit_test_func(3)  # resulting stash: 2, 3

    assert size_limit_test_func(2) == r2  # resulting stash: 3, 2
    assert size_limit_test_func(3) == r3  # resulting stash: 2, 3
    # Notice this last call should remove result for 2
    r12 = size_limit_test_func(1)  # resulting stash: 3, 1
    assert r12 != r1

    # result 3 should be the next in line to be removed,
    # but let's test what happens if we use it
    assert size_limit_test_func(3) == r3  # resulting stash: 1, 3
    # add a new entry should remove the result for 1 and leave the rest
    r4 = size_limit_test_func(4)  # resulting stash: 3, 4
    assert size_limit_test_func(4) == r4  # resulting stash: 3, 4
    assert size_limit_test_func(3) == r3  # resulting stash: 4, 3
    assert size_limit_test_func(1) != r1  # resulting stash: 3, 1

    # finally test that result 2 was removed before
    assert size_limit_test_func(2) != r2  # resulting stash: 1, 2
