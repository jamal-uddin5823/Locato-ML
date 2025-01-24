# recommender.py

import numpy as np
from sklearn.neighbors import NearestNeighbors
from fastapi import HTTPException
from app.crud import get_user_queries
from app.models import UserQuery

def recommend_queries(user_id: int, db):
    # Step 1: Get all users' queries
    user_queries = get_user_queries(db, user_id)

    if not user_queries:
        raise HTTPException(status_code=404, detail="No queries found for the user.")
    
    # Step 2: Create user-query interaction matrix
    user_ids = list(set([uq.user_id for uq in user_queries]))
    query_ids = list(set([uq.query_id for uq in user_queries]))

    interaction_matrix = np.zeros((len(user_ids), len(query_ids)))

    for i, user in enumerate(user_ids):
        for j, query in enumerate(query_ids):
            interaction_matrix[i][j] = 1 if any(uq.user_id == user and uq.query_id == query for uq in user_queries) else 0

    # Step 3: Apply KNN to find similar users
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(interaction_matrix)

    user_idx = user_ids.index(user_id)
    _, indices = knn.kneighbors([interaction_matrix[user_idx]])

    # Step 4: Recommend the most common queries from similar users
    recommended_queries = []
    for idx in indices[0]:
        recommended_queries.extend([query_ids[j] for j in range(len(query_ids)) if interaction_matrix[idx][j] == 1])

    recommended_queries = list(set(recommended_queries))
    return recommended_queries[:5]


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_similar_queries(user_queries, db):
    # Fetch all queries and their text from the database
    all_queries = db.query(UserQuery.query_text).all()
    
    # Convert queries to embeddings or a vector representation, for simplicity, let’s assume we use TF-IDF
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Combine user queries with all queries
    queries = [q.query_text for q in user_queries] + [q.query_text for q in all_queries]
    tfidf_matrix = tfidf.fit_transform(queries)
    
    # Calculate cosine similarity between the user's queries and all queries in the database
    similarity_matrix = cosine_similarity(tfidf_matrix[:len(user_queries)], tfidf_matrix[len(user_queries):])
    
    # Get the top N most similar queries
    similar_queries_idx = np.argsort(similarity_matrix.flatten())[-5:][::-1]
    print(similar_queries_idx)
    similar_queries = [all_queries[(i)%len(all_queries)] for i in similar_queries_idx]
    unique_similar_queries = []
    seen_query_texts = set()

    for query in similar_queries:
        if query.query_text not in seen_query_texts:
            unique_similar_queries.append(query)
            seen_query_texts.add(query.query_text)

    similar_queries = unique_similar_queries
    return unique_similar_queries
