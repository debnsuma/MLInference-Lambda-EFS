import json
import easyocr
import os

model_dir = os.getenv('MODEL_DIR', "/mnt/ml/models/")
network_dir = os.getenv('NETWORK_DIR', "/mnt/ml/network/")

# Cache readers in memory to avoid downloading again
# Note that if using large number of models, you'll have to write an LRU cache as this map will overflow on memory.
model_cache = {}

def lambda_handler(event, context):

    # Reading the body to extract the URL and the language 
    body = json.loads(event['body'])
    
    language_list = [lang.strip() for lang in body["language"].split(",")]
    print(f"Sending the data for prediction")
    
    # Checking the Cache readers, and doing the inference 
    languages_key = '_'.join(language_list)
    if languages_key not in model_cache:
        model_cache[languages_key] = easyocr.Reader(language_list, model_storage_directory=model_dir, user_network_directory=network_dir, gpu=False, download_enabled=False)        
    reader = model_cache[languages_key]   
    results = reader.readtext(body["link"])
    
    # Formating the prediction 
    response = [result[1] for result in results]
    response = " ".join(response)
    
    # Logging the response in the logs
    print(f"Here is the formated output {response}")
    
    # Function Return 
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_label": response,
            }
        )
    }