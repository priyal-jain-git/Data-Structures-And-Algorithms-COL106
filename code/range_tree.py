'''
INPUT:
list of coordinates
OUTPUT:
list of coordinates that are at l∞-distance at most d from q 
'''

class Node:
	
    def __init__(self, coordinates, left=None, right=None, y_tree=None, is_leaf=None,list=None):
        self._coordinates = coordinates
        self._left = left
        self._right = right
        self._y_tree= y_tree
        self._is_leaf=False
        self._list=list


class PointDatabase():

    def sortInput(self,pointlist,coord):
        merge(pointlist,0,len(pointlist),coord)
        x=[]+pointlist
        return x
    
    def __init__(self,pointlist):
        if len(pointlist)!=0:
            X=self.sortInput(pointlist,0)
            Y=self.sortInput(pointlist,1)
            self._head=createrangetree(X,Y)
        else:
            self._head=None
    
    def searchNearby(self,q,d):
        x=SearchTree(self._head,q[0]-d,q[0]+d,q[1]-d,q[1]+d)
        return x

'''Creates tree on the sorted list on the basis of x coordinate and then associates a sorted list will every node
which is sorted on the basis of y coordinate containing the points in the left and right subtree including that point also
Complexity nlogn '''
def createrangetree(X,Y):
    x=[]+Y
    if len(X)==0:
        return None
    if len(X)==1:
        node=Node(X[0])
        node._is_leaf=True
        node._y_tree=x
    else:
        mid=len(X)//2
        node = Node(X[mid])
        Yl=[]
        Yr=[]
        for i in range (0,len(Y)):
            if Y[i][0]<X[mid][0]:
                Yl.append(Y[i])
            elif Y[i][0]>X[mid][0]:
                Yr.append(Y[i])
        node._left = createrangetree(X[:mid],Yl)
        node._right = createrangetree(X[mid+1:],Yr)
        node._y_tree=x
    return node

'''Finds the first node in the range x1 and x2 as per x coordinate'''
def FindNode(root, x1 , x2, coord ):

    splt = root
    while splt != None:
        node = splt._coordinates[coord]
        if x2 < node:
            splt = splt._left
        elif x1 > node:
            splt = splt._right
        elif x1 <= node <= x2 :
            break
    return splt

'''Checks if the point is in the acceptable range'''
def checkRange(coord, range):
    x = coord[0]
    y = coord[1]
    if (x >= range[0][0]   and x <= range[0][1]  and y >= range[1][0]  and y <= range[1][1] ) :
        return True
    else:
        return False

'''Finds the points in the acceptable y range from the list 
logn time complexity'''
def binarySearch(arr, l, r, y1, y2, nodes):
    if len(arr)==0:
        return
    elif len(arr)==1:
        if y1<=arr[0][1] and arr[0][1]<=y2:
            nodes.append(arr[0])
    elif r >= l: 
        mid = l + (r - l) // 2
        if y1<=arr[mid][1] and arr[mid][1]<=y2:
            nodes.append(arr[mid])
            binarySearch(arr,l,mid-1,y1,y2,nodes)
            binarySearch(arr,mid+1,r,y1,y2,nodes)
        elif arr[mid][1] > y2:
            return binarySearch(arr, l, mid-1, y1,y2,nodes)
        else:
            return binarySearch(arr, mid + 1, r, y1,y2,nodes)
    return nodes

'''Searches the tree for the points with the required specifications
Time Complexity m+(logn)^2'''
def SearchTree(tree, x1, x2, y1, y2 ):
    output = []
    splitnode = FindNode(tree, x1, x2, 0)
    if (splitnode == None):
        return output
    elif splitnode._is_leaf==True:
        if checkRange(splitnode._coordinates, [(x1, x2), (y1, y2)]):
            output.append(splitnode._coordinates)
    else:
        if checkRange(splitnode._coordinates, [(x1, x2), (y1, y2)]):
            output.append(splitnode._coordinates)
        vl = splitnode._left 
        while ( vl != None ):
            if checkRange(vl._coordinates, [(x1, x2), (y1, y2)]):
                output.append(vl._coordinates)
            if (x1 <= vl._coordinates[0]):
                if vl._right != None:
                    l=[]
                    output += binarySearch(vl._right._y_tree,0,len(vl._right._y_tree)-1, y1, y2,l)
                vl = vl._left
            else:
                vl = vl._right
        vr = splitnode._right
        while ( vr != None ):
            if checkRange(vr._coordinates, [(x1, x2), (y1, y2)]):
                    output.append(vr._coordinates)
            if ( x2 >= vr._coordinates[0] ):
                if vr._left != None:
                    l=[]
                    output += binarySearch(vr._left._y_tree,0,len(vr._left._y_tree)-1, y1, y2,l)
                vr = vr._right
            else:
                vr = vr._left
    return output

'''Implementation of merge sort'''
def swap(a,i,j):
    c=a[j]
    a[j]=a[i]
    a[i]=c

def join(a,s,m,e,coord):
    i=s
    j=m
    x=[]
    while(i<m and j<e):
        if a[i][coord]>a[j][coord]:
            x.append(a[j])
            j+=1
        else:
            x.append(a[i])
            i+=1
    if i==m:
        for k in range(j,e):
            x.append(a[k])
    else:
        for k in range(i,m):
            x.append(a[k])
    c=s
    for k in range(0,len(x)):
        a[c]=x[k]
        c+=1

def merge(a,s,e,coord):
    l=e-s
    if l>2:
        merge(a,s,s+int(l/2),coord)
        merge(a,s+int(l/2),e,coord)
        join(a,s,s+int(l/2),e,coord)
    else:
        if s!=e-1 and a[s][coord]>a[s+1][coord]:
            swap(a,s,s+1)
