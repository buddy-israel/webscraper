from dateutil.parser import parse


def parse_comments(my_soup):
	Comments = []
	CommentList = my_soup.find("section", "comment-list")

	for comment in CommentList.find_all("div", "comment"):
		Comment = {}
		CommentAuthor = comment.find("a", "author")
		if CommentAuthor is None:
			Comment['CommentAuthor'] = comment.find("span", "author").get_text().strip()
			Comment['CommentContent'] = str("deleted")
			Comment['CommentId'] = None
		else:
			Comment['CommentAuthor'] = CommentAuthor.get_text().strip()
			Comment['CommentContent'] = comment.find("div", "content").get_text().replace('\n', ' ').replace('\t',
																											 '').strip()
			Comment['CommentId'] = comment.find("div", "actions").a.get("href")

		Comment['CommentScore'] = int(comment.find("div", "vote").find("span", "count").get_text().strip())
		Comment['CommentTimestamp'] = str(parse(comment.find("time", "timeago").get("title")))

		Comments.append(Comment)

	return Comments


def parse_post(my_soup):
	PostBody = my_soup.main.find("div", "post")
	Post = {'PostID'    : my_soup.main.find("div", "post")['data-id'],
			'PostAuthor': my_soup.main.find("div", "post")['data-author'],
			'PostTitle' : PostBody.find("div", "top").a.get_text().replace('\n', ' ').replace('\t', '').strip()}

	try:
		if PostBody.find("div", "content text") is not None:
			Post['PostContent'] = PostBody.find("div", "content text").find("div", "clean").get_text()

		elif PostBody.find("div", "content link") is not None:
			Post['PostContent'] = PostBody.find("div", "content link").find("div", "video-container")['data-src']

		elif PostBody.find("div", "details") is not None:
			Post['PostContent'] = PostBody.find("a", "expand-link").get("href")

		else:
			Post['PostContent'] = None
	except:
		Post['PostContent'] = None

	Post['Comments'] = parse_comments(my_soup)
	return Post
