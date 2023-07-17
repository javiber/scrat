def test_watch_functions(patched_decorator):
    counter = 0

    def aux_func():
        return 1

    @patched_decorator(watch_functions=[aux_func])
    def watch_test_func():
        nonlocal counter
        counter += 1
        return aux_func()

    assert watch_test_func() == 1
    assert watch_test_func() == 1
    assert counter == 1

    #
    # Simulate a code change in aux_func
    #
    def aux_func():
        return 2

    @patched_decorator(watch_functions=[aux_func])
    def watch_test_func():
        nonlocal counter
        counter += 1
        return aux_func()

    assert watch_test_func() == 2
    assert watch_test_func() == 2
    assert counter == 2


def test_watch_globals(patched_decorator):
    g1 = 1
    counter = 0

    @patched_decorator(watch_globals=["g1"])
    def test_global_func():
        nonlocal counter
        counter += 1
        return g1

    assert test_global_func() == 1
    assert test_global_func() == 1
    assert counter == 1

    #
    # Change global var
    #
    g1 = 2
    assert test_global_func() == 2
    assert test_global_func() == 2
    assert counter == 2
