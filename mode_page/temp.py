t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    b.sort()

    vec = [[0, 0] for _ in range(m)]

    pos = 0
    neg = 0
    j = 0

    for i in range(n):
        if a[i] >= 0:
            pos += a[i]
        else:
            neg -= a[i]

        if j < m and i + 1 == b[j]:
            vec[j] = [pos, neg]
            j += 1
            pos = 0
            neg = 0

        if j >= m:
            break

    operation = 0

    for i in range(m - 1, -1, -1):
        if operation % 2 == 1:
            vec[i][0], vec[i][1] = vec[i][1], vec[i][0]

        if vec[i][0] < vec[i][1]:
            operation += 1
            vec[i][0], vec[i][1] = vec[i][1], vec[i][0]

    ans = 0

    for i in range(m):
        ans += vec[i][0] - vec[i][1]

    for i in range(b[m - 1], n):
        ans += a[i]

    print(ans)