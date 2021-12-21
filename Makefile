FILES_PY = $(shell find $(CURDIR)/pyblogs -type f -name "*.py")

flake8:
	@echo "Running flake8"
	@flake8 $(FILES_PY)

mypy:
	@echo "Running mypy"
	@mypy $(FILES_PY)

isort:
	@echo "Running isort"
	@isort -c $(FILES_PY)

validate: flake8 mypy isort
