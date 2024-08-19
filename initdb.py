from server.db import SqlSession

websites = [
    {
        "name": "科教要闻",
        "sites": [
            {"url": "http://www.moe.gov.cn/index.html", "name": "教育部"},
            {"url": "https://www.most.gov.cn/index.html", "name": "科技部"},
            {"url": "http://www.sasac.gov.cn/", "name": "国资委"},
            {"url": "http://www.xinhuanet.com/", "name": "新华网"},
            {"url": "http://www.jyb.cn/", "name": "中国教育新闻网"},
            {"url": "http://www.shedunews.com/", "name": "上海教育新闻网"},
            {"url": "http://www.sciencenet.cn/", "name": "科学网"},
            {"url": "https://news.eol.cn/", "name": "中国教育在线"},
            {"url": "https://edu.cri.cn/", "name": "教育频道_国际在线"},
        ],
    },
    {
        "name": "院校动态",
        "sites": [
            {
                "url": "http://www.moe.gov.cn/jyb_xwfb/s6192/s133/",
                "name": "教育部高校动态",
            },
            {"url": "https://www.pku.edu.cn/", "name": "北京大学"},
            {"url": "https://www.tsinghua.edu.cn/", "name": "清华大学"},
            {"url": "https://www.zju.edu.cn/", "name": "浙江大学"},
            {"url": "https://www.fudan.edu.cn/", "name": "复旦大学"},
            {"url": "https://www.nju.edu.cn/", "name": "南京大学"},
            {"url": "http://www.xjtu.edu.cn/", "name": "西安交通大学"},
            {"url": "http://www.hit.edu.cn/", "name": "哈尔滨工业大学"},
            {"url": "https://www.ustc.edu.cn/", "name": "中国科技大学"},
            {"url": "https://www.ruc.edu.cn/", "name": "中国人民大学"},
        ],
    },
    {
        "name": "国际视野",
        "sites": [
            {"url": "https://www.universityworldnews.com/", "name": "大学世界新闻"},
            {"url": "https://www.findworldedu.cn/", "name": "世界教育新闻网"},
            {"url": "https://www.timeshighereducation.com/", "name": "泰晤士高等教育"},
            {"url": "https://aau.org/", "name": "非洲高等教育之声"},
            {"url": "https://www.princeton.edu/", "name": "普林斯顿大学"},
            {"url": "https://www.stanford.edu/", "name": "斯坦福大学"},
            {"url": "https://www.ox.ac.uk/", "name": "牛津大学"},
            {"url": "https://www.harvard.edu/", "name": "哈佛大学"},
            {
                "url": "https://special.rhky.com/mobile/mooc/tocourse/221495955?user_token=123&fid=&UID=&uf=&vc2=&_industry=&_d=&DSSTASH_LOG=&vc3=&_uid=&vc=",
                "name": "《世界教育动态》",
            },
        ],
    },
]

from common.models import *

with SqlSession() as db:
    for c in websites:
        cate = Category(name=c["name"])
        db.add(cate)
        db.flush()
        # db.refresh(cate)

        for s in c["sites"]:
            site = Site(name=s["name"], url=s["url"], cate_id=cate.id)
            db.add(site)
    db.commit()
print("done")
