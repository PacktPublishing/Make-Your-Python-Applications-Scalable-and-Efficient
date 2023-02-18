.PHONY: help

status:
		docker-compose ps

stop:
		docker stop $(shell docker ps -aq)

clean:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)

destroy:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)
		docker rmi -f $(shell docker images -q)

up:
		# docker stop $(shell docker ps -aq)
		docker-compose -f docker-compose.yml up --build --scale application=6 -d
		sleep 5
		docker-compose ps

up-tests:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)
		docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build -d
		sleep 5
		docker-compose ps
