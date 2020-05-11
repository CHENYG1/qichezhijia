import time

#写错误日志的函数
def writeLog(s):
    with open("errorLogs.txt", "a+", encoding="utf-8") as f:
        div = "///////////////////////////////"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f.write(div+str(timestamp)+div+"\n")
        f.write(s + "\n")


def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m" % '////'] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


