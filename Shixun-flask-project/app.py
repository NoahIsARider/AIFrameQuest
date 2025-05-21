from app import create_app
from utils.faiss_search.faiss_search import process_search_request, initialize_index, IMAGE_FOLDER, UPLOAD_FOLDER
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=5050) 
    initialize_index() # 初始化faiss索引