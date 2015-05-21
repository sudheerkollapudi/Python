s=list(raw_input())
s1=list(raw_input())
print len(list(set(s)-set(s1)))+len(list(set(s1)-set(s)))
