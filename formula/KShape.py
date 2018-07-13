
from formula.Direction import Direction
# return
# 0, 1

# 1.
def Hammer(ks, idx = -1):
    k = ks[idx];
    shadow = 10;
    d = k.Dir();
    if d == Direction.UP:
        if k.ShadowUp() < shadow and k.ShadowDown() / k.Entity() >= 2:
            return 1;
    if d == Direction.DOWN:
        if k.ShadowDown() < shadow and k.ShadowUp() / k.Entity() >= 2:
            return 1;
    return 0;

def Engulfer(ks, idx = -1):
    if len(ks) < 2:
        return 0;
    k1 = ks[idx - 1];
    k2 = ks[idx];

    d1 = k1.Dir();
    d2 = k2.Dir();
    if d1 == d2:
        return 0;

    eh1 = max(k1.c, k1.o);
    el1 = min(k1.c, k1.o);
    eh2 = max(k2.c, k2.o);
    el2 = min(k2.c, k2.o);

    if eh2 > eh1 and el2 < el1:
        return 1;
    return 0;

def DarkCloud(ks, idx = -1):
    if len(ks) < 2:
        return 0:
    k1 = ks[idx - 1];
    k2 = ks[idx - 2];

    d1 = k1.Dir();
    d2 = k2.Dir();
    if d1 == d2 or d1 == Direction.FLAT:
        return 0;

    if k1.Entity() < 60:
        return 0:
    if k2.o < k1.h * 0.02:
        return 0:

    if ((d1 == Direction.UP and k2.c < k1.c*0.98) or (d1 == Direction.DOWN and k2.c > k1.c*1.02)) and k2.Entity() > 20:
        return 1;
    return 0:

