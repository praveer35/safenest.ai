import requests
import json
import argparse
import time

# Replace <apiKey> with your HumeAI API key
API_KEY = 'jzxNrIzPdz2FovYG4DkBj00fW2ijG6KHUa35Hdp8dDChHA2M'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload an image and process it with HumeAI.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    image_path = args.image_path

    try:
        # Send POST request to create a job
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

        # Print the response for debugging
        print("Response status code:", response.status_code)
        print("Response headers:", response.headers)
        print("Response text:", response.text)

        # Check if the response is JSON
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
            response_data = response.json()
            if 'job_id' in response_data:
                job_id = response_data['job_id']
                print(f"Job created with ID: {job_id}")

                print("Waiting for job to complete...")
                time.sleep(4)  # Wait for 30 seconds to allow job completion

                # Fetch predictions from the job
                url = f'https://api.hume.ai/v0/batch/jobs/{job_id}/predictions'
                headers = {
                    'X-Hume-Api-Key': API_KEY
                }
                predictions_response = requests.get(url, headers=headers)

                # Print predictions if successful
                if predictions_response.status_code == 200:
                    predictions = predictions_response.json()
                    print(json.dumps(predictions, indent=2))
                else:
                    print(f"Failed to fetch predictions. Status code: {predictions_response.status_code}")
            else:
                raise KeyError(f"Job ID not found in response: {response_data}")
        else:
            raise ValueError(f"Unexpected response format or status: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the request: {e}")
    except KeyError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

