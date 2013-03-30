def get_last_articles():
	from howmuch.article.models import Article
	articles = Article.objects.all()[:10]
	return articles
