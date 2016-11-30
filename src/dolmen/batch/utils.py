# -*- coding: utf-8 -*-

from math import log


def get_dichotomy_batches(batches, N, n):

    # normalize
    n = max(1, min(n, N))
    if not n:
        n = 1
    # number of iteration to find n doing a dichotomic search in 1..N
    log_position = int(log(max(N/n, 1), 2))

    markers = set([1, max(1, n-1), n, min(n+1, N), N])
    # always middle
    markers.add(int(N/2))
    # previous numbers in a dichotomich search
    for i in range(log_position)[-2:]:
        markers.add(int(N / 2**i))
    # next numbers  in a dichotomich search
    i = int(N / 2**(log_position+1))
    markers.add(i)
    markers.add(min(n + i, N))

    for i in range(log_position, ):
        markers.add(int(N / 2**i))

    # if we have less than 8 buttons, add some around current
    maxlen = min(8, N)  # maybe N < 8 !
    i = 2
    while len(markers) < maxlen:
        markers.add(min(n+i, N))
        markers.add(max(n-i, 1))
        i += 1
    markers = list(markers)
    markers.sort()

    last = 0
    for b in markers:
        if b and b > last:

            batch = batches[b - 1]

            if last and b > last + 1:
                yield 'ellipsis', '...'

            if b == n:
                yield 'current', batch
            elif b > n:
                yield 'next', batch
            else:
                yield 'previous', batch

            last = b


def iter_batches(batches, N, n):
    for b in batches:
        if b.number == n:
            yield 'current', b
        elif b.number > n:
            yield 'next', b
        else:
            yield 'previous', b
