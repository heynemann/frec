compile:
	@python setup.py build_ext -i

test pyvows: compile
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=frec --cover_threshold=90 vows/

ci_test: compile
	@PYTHONPATH=.:$$PYTHONPATH pyvows -v --profile --cover --cover_package=frec --cover_threshold=90 --profile -vvv --no_color vows/

pep8:
	@for file in `find . -name '*.py'`; do autopep8 -i $$file; done


# %%%%%%%%%%%%%% APP %%%%%%%%%%%%%%
app:
	@PYTHONPATH=$$PYTHONPATH:. r3-app --redis-port=7778 --redis-pass=r3 --config-file="./frec/r3config.py"


# %%%%%%%%%%%%%% WORKER %%%%%%%%%%%%%%
kill-mappers:
	@ps aux | egrep r3-map | egrep -v egrep | awk '{ print $$2 }' | xargs kill -9

mapper:
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="1" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3

mappers: kill-mappers
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="1" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="2" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="3" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="4" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="5" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="6" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="7" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="8" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="9" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="10" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="11" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="12" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="13" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="14" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="15" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="16" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="17" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="18" --mapper-class="frec.map.FaceRecMapper" --redis-port=7778 --redis-pass=r3 &


# %%%%%%%%%%%%%% WEB %%%%%%%%%%%%%%
web:
	@PYTHONPATH=$$PYTHONPATH:. r3-web --redis-port=7778 --redis-pass=r3 --debug


# %%%%%%%%%%%%%% REDIS %%%%%%%%%%%%%%
kill_redis:
	@ps aux | awk '(/redis-server/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

redis: kill_redis
	@mkdir -p /tmp/r3/db
	@redis-server redis.conf &

