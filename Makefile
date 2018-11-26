.PHONY: clean
clean:
	-rm output.mp4
	-pkill Python

bench-tcp: clean
	python3 sender.py &
	sleep 1;
	python3 client.py

bench-udp: clean
	python3 client.py -u &
	sleep 1;
	python3 sender.py -u
