import aiohttp,datetime,os,re
from loguru import logger

logger.level("INFO")

async def ensure_file_exists(filename):
    """确保文件存在，不存在则创建空文件"""
    if not os.path.exists(filename):
        # 创建空文件
        with open(filename, "w", encoding="utf-8") as f:
            pass

async def get_deltaforce_secrets():
    url = "https://www.onebiji.com/hykb_tools/sjz/mrmm/index.php?immgj=1"
    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.62(0x18003e33) NetType/WIFI Language/zh_CN",
        'Accept-Encoding': "gzip,compress,br,deflate",
        'content-type': "application/x-www-form-urlencoded;",
        'Referer': "https://servicewechat.com/wx1c36464bbea2507a/84/page-frame.html",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            response_text = await response.text()
            result = re.findall(r'<span\s+class="name">(.*?)</span>', response_text)
            logger.debug(f"获取密码门密码返回值：{set(result)}")
            if response.status == 200:
                formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
                formatted_text = formatted_date + "\n(今日密码门密码：" + "\n" + "\n".join(result[0:5])
                # 缓存到文件
                with open("deltaforce_secrets.txt", "w", encoding="utf-8") as f:
                    f.write(formatted_text)
                return formatted_text
            else:
                logger.error(f"获取密码门密码失败，状态码：{response.status}")

async def getSecrets():
    formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
    await ensure_file_exists("deltaforce_secrets.txt")
    with open("deltaforce_secrets.txt", "r", encoding="utf-8") as f:
        file_text = f.read()
        last_date = file_text.split("\n")[0].strip()
        if last_date != formatted_date:
            formatted_text = await get_deltaforce_secrets()
        else:
            logger.debug("今日密码门密码已更新")
            formatted_text = file_text
    return formatted_text

