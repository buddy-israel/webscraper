import sqlite3

Database = "./Con.db"
conn = sqlite3.connect(Database)


# #################################### #
# #################################### #


def drop_tables():
	print("drop_tables")
	c = conn.cursor()

	try:
		c.execute("DROP TABLE post_tbl")
	except:
		pass

	try:
		c.execute("DROP TABLE comment_tbl")
	except:
		pass
	conn.commit()


def reset_tables():
	print("reset_tables")

	try:
		drop_tables()
	except:
		pass
	create_post_tbl()


def alter_table():
	c = conn.cursor()
	c.execute("""
		ALTER TABLE
			post_tbl
		ADD COLUMN
			PostContent VARCHAR
			""")
	conn.commit()
	return True


# create_comment_tbl()


# #################################### #
# #################################### #


def create_post_tbl():
	c = conn.cursor()
	c.execute("""
	CREATE TABLE IF NOT EXISTS
		post_tbl (
			PostID VARCHAR PRIMARY KEY UNIQUE,
			PostAuthor VARCHAR,
			PostTitle VARCHAR,
			PostLink VARCHAR,
			PostScore INTEGER,
			PostComments INTEGER,
			PostTimeStamp VARCHAR,
			PostContent VARCHAR
			)""")
	conn.commit()


def select_PostID(PostID):
	c = conn.cursor()
	c.execute("""
		SELECT
			PostID,
			PostComments
		FROM
			post_tbl
		WHERE
			:PostID=PostID
		""", {'PostID': PostID})

	r = c.fetchone()
	if r is None:
		return {'PostID': None, 'PostComments': None}
	else:
		return {'PostID': r[0], 'PostComments': r[1]}


def insert_post_tbl(post):
	c = conn.cursor()
	c.execute("""
			INSERT OR IGNORE INTO
				post_tbl 
			VALUES (
				:PostID,
				:PostAuthor,
				:PostTitle,
				:PostLink,
				:PostScore,
				:PostComments,
				:PostTimeStamp,
				:PostContent
				) """, {
		'PostID'       : post['PostID'],
		'PostAuthor'   : post['PostAuthor'],
		'PostTitle'    : post['PostTitle'],
		'PostLink'     : post['PostLink'],
		'PostScore'    : post['PostScore'],
		'PostComments' : post['PostComments'],
		'PostContent'  : None,
		'PostTimeStamp': post['PostTimeStamp']})
	conn.commit()
	return True


def update_comment_on_posts(PostID, PostComments):
	c = conn.cursor()
	c.execute("""
		UPDATE 
			post_tbl
		SET
			:PostComments=PostComments 
		WHERE
			:PostID=PostID
		""", {
		'PostID'      : PostID,
		'PostComments': PostComments})
	conn.commit()
	return True


def update_PostContent(PostID, PostContent):
	c = conn.cursor()
	c.execute("""
		UPDATE
			post_tbl
		SET
			PostContent = :PostContent
		WHERE
			:PostID=PostID
		""", {
		'PostID'     : PostID,
		'PostContent': PostContent
	})
	conn.commit()
	return True


def count_posts():
	c = conn.cursor()
	c.execute("""
		SELECT
			COUNT(*)
		FROM
			post_tbl
		""")
	return c.fetchall()


def select_Post(PostID):
	c = conn.cursor()
	c.execute("""
		SELECT
			*
		FROM
			post_tbl
		WHERE
			:PostID=PostID
		""", {'PostID': PostID})
	return c.fetchall()


# #################################### #
# #################################### #


def create_comment_tbl():
	c = conn.cursor()
	c.execute("""
	CREATE TABLE IF NOT EXISTS
		comment_tbl (
			CommentId VARCHAR PRIMARY KEY UNIQUE,
			PostID VARCHAR,
			CommentScore VARCHAR,
			CommentAuthor VARCHAR,
			CommentContent VARCHAR,
			CommentTimestamp VARCHAR,
		FOREIGN KEY
			(PostID)
		REFERENCES 
			post_tbl (PostID)
			)""")
	conn.commit()


def insert_comment_tbl(PostID, comment):
	c = conn.cursor()
	c.execute("""
			INSERT OR IGNORE INTO
				comment_tbl 
			VALUES (
				:CommentId,
				:PostID,
				:CommentScore,
				:CommentAuthor,
				:CommentContent,
				:CommentTimestamp
				) """, {
		'CommentId'       : comment['CommentId'],
		'CommentScore'    : comment['CommentScore'],
		'CommentAuthor'   : comment['CommentAuthor'],
		'CommentContent'  : comment['CommentContent'],
		'CommentTimestamp': comment['CommentTimestamp'],
		'PostID'          : PostID
	})
	conn.commit()
	return True


def count_comments(PostID):
	c = conn.cursor()
	c.execute("""
		SELECT
			COUNT(*)
		FROM
			comment_tbl
		WHERE
			:PostID=PostID
		""", {'PostID': PostID})
	return c.fetchall()[0][0]


def count_all_comments():
	c = conn.cursor()
	c.execute("""
		SELECT
			COUNT(*)
		FROM
			comment_tbl
		WHERE
			CommentId
		IS NOT NULL
		""")
	return c.fetchall()[0][0]
