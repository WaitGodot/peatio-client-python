# formula

#MA
def MA(xArr, yArr, N):
    lenY = len(yArr);
    lenX = len(xArr);
    if lenX < N:
        return 0;
    for idx in range(lenY, lenX):
        ss = 0;
        av = 0;
        for k in range(0, N):
            nidx = idx - k;
            if nidx < 0:
                av = ss / float(k);
            else: 
                ss += xArr[idx - k];
        if av == 0:
            yArr.append(ss / float(N));
        else:
            yArr.append(av);

#EMA
def EMA(xArr, yArr, N):
    k = (2.0 / (N + 1.0));
    lenY = len(yArr);
    lenX = len(xArr);
    for idx in range(lenY, lenX):
        value = xArr[idx];
        if idx != 0:
            yArr.append(value * k + (1.0 - k) * yArr[idx - 1]);
        else:
            yArr.append(value);

#SMA(X,N,M) = SMA(N-1) * (N-M)/N + X(N)*M/N
def SMA(xArr, yArr, N, M):
    lenX = len(xArr);
    lenY = len(yArr);
    for idx in range(lenY, lenX):
        value = xArr[idx];
        if idx != 0:
            yArr.append(value*(float)(M)/(float)(N) + yArr[idx - 1] * ((float)(N)-(float)(M))/(float)(N));
        else:
            yArr.append(value);
#HIGH
def HIGH(xArr, yArr, N):
    lenX = len(xArr);
    lenY = len(yArr);
    for idx in range(lenY, lenX):
        high = 0;
        for n in range(0, N):
            nidx = idx - n;
            if nidx < 0:
                break;
            value = xArr[nidx];
            if high == 0:
               high = value;
            if high < value:
               high = value;
        yArr.append(high);
#LOW
def LOW(xArr, yArr, N):
    lenX = len(xArr);
    lenY = len(yArr);
    for idx in range(lenY, lenX):
        low = 0;
        for n in range(0, N):
            nidx = idx - n;
            if nidx < 0:
                break;
            value = xArr[nidx];
            if low == 0:
               low = value;
            if low > value:
               low = value;
        yArr.append(low);
    
#CROSS
def CROSS(AArr, BArr, N):
    lena = len(AArr);
    lenb = len(BArr);
    if lena < N or lenb < N or N <= 0:
        return False;
    if AArr[N-1] < BArr[N-1] and AArr[N] > BArr[N]:
        return True;
    return False;
#Angle
def ANGLE(Arr):
    lena = len(Arr);
    if lena < 2:
        return 0;
    rt = Arr[-1] - Arr[-2];
    if rt > 0:
        return rt;
    if rt < 0:
        return rt;
    return rt;
