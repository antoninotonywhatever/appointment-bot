import requests, boto3, os

# Store email + password as environment variables in lambda, reference if needed.
login_payload = {
    'Email': os.environ.get('email'),
    'Password': os.environ.get('password')
}
  
# The root of where you want the bot to check, with the path after. 
url_payload = {
    'url': "URL Of Site Here",
    'path': "Login URL / Path here if applicable"
}  

# This code does not introduce any element of randomness to execution
# Your eventbridge schedule should be set to something like 1 hour with 15-30 minutes of variation 

def lambda_handler(event, context):
    # The header you're sending to the site. User Agent is an example here, you should update it according to your findings
    # The origin is the root URL we're visiting, and the referer is the full path of the log in, if necessary

    HEADERS = {'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'origin': url_payload['url'], 'referer': url_payload['url'] + url_payload['path']}
   
    # Open a session with the site, send the URL + login payload
    # If the site doesn't need a log in, you can drop the login payload

    checker_session = requests.session()
    login_req = checker_session.post(url_payload['url'] + url_payload['path'], headers=HEADERS, data=login_payload)
    
    # The canary you're using on the site. Basically, what's the disappointing message you see on the site?
    # Eg, this might be something like "No appointments available" or "under construction" or "Check back later", etc.
    # The find function returns -1 when the given string isn't present.

    if (login_req.text).find('The text found on the website that represents it being booked / the same as before') != -1:
        print("## No Change")
        print("Site has not changed")
        
        # You can uncomment this line while troubleshooting to see what the bot is finding on the site
        # print(login_req.text)
        

    # The statement that fires when the site HAS changed

    else:
        print("## Change Detected")

        # invoke our lambda function to send an SMS. Both this function and the one sending the SMS need to be in the same region
        # Additionally, this function needs to have permissions to execute lambdas 

        lambda_client = boto3.client('lambda')
        lambda_client.invoke(FunctionName='name of your notification lambda',
            InvocationType='Event')

        # You can uncomment this line while troubleshooting to see what the bot is finding on the site
        # print("## Website Findings")
        # print(login_req.text)
