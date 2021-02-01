from dateutil.parser import parse


def find_page_data_on_page(my_soup):
	try:
		PageId = my_soup.find("a", "next-page").get('href').replace('?from=', '')
		PageUrl = str("https://conspiracies.win/?from=" + PageId)
		return PageId, PageUrl
	except Exception:
		print("error on: find_page_data_on_page")


def find_post_data_on_page(my_soup):
	try:
		Posts = []
		for post in my_soup.find_all("div", "post"):
			Post = {'PostID'       : post.get('data-id'), 'PostAuthor': post.get('data-author'),
					'PostTitle'    : post.find("div", "top").a.get_text().replace('\n', ' ').replace('\t', '').strip(),
					'PostLink'     : post.find("div", "top").a.get('href'),
					'PostScore'    : int(post.find("div", "vote").get_text().strip()), 'PostComments': int(
					post.find("a", "comments").get_text().replace('comments', '').replace('comment', '').strip()),
					'PostTimeStamp': str(parse(post.find("time", "timeago").get("title")))}

			Posts.append(Post)
		return Posts

	except Exception:
		print("error on: find_post_data_on_page")
		return False


def parse_page(my_soup):
	try:
		PageSoup = find_page_data_on_page(my_soup)
		PostSoup = find_post_data_on_page(my_soup)
		Page = {
			'PageId' : PageSoup[0],
			'PageUrl': PageSoup[1],
			'Posts'  : PostSoup
		}
		return Page

	except Exception:
		return False
