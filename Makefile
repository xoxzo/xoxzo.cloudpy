all: test

test:
    # exec all tests
	python -m unittest

test1:
	python -m unittest tests.test_cloudpy.TestXoxzoClientTestCase.test_get_din_list_success
