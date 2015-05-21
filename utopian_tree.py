t=int(raw_input())
for value in range(t):
    n=int(raw_input())
    h=1
    if (n==0):
        print 1
    else:
        for value in range(1,n+1):
            if value%2 == 0:
                h+=1
            else:
                h+=h
        print h   
