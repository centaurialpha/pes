all:
	@echo "run 	run the local development version."
	@echo "clean	clean environment."
	@echo "flake8	run flake8."
	@echo "test	run the test suite."

run: clean
ifeq ($(VIRTUAL_ENV), )
	@echo "Your virtual environment is not activated."
else
	@python -m pes -d
endif

clean:
	rm -rf build
	rm -rf dist
	rm -rf .eggs
	rm -rf *.egg-info
	find . | grep -E "(__pycache__)" | xargs rm -rf
	find . | grep -E "*.py[co]" | xargs rm -rf

flake8:
	flake8 src/ tests/

test:
	@./run_tests
