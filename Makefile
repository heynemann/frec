compile:
	@python setup.py build_ext -i

test pyvows: compile
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=frec --cover_threshold=90 vows/

ci_test: compile
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=frec --cover_threshold=90 --profile -vvv --no_color vows/

pep8:
	@for file in `find . -name '*.py'`; do autopep8 -i $$file; done
