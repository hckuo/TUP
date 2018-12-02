all: bench-tcp bench-udp bench_tup

clean:
	-rm output.mp4
	-pkill -9 Python python3

bench-tcp: clean
	python3 sender.py -t &
	sleep 1;
	python3 client.py -t

bench-udp: clean
	python3 client.py -u &
	pclient=$$!
	sleep 1;
	python3 sender.py -u
	wait $$pclient

bench-tup: clean
	python3 sender.py -tu &
	sleep 1;
	python3 client.py -tu


.PHONY: clean all
