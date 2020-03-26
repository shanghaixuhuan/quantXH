import datetime

now = datetime.datetime.now()
f = open("./static/local.txt","r+")
f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
f.close()