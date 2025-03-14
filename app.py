
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, clicks INTEGER, time_spent INTEGER, visits INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS reviews (id TEXT, review TEXT, rating INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
conn.commit()

class UserActivity(BaseModel):
    userId: str
    clicks: int
    timeSpent: int
    visits: int

class UserReview(BaseModel):
    userId: str
    review: str
    rating: int

@app.post("/track")
def track_user(data: UserActivity):
    try:
        cursor.execute("INSERT INTO users (id, clicks, time_spent, visits) VALUES (?, ?, ?, ?)",
                       (data.userId, data.clicks, data.timeSpent, data.visits))
        conn.commit()
        return {"message": "Data recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review")
def submit_review(data: UserReview):
    try:
        cursor.execute("INSERT INTO reviews (id, review, rating) VALUES (?, ?, ?)",
                       (data.userId, data.review, data.rating))
        conn.commit()
        return {"message": "Review submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)}

@app.get("/reviews", response_model=List[UserReview])
def get_reviews():
    cursor.execute("SELECT id, review, rating FROM reviews ORDER BY timestamp DESC")
    reviews = cursor.fetchall()
    return [{"userId": r[0], "review": r[1], "rating": r[2]} for r in reviews]
