from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import socket
import json
import time
import select
import requests
import os
import cv2
import shutil
import boto3
import json
from xml.dom.minidom import parseString
from botocore.exceptions import ClientError

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
IMAGE_NAME = "baby.png"

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

app = Flask(__name__)
CORS(app)
client = None

'''vitals = {
    'time': [],
    'heartbeat': [],
    'temperature': [],
    'breathing': [],
    'heartbeat_minmax': [0, 0],
    'temperature_minmax': [0, 0],
    'breathing_minmax': [0, 0]
}'''

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ai_dangers_record = []
frames = []
seconds = 20

img_ai_resp = dict()
hume_resp = dict()

@app.route('/vitals-data')
def get_vitals_data():
    # Generate some random data for the line chart
    #data = []

    response = requests.get('http://localhost:9999/data')
    #print(response.json())
    #vitals = json.loads(response.json())
    vitals = response.json()
    global seconds
    seconds = len(vitals) // 1
    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print('Failed to fetch data')



    data = [["Time", "BPM", "Temperature", "Point"]] + [
        #[float(vitals['time'][i]), float(vitals['heartbeat'][i], float(vitals['temperature'][i]))] for i in len(range(vitals['time']))
        [float(vital[0]), float(vital[1]), float(vital[2]), -1000 if vital[3] == None else float(vital[3])] for vital in vitals
    ]
    #print(data)
    return jsonify(data)
    #return data

def calculate_distress_index(emo):
    sum_distress = 0.0
    for e in emo:
        if e['name'] == 'Anger' or e['name'] == 'Anxiety' or e['name'] == 'Confusion' or e['name'] == 'Pain' or e['name'] == 'Surprise (negative)':
            sum_distress += e['score']
        elif e['name'] == 'Distress' or e['name'] == 'Fear' or e['name'] == 'Horror':
            sum_distress += e['score'] * 2
    return 10 * sum_distress / 8

def get_ai_opinions(current_frame, SECOND):
    return [SECOND+1, random.randint(50, 80), random.randint(50, 80), random.randint(50, 80), random.randint(50, 80), random.randint(50, 80), random.randint(50, 80), -1000]
    if current_frame == None:
        return [SECOND+1, -1000, -1000, -1000, -1000, -1000, -1000, -1000]
    response_text = None
    hume_distress = None
    if current_frame in img_ai_resp:
        response_text = img_ai_resp[current_frame]
    else:
        frame_name = os.path.join('opencv', f'frame{current_frame}.jpg')
        with open(frame_name, "rb") as f:
            image = f.read()

        ml_prompt = ml_prompt = """
            For each hazard, provide a rating from 1 (lowest) to 10 (highest) to indicate the level of risk to the baby in the picture.\n
            For the rationale, you will explain why you give the rate of each factor and how dangerous the factors are on the subject baby IF AND ONLY IF you gave it a rating of 7 or above. If all ratings are below 7, simply state None.\n
            Output format:
            {
                choking: <integer>,
                electrical_shock: <integer>,
                hard_falling: <integer>,
                suffocation: <integer>,
                sharp_objects: <integer>,
                rationale: <string>
            }"""

        messages = [
            {
                "role": "user",
                "content": [
                    {"image": {"format": "png", "source": {"bytes": image}}},
                    {"text": ml_prompt},
                ],
            }
        ]

        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=messages,
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        img_ai_resp[current_frame] = response_text
    print(response_text)

    if current_frame in hume_resp:
        hume_distress = hume_resp[current_frame]
    else:
        image_path = os.path.join('opencv', f'frame{current_frame}.jpg')
        API_KEY = 'jzxNrIzPdz2FovYG4DkBj00fW2ijG6KHUa35Hdp8dDChHA2M'

        try:
            print("Creating job...")
            with open(image_path, 'rb') as file:
                files = {
                    'file': (image_path, file, 'image/png')
                }
                response = requests.post(
                    "https://api.hume.ai/v0/batch/jobs",
                    headers={
                        "X-Hume-Api-Key": API_KEY
                    },
                    files=files
                )

            print("Response status code:", response.status_code)
            print("Response headers:", response.headers)
            print("Response text:", response.text)


            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                response_data = response.json()
                if 'job_id' in response_data:
                    job_id = response_data['job_id']
                    print(f"Job created with ID: {job_id}")

                    print("Waiting for job to complete...")
                    time.sleep(4) 

                    # Fetch predictions from the job
                    url = f'https://api.hume.ai/v0/batch/jobs/{job_id}/predictions'
                    headers = {
                        'X-Hume-Api-Key': API_KEY
                    }
                    predictions_response = requests.get(url, headers=headers)


                    if predictions_response.status_code == 200:
                        predictions = predictions_response.json()
                        print(json.dumps(predictions, indent=2))
                    else:
                        print(f"Failed to fetch predictions. Status code: {predictions_response.status_code}")
                        hume_distress = -1000
                else:
                    raise KeyError(f"Job ID not found in response: {response_data}")
            else:
                raise ValueError(f"Unexpected response format or status: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred with the request: {e}")
            hume_distress = -1000
        except KeyError as e:
            print(e)
            hume_distress = -1000
        except ValueError as e:
            print(e)
            hume_distress = -1000
        except Exception as e:
            print(f"An error occurred: {e}")
            hume_distress = -1000
        try:
            hume_distress = calculate_distress_index(predictions[0]['results']['predictions'][0]['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions'])
        except:
            hume_distress = -1000
    try:
        res = json.loads(response_text)
    except:
        return (SECOND+1, -1000, -1000, -1000, -1000, -1000, hume_distress, None)
    return (SECOND+1, res['choking'], res['electrical_shock'], res['hard_falling'], res['suffocation'], res['sharp_objects'], hume_distress, None)
    #return [current_frame, random.randint(50, 80), random.randint(50, 80), random.randint(50, 80)]

