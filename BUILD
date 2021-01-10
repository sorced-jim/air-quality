py_binary(
    name = 'single_measure',
    srcs = ['single_measure.py'],
    deps = [':monitoring',
            ':sds011',
           ]
)

py_library(
    name = 'monitoring',
    srcs = ['monitoring.py'],
)

py_library(
    name = 'sds011',
    srcs_version = 'PY3',
    srcs = ['sds011_read.py'],
)

py_test(
    name = 'sds011_read_test',
    srcs = ['sds011_read_test.py'],
    python_version = 'PY3',
    srcs_version = 'PY3',
    deps = [':sds011'],
)
