import os
import psycopg2
from dotenv import load_dotenv

# Loading ENV variables
load_dotenv()

db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")

# connect to postgreSQL server using only psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host=db_host, user=db_user, database=db_name, password=db_pwd, cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database Connection Successful")
#         break
    
#     except Exception as e:
#         print(f"Error {e} occurred")


# # Getting all posts from DB
# @app.get("/post")
# def get_posts(db: Session = Depends(get_db)):
    
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# # Creating a Post
# @app.post("/create-post", status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):

#     cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
#                 (post.title, post.content, post.published)
#     )

#     new_post = cur.fetchone()
#     conn.commit()

#     # print(f"{post.number}, {post.publish}, {post.rating}")
#     # print(post.model_dump())  # converting pydantic model to dict (.dict() deprecated)

#     return {"Data": new_post}


# # Getting a single posts from DB
# @app.get("/get-post/{id}")
# def get_post(id:int, response:Response):

#     cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
#     post = cur.fetchone()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found" )
#         # response.status_code = status.HTTP_404_NOT_FOUND

#     return {"Post_details":post}



# # DELETING A POST
# @app.delete("/delete/{id}")
# def delete_post(id:int):

#     cur.execute("DELETE FROM posts WHERE id = %s", (id,))
#     deleted_post = cur.fetchone()
#     conn.commit()

#     # Check if post was deleted
#     if deleted_post == None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"post with id: {id} was not found")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

    
# # Updating the DB
# @app.put("/update/{id}")
# def update_post(id:int, post:Post):

#     cur.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",
#                 (post.title, post.content, post.published, id))
    
#     updated_post = cur.fetchone()
#     conn.commit()

#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
    
#     return {"Updated Post":post}


# # Closing all connections
# # cur.close()
# # conn.close()

 