@app.route('/ai-data')
def get_ai_data():
    data = [["Time", "Choking Danger", "Shock Danger", "Falling Danger", "Suffocation Danger", "Sharp Danger", "Distress", "Point"], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1000]]

    for SECOND in range(seconds):
        # if exists(frame from 24*seconds --> 24*(seconds+1)) use frame
        record = None if len(frames) == 0 else next((x for x in frames if x >= 24*SECOND and x <= 24*(SECOND+1)), None)
        print(record, frames)
        #record = None
        ai_opinion = get_ai_opinions(record, SECOND)
        #ai_opinion = None if record == None else get_ai_opinions(record)
        #avg_danger_level = None if record == None else (record[1] + record[2] + record[3]) / 3
        #data.append([float(SECOND), 0.0 if avg_danger_level == None else float(avg_danger_level), -1000.0])
        data.append(ai_opinion)
    return jsonify(data)

# Supported video file extensions

def extract_key_frames(video_path, threshold=5, min_contour_area=500):
    ai_dangers = []
    SUPPORTED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    # Check file extension
    print(video_path)
    _, ext = os.path.splitext(video_path)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported file type '{ext}'. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}")
        return
    
    # Extract the base name of the video file without extension
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Create the output directory based on the video file name
    output_dir = f"{base_name}_output"
    
    # Read the video from specified path
    cam = cv2.VideoCapture(video_path)
    if not cam.isOpened():
        print("Error: Unable to read video")
        return

    # Create the output directory if it doesn't exist
    if os.path.exists('opencv'):
        shutil.rmtree('opencv')
    os.makedirs('opencv')

    # Frame counters
    current_frame = 0
    key_frame_count = 0
    most_recent_frame = 0

    # Read the first frame
    ret, prev_frame = cam.read()
    if not ret:
        print("Error: Unable to read video")
        return

    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    while True:
        # Read the next frame
        ret, frame = cam.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Compute the absolute difference between the current frame and the previous frame
        frame_diff = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)[1]

        # Dilate the threshold image to fill in holes, then find contours on threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if there is any significant motion
        motion_detected = any(cv2.contourArea(contour) > min_contour_area for contour in contours)

        if motion_detected:
            # Save the frame in the output directory
            if current_frame > most_recent_frame + 24:
                frame_name = os.path.join('opencv', f'frame{current_frame}.jpg')
                print(f'Creating... {frame_name}')
                cv2.imwrite(frame_name, frame)
                frames.append(current_frame)
                #ai_dangers.append(get_ai_opinions(frame_name, current_frame))
                key_frame_count += 1

        # Update the previous frame
        prev_gray = gray
        current_frame += 1

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return ai_dangers

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    print(os.path.join(UPLOAD_FOLDER, file.filename))
    global frames
    frames = []
    global ai_dangers_record
    ai_dangers_record = extract_key_frames(os.path.join(UPLOAD_FOLDER, file.filename), 5, 500)
    print(ai_dangers_record)
    global img_ai_resp
    img_ai_resp = dict()
    global hume_resp
    hume_resp = dict()
    response = requests.get('http://localhost:9999/restart-data')
    if (response.json() != 'success'): print('err')
    #response = requests.post('http://localhost:9998/start-data/', data=jsonify(ai_dangers))
    return 'success', 200

@app.route('/upload-test', methods=['GET'])
def upload_file_test():
    filename = '../app/testvid.mp4'
    global ai_dangers_record
    ai_dangers_record = extract_key_frames(filename, 5, 500)

    response = requests.get('http://localhost:9999/restart-data')
    if (response.json() != 'success'): print('err')
    print(ai_dangers_record)
    #response = requests.post('http://localhost:9998/start-data/', data=jsonify(ai_dangers))
    return 'success', 200

def irregularity(vitals, vital):
    state = False
    if vitals[vital][-1] > vitals[vital + '_minmax'][0] + 10 or vitals[vital][-1] < vitals[vital + '_minmax'][1] - 10:
        state = True
    if vitals[vital + '_minmax'] == [0, 0]:
        state = False
        vitals[vital + '_minmax'] = [vitals[vital][-1]] * 2
    elif vitals[vital][-1] > vitals[vital + '_minmax'][1]: vitals[vital + '_minmax'][1] = vitals[vital][-1]
    elif vitals[vital][-1] < vitals[vital + '_minmax'][0]: vitals[vital + '_minmax'][0] = vitals[vital][-1]
    return state


    #start_time = time.time()

    
'''
    try:
        while True:
            ready = select.select([client], [], [], 5)
            response = None
            if ready[0]:
                response = client.recv(4096)
            if not response:
                break
            report = json.loads(response.decode('utf-8'))
            vitals['time'].append(time.time() - start_time)
            vitals['heartbeat'].append(float(report['BPM']))
            vitals['temperature'].append(float(report['Temperature']))
            vitals['breathing'].append(float(report['Breathing']))
            #irregularity('heartbeat')
            #irregularity('temperature')
            #irregularity('breathing')

            print(time.time() - start_time, {
                'heartbeat': irregularity('heartbeat'),
                'temperature': irregularity('temperature'),
                'breathing': irregularity('breathing')
            })
            #print(response.decode('utf-8'))
            #print(json.dumps(vitals), time.time() - start_time)
    finally:
        client.close()'''


if __name__ == '__main__':
    #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.connect(('127.0.0.1', 9999))
    #while input():
        #print(json.loads(get_data()))
    #    print(get_data())
    app.run(debug=True, port=1601)