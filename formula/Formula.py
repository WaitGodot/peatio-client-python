# formula


#EMA

def EMA(xArr, yArr, N):
    k = (2.0 / (N + 1.0));
    lenY = len(yArr);
    count = len(xArr) - lenY;
    for idx in range(lenY, count):
        value = xArr[idx];
        if idx != 0:
            yArr.append(value * k + (1.0 - k) * lenY[idx - 1]);
        else:
            yArr.append(value);


def High(arr):
    return sorted(arr)[-1];

def Low(arr):
    return sorted(arr)[0];