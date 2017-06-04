# formula


#EMA

def EMA(arr, N):
    rtarr = [];
    k = (2.0 / (N + 1.0));
    for idx, value in enumerate(arr):
        x = 0;
        if idx - 1 >= 0 & idx - 1 <= len(rtarr):
            x = rtarr[idx - 1];
        if idx != 0:
            rtarr.append(value * k + (1.0 - k) * x);
        else:
            rtarr.append(value);
    return rtarr;