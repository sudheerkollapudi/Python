# Enter your code here. Read input from STDIN. Print output to STDOUT
no_it=int(raw_input())
s=[]
for value in range(no_it):
    s.append(raw_input())
k=[]
k.append(s[0])
for value in range(1,len(s)-1):
    k.append(s[value]) 
    for val1 in range(1,len(s[value])-1):
        if (int(s[value-1][val1]) < int(s[value][val1]) and
            int(s[value+1][val1])< int(s[value][val1]) and
            int(s[value][val1+1]) < int(s[value][val1]) and
            int(s[value][val1-1]) < int(s[value][val1])):
            s1=k[value]
            s1=s1[:val1]+'X'+s1[val1+1:]
            k[value]=s1
            
k.append(s[len(s)-1])
for value in k:
            print value
