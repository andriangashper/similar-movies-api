from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from data import get_data, mod_data

app = Flask(__name__)
CORS(app)

app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)


def update_and_cache_data(cache, key, data, timeout):
    cache.delete(key)
    cache.set(key, data, timeout = timeout)


@app.route("/movies/update_data", methods = ["POST"])
def update_movies_inmemory_data():
    timeout = 604800
    try:
        movies_raw_data = get_data.get_movies_table_data()
        similarity_matrix = mod_data.similarity_matrix_between_movies(movies_raw_data)
        edges = mod_data.get_movies_network_edges(movies_raw_data, similarity_matrix)
        nodes = mod_data.get_movies_network_nodes(movies_raw_data, edges)

        update_and_cache_data(cache, "movies_raw_data", movies_raw_data, timeout)
        update_and_cache_data(cache, "edges", edges, timeout)
        update_and_cache_data(cache, "nodes", nodes, timeout)

        return jsonify({"Message": "In-memory variables updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movies/graph_data", methods = ["GET"])
def get_movies_graph_data():
    nodes = cache.get("nodes")
    edges = cache.get("edges")
    movie_id = int(request.args.get("movie_id"))

    if nodes and edges and movie_id:
        if movie_id != -1:
            nodes, edges = mod_data.get_filtered_movies_network_nodes_and_edges(nodes, edges, movie_id)
        return jsonify({"nodes":nodes, "edges":edges}), 200
    
    else:
        return jsonify({"error": "Variables not available."}), 404


@app.route("/movies/nsimilar_movies", methods = ["GET"])
def get_topn_similar_movies():
    try:
        movies_raw_data = cache.get("movies_raw_data")
        input_text = str(request.args.get("input_text"))
        n = max(int(request.args.get("n")),1)

        if movies_raw_data and input_text and n:
            topn_similar_movies = mod_data.topn_similar_movies_to_input(input_text, movies_raw_data, n)
            return jsonify({"data":topn_similar_movies}), 200
        
        else:
            return jsonify({"error": "Variables not available."}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def calls_on_startup():
    with app.test_client() as client:
        response = client.post("/movies/update_data")
        print(response.data)


if __name__ == "__main__":
    calls_on_startup()
    app.run(debug=True, host="0.0.0.0", port=8000)