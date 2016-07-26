all: sdist bdist_wheel

sdist:
	python setup.py sdist

bdist_wheel:
	python setup.py bdist_wheel

clean:
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf dist
