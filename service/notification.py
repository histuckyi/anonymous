from query import keyword_noti_query
from util.keyword_analyzer import KeywordAnalyzer


def notify(text):
    keyword_list = KeywordAnalyzer().extract_keyword(text)
    noti_user_list = set()
    for keyword in keyword_list['termAtt']:
        users = keyword_noti_query.getNameByKeyword(keyword)
        names = [user.name for user in users]
        noti_user_list = noti_user_list.union(names)
    # 키워드를 등록한 유저에게 알림 전송
    print("notify to noti_user_list")
