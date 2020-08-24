__DOC__ = """根据斗鱼websocket传输协议，需要将发送的登录、入组、心跳等消息封装成特定结构的字节流。
即：
构造请求字符串 ---> 转换成字节流 ---> 按照协议将字节流封装 ---> 发送给服务器 ---> 弹幕数据传输
"""
import websocket
import time
import re


roomid = 252140


def gen_bytes(msg):
    """将像服务器发送的消息转换成字节流，并加入头部尾部封装成帧"""
    # 头部8字节，尾部1字节，与字符串长度相加即数据长度
    stream_len = len(msg) + 9
    # 消息长度
    len_byte = int.to_bytes(stream_len, length=4, byteorder='little')
    # 消息类型: 689(转换成字节流),表示客户端发给服务器的文本格式数据
    type_byte = int.to_bytes(689, 4, byteorder='little')
    # 数据部分
    msg_byte = msg.encode('utf-8')
    # 尾部以'\0'结束
    end_byte = bytearray([0x00])
    # 按顺序拼接在一起
    stream = len_byte + len_byte + type_byte + msg_byte + end_byte
    return stream

def login( ws):
    print("正在请求登录Websocket Server")
    msg = 'type@=loginreq/roomid@={0}/dfl@=sn@AA=105@ASss@AA=1/username@=auto_qJgSNpofja/uid@=18111590/ver@=20190610/aver@=218101901/ct@=0/'.format(roomid)
    msg_bytes = gen_bytes(msg)
    ws.send(msg_bytes)

def join_group( ws):
    """加入组信息"""
    print("正在请求加入组")
    msg = 'type@=joingroup/rid@={0}/gid@=1/'.format(roomid)
    msg_bytes = gen_bytes(msg)
    ws.send(msg_bytes)

def mk_alive():
    msg = 'type@=mkl/'
    msg_bytes = gen_bytes(msg)
    return msg_bytes

def on_message(ws, message):
    """client接收server端数据时触发"""
    danmu = message.decode(encoding='utf-8', errors='ignore')
    # 匹配弹幕类型
    re_str = '.*?/{0}@=(.*?)/.*?'
    uid = re.search(re.compile(re_str.format('uid')), danmu).group(1)
    user = re.search(re.compile(re_str.format('nn')), danmu).group(1)
    # 聊天弹幕
    if 'type@=chatmsg' in danmu:
        text = re.search(re.compile(re_str.format('txt')), danmu).group(1)
        info = '聊天信息：{0}({1}): {2}'.format(user, uid, text)
        print(info)
    # 用户进入
    elif 'type@=uenter' in danmu:
        level = re.search(re.compile(re_str.format('level')), danmu).group(1)
        info = '欢迎用户:lv{0}{1}({2})'.format(level, user, uid)
        print(info)
    # 其他
    else:
        info = danmu
        print(info)
    # 生成弹幕文件
    with open('danmu_files/{0}_danmu.txt'.format(roomid), 'a+', encoding='utf-8') as f:
        f.write(info + '\n')
        f.write('*******************************************************' + '\n')

def on_error(ws, error):
    """通信错误时触发"""
    print(error)

def on_close(ws):
    """关闭ws时触发"""
    print('wss连接已断开')

def on_open(ws):
    """建立ws连接时触发"""
    print('open')
    login(ws)
    print("登录成功")
    join_group(ws)
    print("加入成功")


ws = websocket.WebSocketApp('wss://danmuproxy.douyu.com:8505/',
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            on_open=on_open,
                            keep_running=True)
ws.run_forever(ping_interval=60, ping_timeout=5)

