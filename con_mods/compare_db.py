from con_mods import db_util


class DB:
	def __init__(self, PostID):
		self.PostID = db_util.select_PostID(PostID)['PostID']
		self.PostComments = db_util.select_PostID(PostID)['PostComments']


def update_post_db(PageSoup):
	Missing = []

	for post in PageSoup['Posts']:
		MissingPost = {}
		PostID = post['PostID']
		PostComments = db_util.count_comments(PostID)
		# creates class for db values
		db = DB(PostID)

		if db.PostID != PostID or db.PostComments > PostComments:
			MissingPost['PostID'] = PostID
			MissingPost['Link'] = post['PostLink']
			Missing.append(MissingPost)
			db_util.insert_post_tbl(post)
		else:
			pass

	return Missing
