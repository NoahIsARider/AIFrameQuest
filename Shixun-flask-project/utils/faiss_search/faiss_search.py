import os
import numpy as np
import faiss
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import glob

# Set environment variable to handle OpenMP runtime conflict
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Configuration
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'images')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads')
# Use a simple ASCII path for the index file to avoid issues with non-ASCII characters
INDEX_PATH = os.path.join('D:\\', 'faiss_index.index')
TOP_K = 10  # Number of similar images to retrieve

# Global variables to store the index and image files in memory
global_index = None
global_image_files = []
index_built = False

# Create necessary folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)  # Ensure index directory exists

# Load pre-trained model (ResNet-50)
def get_model():
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    # Remove the last fully connected layer (classification layer)
    model = torch.nn.Sequential(*list(model.children())[:-1])
    model.eval()  # Set to evaluation mode
    return model

# Image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Extract features from an image
def extract_features(img_path, model):
    img = Image.open(img_path).convert('RGB')
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    
    with torch.no_grad():
        features = model(batch_t)
    
    # Reshape and convert to numpy array
    features = features.reshape(-1).numpy()
    return features

# Load the Faiss index
def load_index():
    global global_index, global_image_files, index_built
    
    # If index is already loaded in memory, return it
    if global_index is not None:
        return global_index
    
    try:
        if not os.path.exists(INDEX_PATH):
            print(f"Index file not found at {INDEX_PATH}")
            return None
            
        index = faiss.read_index(INDEX_PATH)
        print(f"Loaded index with {index.ntotal} vectors")
        global_index = index
        return index
    except Exception as e:
        print(f"Error loading index: {e}")
        return None

# Build the index if it doesn't exist
def build_index():
    global global_index, global_image_files, index_built
    
    # If index is already built, return it
    if index_built and global_index is not None:
        print("Index already built and loaded in memory")
        return global_index, global_image_files
    
    try:
        model = get_model()
        image_files = glob.glob(os.path.join(IMAGE_FOLDER, '*.jpg'))
        
        if not image_files:
            print(f"No image files found in {IMAGE_FOLDER}")
            return None, []
        
        print(f"Found {len(image_files)} images for indexing")
        
        # Get the dimension of feature vectors
        sample_features = extract_features(image_files[0], model)
        dimension = len(sample_features)
        
        # Create a new index
        index = faiss.IndexFlatL2(dimension)
        
        # Extract features and add to index
        all_features = []
        valid_image_files = []
        
        for i, img_path in enumerate(image_files):
            try:
                features = extract_features(img_path, model)
                all_features.append(features)
                valid_image_files.append(img_path)
                if i % 100 == 0:
                    print(f"Processed {i}/{len(image_files)} images")
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        if not all_features:
            print("No valid features extracted from images")
            return None, []
        
        # Convert to numpy array and add to index
        all_features = np.array(all_features).astype('float32')
        index.add(all_features)
        
        # Save the index with better error handling
        try:
            print(f"Attempting to save index to {INDEX_PATH}")
            # Create a temporary directory with a simple ASCII name if needed
            index_dir = os.path.dirname(INDEX_PATH)
            os.makedirs(index_dir, exist_ok=True)
            
            # Try to save the index
            faiss.write_index(index, INDEX_PATH)
            print(f"Successfully saved index with {index.ntotal} vectors")
        except Exception as e:
            print(f"Error saving index: {e}")
            print("Continuing with in-memory index only")
            # Return the index even if we couldn't save it
            return index, valid_image_files
        
        # Store in global variables
        global_index = index
        global_image_files = valid_image_files
        index_built = True
        
        return index, valid_image_files
    except Exception as e:
        print(f"Unexpected error in build_index: {e}")
        return None, []

# Search for similar images
def search_similar_images(query_features, index, image_files, k=TOP_K):
    # Reshape query features for Faiss
    query_features = query_features.reshape(1, -1).astype('float32')
    
    # Search the index
    distances, indices = index.search(query_features, k)
    
    # Get the image paths for the results
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(image_files):
            results.append({
                'image': f'/static/uploads/{os.path.basename(image_files[idx])}',
                'distance': float(distances[0][i])
            })
    
    return results

# Function to handle the search request
def process_search_request(file):
    global global_index, global_image_files
    
    # Save the uploaded image
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)
    
    # Load the model and extract features
    model = get_model()
    query_features = extract_features(upload_path, model)
    
    # Use global index if available, otherwise load or build it
    index = global_index
    image_files = global_image_files
    
    if index is None:
        # Try to load the index from disk
        index = load_index()
        image_files = glob.glob(os.path.join(IMAGE_FOLDER, '*.jpg'))
    
    if index is None:
        # If still None, build the index
        print("Building index...")
        index, valid_image_files = build_index()
        if index is None:
            return {'error': 'Failed to build index. Please check server logs.'}, 500
        image_files = valid_image_files
    
    # Search for similar images
    results = search_similar_images(query_features, index, image_files)
    
    return {
        'query_image': file.filename,
        'results': results
    }

# Initialize the index
def initialize_index():
    global global_index, global_image_files
    print("Initializing the index...")
    global_index, global_image_files = build_index()
    if global_index is not None:
        print("Index successfully built and loaded in memory")
        return True
    else:
        print("Failed to build index at startup. Will try again when needed.")
        return False