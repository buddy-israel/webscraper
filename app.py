from con_mods import util, page_parser, compare_db, db_util, post_parser


def run(url):
	# [1] request and save first page
	s = util.send_request(url)
	util.save("./Files/page.html", s)

	# [2] parse first page
	my_page = util.open_file("./Files/page.html")
	Page = page_parser.parse_page(my_page)

	# [3] check what posts are already in DB
	Missing = compare_db.update_post_db(Page)
	# print(json.dumps(Missing, indent=4))

	# [4] request missing posts
	for m in Missing:
		url = str("https://conspiracies.win" + str(m['Link']))
		print(url)
		s = util.send_request(url)
		util.save("./Files/post.html", s)

		# [5] parse missing posts
		my_soup = util.open_file("./Files/post.html")
		Post = post_parser.parse_post(my_soup)

		# [6] insert post content into post tables
		db_util.update_PostContent(Post['PostID'], Post['PostContent'])

		# [7] insert comments content into comment tables
		for comment in Post['Comments']:
			db_util.insert_comment_tbl(Post['PostID'], comment)

	print(db_util.count_all_comments())

	# [8] return url for next page
	print(Page['PageUrl'])
	return Page['PageUrl']


def main():
	url = "https://conspiracies.win/new"

	i = 0

	while True:
		print("starting Page:", i)
		PageSoup = run(url)
		if not PageSoup:
			print("error")
			break
		else:
			print("completed Page:", i)
			url = PageSoup
			i = i + 1


main()
