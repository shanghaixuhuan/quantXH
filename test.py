def change_name(s):
    l = s.split('/')
    if len(l[1]) == 1:
        l[1] = "0"+l[1]
    if len(l[2]) == 1:
        l[2] = "0" + l[2]
    return ("-".join(l))


print(change_name("2020/1/1"))