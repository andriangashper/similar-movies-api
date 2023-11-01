import numpy as np
from scipy import spatial
from sys import getsizeof
import time
from .get_data import vectorize_text, get_movies_vector_matrix, get_movies_table_data
from .variables import NODES_DATA_COLUMNS, MIN_COS_SIM_SCORE
from .logging_config import configure_logger

logger = configure_logger(__name__)


def cosine_similarity_scipy(l1,l2):
    return 1 - spatial.distance.cosine(l1,l2)


def topn_similar_movies_to_input(input_text, movies_raw_data, n):
    vectorized_input = vectorize_text(input_text)
    vector_matrix = get_movies_vector_matrix(movies_raw_data, include_genres=False)

    cos_similarities = [cosine_similarity_scipy(vectorized_input, vector) for vector in vector_matrix]

    indexed_cos_similarities = list(enumerate(cos_similarities))
    sorted_cos_similarities = sorted(indexed_cos_similarities, key = lambda x: x[1], reverse=True)
    indexes_of_topn_similar_movies = [index for index, _ in sorted_cos_similarities[:n]]

    logger.info(f"Topn similar movies function was triggered. It returned {len(indexes_of_topn_similar_movies)} movies")

    return [{key:movies_raw_data[i][key] 
             for key in movies_raw_data[i] if key in NODES_DATA_COLUMNS}|
             {"cos_sim":round(indexed_cos_similarities[i][1],2)} 
             for i in indexes_of_topn_similar_movies]


def similarity_matrix_between_movies(movies_raw_data):
    vector_matrix_np = np.array(get_movies_vector_matrix(movies_raw_data, include_genres=True))

    norms = np.linalg.norm(vector_matrix_np, axis=1)
    normalized_matrix = vector_matrix_np / norms[:, np.newaxis]
    similarity_matrix = np.dot(normalized_matrix, normalized_matrix.T)
    similarity_matrix[np.tril_indices_from(similarity_matrix)] = 0

    logger.info(f"Generated similarity matrix, with dim: {len(similarity_matrix)}x{len(similarity_matrix[0])}," + 
                f" and size: {round(getsizeof(similarity_matrix)/1000000,2)} MB")

    return similarity_matrix


def get_movies_network_edges(movies_raw_data, similarity_matrix):
    idx_i, idx_j = np.where(similarity_matrix > MIN_COS_SIM_SCORE)

    edges = [{"from": movies_raw_data[i]["id"], "to": movies_raw_data[j]["id"], "cos_sim":round(similarity_matrix[i,j],2)} \
             for i, j in zip(idx_i, idx_j)]
    
    logger.info(f"Generated {len(edges):,} network edges, and size: {round(getsizeof(edges)/1000000,2)} MB")

    return edges


def get_movies_network_nodes(movies_raw_data, edges):
    unique_node_ids = set(edge["from"] for edge in edges) | set(edge["to"] for edge in edges)
    nodes = [{key: movie[key] for key in movie if key in NODES_DATA_COLUMNS} \
             for movie in movies_raw_data if movie["id"] in unique_node_ids]
    
    logger.info(f"Generated {len(nodes)} network nodes, and size: {round(getsizeof(nodes)/1000000,2)} MB")

    return nodes


def get_filtered_movies_network_nodes_and_edges(movies_raw_data, edges, movie_id):
    edges = [edge for edge in edges if movie_id in [edge["from"], edge["to"]]]
    nodes = get_movies_network_nodes(movies_raw_data, edges)

    return nodes, edges


def get_top_n_similar_movies_to_movie_id(movie_id, filtered_nodes, filtered_edges, top_n):

    similarity_dict = similarity_dict = {edge["from"] if edge["from"] != movie_id else edge["to"]: edge["cos_sim"] for edge in filtered_edges}

    nodes = [node | {"cos_sim" : similarity_dict[node["id"]]} for node in filtered_nodes if node["id"] != movie_id] 

    nodes  = sorted(nodes, key = lambda x: x["cos_sim"], reverse=True)

    return nodes[:top_n]                         


def time_function(function, *args):
    start = time.perf_counter()
    function_result = function(*args)
    time_elapsed = (time.perf_counter() - start)    
    print("%5.1f secs" % (time_elapsed))
    
    return function_result



if __name__ == "__main__":
    
    movies_raw_data = time_function(get_movies_table_data)

    top_N_movies = time_function(topn_similar_movies_to_input,"Movie about a girl who used to ski but now she runs high stakes poker games", movies_raw_data, 3)
    logger.info(f"Top N movies info\n{top_N_movies}")

    similarity_matrix = time_function(similarity_matrix_between_movies, movies_raw_data)
    
    edges = time_function(get_movies_network_edges, movies_raw_data, similarity_matrix)
    
    nodes = time_function(get_movies_network_nodes, movies_raw_data, edges)

    django_movie_id = [node["id"] for node in nodes if "django" in node["name"].lower()][0]

    logger.info("Filtering nodes and edges")
    filtered_nodes, filtered_edges = time_function(get_filtered_movies_network_nodes_and_edges, movies_raw_data, edges, django_movie_id)
    logger.info(f"Django filtered nodes:\n{filtered_nodes}\nand edges:\n{filtered_edges}")