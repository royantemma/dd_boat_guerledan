from datetime import datetime

s = datetime.now()
print(s)
s=s.strftime("%Y%m%d_%H%M%S%f")
h=int(s[9:11])
m=int(s[11:13])
sec=int(s[13:])*10e-7
print(h)
print(m)
print(sec)

t=(h*60 +m)*60 +sec
print(t)
