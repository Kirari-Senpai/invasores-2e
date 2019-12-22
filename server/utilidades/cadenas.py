
import time,sys

def chain_alien(chain, timer=0.03):
	for i in chain:
			time.sleep(0.03)
			sys.stdout.write(str(i)+'')
			sys.stdout.flush()