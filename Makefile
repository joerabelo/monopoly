help:
	@echo "Try run: make install"

install:
	pdm install
	pdm run pre-commit install
run:
	@clear
	@pdm run python ./src/main.py

test:
	@clear
	pdm run pytest -v -s ./tests
test-quiet:
	@clear
	pdm run pytest -q ./tests

flake8:
	pdm run flake8 --extend-ignore E501 ./src
black: flake8
	pdm run black ./src
pre-commit:
	pdm run pre-commit run --all-files

docker: docker-build docker-run
	@# docker run -it --rm --name brasil-prev-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 python your-daemon-or-script.py
docker-build:
	docker build -t brasil-prev-python-app .
docker-run:
	docker run -it --rm --name brasil-prev-running-app brasil-prev-python-app
