test pyvows:
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=frec --cover_threshold=90 vows/
