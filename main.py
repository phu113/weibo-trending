import os
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import util
from util import logger
from weibo2 import Weibo

def generate_archive_md(searches, topics):
    """生成归档readme
    """
    def search(item):
        if "icon" in item.keys() and "4_0.png" in item['icon']:
            item['desc'] = "爆|" + item['desc'] +  "_" + util.current_date()
        else:
            item['desc'] = item['desc'] +  "_" + util.current_date()
        return '1. [{}]({})'.format(item['desc'], item['scheme'])

    def topic(item):
        detail = ''
        if 'card_expand' in item:
            if 'content' in item['card_expand']:
                detail = item['card_expand']['content']
        return '1. [{}]({})\n    - {}\n'.format(item['title_sub'], item['scheme'], detail)

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    topicMd = '暂无数据'
    if topics:
        topicMd = '\n'.join([topic(item) for item in topics])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{topics}", topicMd)

    return readme


def generate_readme(searches, topics):
    """生成今日readme
    """
    def search(item):
        return '1. [{}]({})'.format(item['desc'], item['scheme'])

    def topic(item):
        detail = ''
        if 'card_expand' in item:
            if 'content' in item['card_expand']:
                detail = item['card_expand']['content']
        return '1. [{}]({})\n    - {}\n'.format(item['title_sub'], item['scheme'], detail)

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    topicMd = '暂无数据'
    if topics:
        topicMd = '\n'.join([topic(item) for item in topics])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{topics}", topicMd)

    return readme


def save_readme(md):
    logger.debug('readme:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.debug('archive md:%s', md)
    name = '{}.md'.format(util.current_first_date_week())
    file = os.path.join('archives', name)
    util.append_text(file, md)


# def save_raw_content(content: str, filePrefix: str):
#     filename = '{}-{}.json'.format(filePrefix, util.current_date())
#     file = os.path.join('raw', filename)
#     util.write_text(file, content)

def delete_old_files():
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the date 6 months ago
    six_months_ago = current_date - relativedelta(months=6)
    
    # Format the result as a string in YYYY-MM format
    six_months_ago_str = six_months_ago.strftime('%Y-%m')
    
    # Iterate over the files in the folder
    for filename in os.listdir("archives"):
        file_path = os.path.join("archives", filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):           
            # If the file's name include 6 months before, 
            # delete it(only delete that month file)
            if six_months_ago_str in filename:
                os.remove(file_path) # os.remove('archives/2024-09-01.md')

def run():
    weibo = Weibo()
    # 热搜
    searches, resp = weibo.get_hot_search()

    # 话题榜
    topics, resp = weibo.get_hot_topic()

    # if resp:
    #     save_raw_content(resp.text, 'hot-search')
    # if resp:
    #     save_raw_content(resp.text, 'hot-topic')

    # 最新数据
    readme = generate_readme(searches, topics)
    save_readme(readme)
    # 归档
    archiveMd = generate_archive_md(searches, topics)
    save_archive_md(archiveMd)
    delete_old_files()


if __name__ == "__main__":
    run()
