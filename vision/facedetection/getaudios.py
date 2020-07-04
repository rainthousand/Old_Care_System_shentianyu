import requests
import execjs


# tk算法
class Return_tk:

    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


# 获取音频内容
def get_audio(keyword):
    # 请求网址
    url = 'https://translate.google.cn/translate_tts'

    js = Return_tk()
    # 获取请求参数的tk
    tk = js.getTk(keyword)
    # 请求参数
    params = {
        'ie': 'UTF-8',
        'q': keyword,
        'tl': 'zh-CN',
        'total': 1,
        'idx': 0,
        'textlen': len(keyword),
        'tk': tk,
        'client': 'webapp'
    }

    # 定义请求头
    headers = {
        'user - agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    # 请求网址
    r = requests.get(url, params=params, headers=headers)
    try:
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(e.__str__())


# 保存音频文件 filename为保存文件名
def save_audio(content, filename):
    with open(filename, 'wb+') as f:
        f.write(content)


if __name__ == "__main__":
    html = get_audio('你好')
    save_audio(html, 'b.mp3')
