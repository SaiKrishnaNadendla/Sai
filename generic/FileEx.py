import pickle
object = [[101,'sai',2000],[102,'siva',3000]]
x = open("myfile.txt",'r')
pickle.load(x)
#print x
print  x.read()
x.close()
