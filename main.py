import requests
from bs4 import BeautifulSoup

# 静态网站来源
path = 'http://www.fosss.org/Book/ZhuangZi/Index.html'
# 获取页面
r = requests.get(path)
r.encoding = 'utf-8'
raw = BeautifulSoup(r.content, features="html.parser")
raw_content = ''
explanation = ''
record_raw = False
record_explanation = False
needed_useless = False
needed_convertion = False
# 提取所有p标签
for line in raw.find_all('p'):
    # 以“原文”，“译文”，“题解”，“注释”为节点截取文章
    # 并对照
    if '【原文】' in line.get_text():
        record_raw = True
        record_explanation = False
        if len(explanation) > 0:
            if needed_useless:
                with open('useless.txt', 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.writelines(explanation)
                    f.write('\n\n')
                needed_useless = False
            if needed_convertion:
                with open('convertion.txt', 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.writelines(explanation)
                    f.write('\n\n')
                needed_convertion = False
        explanation = ''
        continue
    if '【译文】' in line.get_text():
        record_explanation = True
        continue
    if '【注释】' in line.get_text():
        record_raw = False
        record_explanation = False
        if len(raw_content) > 0:
            if '无用' in raw_content:
                with open('useless.txt', 'a', encoding='utf-8') as f:
                    f.writelines(raw_content)
                needed_useless = True
            if '物化' in raw_content:
                with open('convertion.txt', 'a', encoding='utf-8') as f:
                    f.writelines(raw_content)
                needed_convertion = True
        raw_content = ''
        continue
    if '【题解】' in line.get_text():
        record_raw = False
        record_explanation = False
        if len(explanation) > 0:
            if needed_useless:
                with open('useless.txt', 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.writelines(explanation)
                    f.write('\n\n')
                needed_useless = False
            if needed_convertion:
                with open('convertion.txt', 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.writelines(explanation)
                    f.write('\n\n')
                needed_convertion = False
        explanation = ''
        continue
    if record_raw:
        raw_content = raw_content + str(line.get_text())
    if record_explanation:
        explanation = explanation + str(line.get_text())
