n = int(input())
for i in range(n):
    s = input()
    j = 0
    while j < len(s):
        if (j > 1 and s[j-2] == s[j-1] and s[j-1] == s[j]) or (j > 2 and s[j] == s[j-1] and s[j-2] == s[j-3]):
            s = s[:j] + s[j+1:]
        else:
            j += 1
    print(s)