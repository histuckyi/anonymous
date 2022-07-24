from models.keyword_notification import KeywordNotification


def getNameByKeyword(keyword):
    result = KeywordNotification.query.filter_by(
        keyword=keyword)
    return result.all()
