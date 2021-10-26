def test_pipetools():
    import numpy as np
    from with_pipe.pipe_context import PipeContext
    from pipetools import pipe

    with PipeContext() as _:
        ret = (
            10
            > pipe | _.np.ones() | _.np.reshape(newshape=(5, 2)) | _.np.mean() | _.int()
        )
        assert ret == 1
