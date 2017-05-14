.DELETE_ON_ERROR:

test-2.md: test.md
	@awk '/^#include/ {f=$$2; while(getline l<f){print l}; next} {print}' $< > $@


script-%.py: calculando-pi-en-raspberry-pi.md
	awk -vM=$* '/^```/ {n++; next} n==M {print}' $^ > $@
