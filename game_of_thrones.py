s = raw_input()
 
# Write the code to find the required palindrome and then assign the variable 'found' a value of True or False
s=list(s)
k=list(set(s))
c1=0
for v in k:
    if (s.count(v))%2 != 0:
        c1+=1

if c1 != 1 and c1 !=0:
    print("NO")
else:
    print("YES")
