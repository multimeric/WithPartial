from with_pipe.pipe_context import PipeContext


def test_pipe_context_local():
    # Check that we can use functions defined "locally", ie within the current
    # scope
    module = {"a": [lambda: "foo"]}
    with PipeContext() as p:
        part = p.module.a[0]()
        assert callable(part)
        assert part() == "foo"


def test_pipe_context_module():
    # Check that we can use functions defined in another module
    import math

    with PipeContext() as p:
        part = p.math.floor(23.4)
        assert math.floor(23.4) == part()
