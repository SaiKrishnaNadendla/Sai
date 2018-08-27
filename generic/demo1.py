import  yaml
with open(r'settings.yaml', 'r') as stream:
    try:
        yaml_obj = yaml.load(stream)
    except yaml.YAMLError as exc:
        print  exc
        raise
#keys  = [1,10,2,5]
#print help(yaml_obj)
keys = yaml_obj.keys()
#print type(keys)
#print yaml_obj.keys().sort(key=int)
#print sorted(keys)
for i in range(10,20,5):
    print i
for i in range(10,20,2):
    print id(i)
    print i
ex = "Sai Krishna"
print len(ex)
class demo:
    def display(self):
        print "hi      0"
d = demo()
d.display
print type(d)

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):

    '''alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)'''
    print  [[atoi(c)] for c in re.split('(\d+)', text)]
    return [ atoi(c) for c in re.split('(\d+)', text) ]
def demo1(text):
    print "hi    "
#print keys
keys = ['Forum_16','Forum_32', 'Froum_14']
keys.sort(key=natural_keys)
print keys
#print(help(list.sort))
def demo1(text):
    print "hi    "
    return "hi"

map(demo1,'sai')
#print help(list)
#f = lambda a,b:  print a else b
def f(a):
    print a
map(f, [47,11])