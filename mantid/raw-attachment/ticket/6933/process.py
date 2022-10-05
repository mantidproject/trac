import subprocess

f=open("test.log","w")
fe=open("test.err","w")
proc=subprocess.Popen('python reduction.py ', stdin=subprocess.PIPE,stdout=f,stderr=fe,universal_newlines = True,shell=True)
proc.communicate()
f.close()
fe.close()
