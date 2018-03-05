import re


# url = '😱屏幕好像没有店家发的图看起来大，但总体还不错啊😱'

def filter_emoji(desstr, restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


url = '😱屏幕好像没😁有店家发的图看起来大，但总体还不错啊😱'
# url = '吖'
url = filter_emoji(url)
print(filter_emoji(url))
