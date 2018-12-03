all: bench-tcp bench-udp bench_tup

clean:
	-@rm output.mp4 2> /dev/null || true
	echo $(whoami)
	-@pkill -u hckuo2 python3 || true

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

# example: sender_opts="--audp --budp --pudp -d 10" make bench-tup
bench-tup: clean
	@python3 sender.py -tu $$sender_opts &
	@psender=$$!
	@sleep 2;
	@python3 client.py -tu
	@wait $$psender


.PHONY: clean all
.SILENT:clean
