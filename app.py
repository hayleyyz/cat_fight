from flask import Flask, request, jsonify, render_template
import video_processor
import frame_inference
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-profile', methods=['POST'])
def generate_profile():
    print("Received request at /generate-profile")
    
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        temp_dir = tempfile.gettempdir()
        filename = secure_filename(file.filename)
        temp_video_path = os.path.join(temp_dir, filename)
        
        file.save(temp_video_path)
        print(f"Video saved temporarily to {temp_video_path}")

        try:
            print("Extracting cat portraits...")
            cat_portraits = video_processor.extract_cat_portraits(temp_video_path)
            
            if not cat_portraits:
                raise ValueError("No cats were detected in the video.")
            print(f"Successfully extracted {len(cat_portraits)} cat portrait(s).")

            fighter_profiles = []
            for portrait in cat_portraits:
                profile_data = frame_inference.generate_fighter_profile([portrait])
                
                profile_data['image_frame'] = portrait
                fighter_profiles.append(profile_data)
            
            print(f"Successfully generated {len(fighter_profiles)} profile(s).")

            return jsonify(fighter_profiles), 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        
        finally:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                print(f"Cleaned up temporary file: {temp_video_path}")

    return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
