def in_order_traver(obj):
    if obj==None:
        return
    trav(obj.left)
    print obj.data
    trav(obj.right)
   
    
class node:
    def __init__ (self,data):
        self.data=data
        self.left=None
        self.right=None
        
root=node1(0)
i=0
while(i<5):
    i+=1
    s=int(raw_input())
    if root.data == 0:
        root.data=s
    else:
        temp1=root
        temp= node(s)
        while True:
            if (temp1.data < temp.data):
                if temp1.right != None:
                    temp1=temp1.right
                else:
                    temp1.right=temp
                    break
            elif (temp1.data >= temp.data):
                if temp1.left != None:
                    temp1=temp1.left
                else:
                    temp1.left=temp
                    break

trav(root)                


                
