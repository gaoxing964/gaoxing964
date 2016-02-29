import thread

def funt(no,a):	
	while true :
		a = a+1 
		
def test():
	thread.start_new_thread(funt , (1,2))
	thread.start_new_thread(funt , (2,2))

test()
		
	

