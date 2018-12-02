all: bench-tcp bench-udp

clean:
	-rm output.mp4
	-pkill -9 Python

bench-tcp: clean
	python3 sender.py -t &
	sleep 1;
	python3 client.py -t

bench-udp: clean
	python3 client.py -u &
	sleep 1;
	python3 sender.py -u
	wait

.PHONY: clean all
