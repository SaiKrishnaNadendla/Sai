import re
def demo1(text):
    print "hi    "
    return  int(text) if text.isdigit() else text

'''print [(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]
for x in range(1,30):
    print "x    ",x
    for y in range(x, 30):
        print "y    ",y
        for z in range(y, 30):
            print "z    ",z
            #print "x ** 2    ",x ** 2
            #print "y ** 2    ",y ** 2
            #print "z ** 2    ",z ** 2
            if x ** 2 + y ** 2 == z ** 2:
                print [x,y,z]'''
x = 0

print "hi"
def demo2(x):
    print [demo1(text) for text in re.split('(\d+)', x)]
    return  [demo1(text) for text in re.split('(\d+)', x)]
x = ['Forum_16','Forum_32', 'Froum_14']
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):

    '''alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)'''

    return [ atoi(c) for c in re.split('(\d+)', text) ]
x.sort(key=natural_keys)
print (x)
#list = [demo1(text) for text in re.split('(\d+)', x)]
#print  "list  ",list














