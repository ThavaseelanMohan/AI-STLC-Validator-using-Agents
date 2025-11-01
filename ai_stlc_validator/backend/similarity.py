from sentence_transformers import SentenceTransformer, util
import numpy as np

# Lightweight open embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity_score(requirement, testcase_df):
    """Compute similarity between requirement and all test cases using SentenceTransformer"""
    req_emb = model.encode(requirement, convert_to_tensor=True)
    tc_embs = model.encode(testcase_df["TestCase_Description"].astype(str).tolist(), convert_to_tensor=True)

    cosine_scores = util.cos_sim(req_emb, tc_embs)[0]
    best_idx = int(np.argmax(cosine_scores))
    best_tc = testcase_df.iloc[best_idx]["TestCase_Description"]
    best_score = float(cosine_scores[best_idx])

    return best_tc, round(best_score, 3)
