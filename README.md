# appointment-bot
Ethical bot that checks for website changes (like appointments or products being available) and alerts you when it notices one.

**tl;dr: This repo has two lambda functions in it. One checks a website and reports if it has changed from a user-defined state. The other function sends an SMS to the user when triggered.**

This can be used to monitor websites for a variety of reasons. You might be looking to make an appointment, or just want to know if a site changes (New blogpost or video, etc.) You can basically think of this as a lightweight notification layer for a website. I built this because I needed to book an appointment on an ancient government website that had no waitlist or schedule for appointment availability. 

**Limitations:** This bot is very simple, and assumes the target site has some kind of static element to it. It can only handle basic logins, and can't handle MFA. **Most importantly, by design it doesn't take any direct action on its findings.** 

Bots that scoop up appointments or buy up tickets are lame as fuck and make the world worse, don't build those. 

# Real set up

**Tl;dr: Set up two lambdas for each python script. Trigger the website checker function via an eventbridge schedule, and give it permission to execute other lambdas.**

You will need:
* An AWS account
* A Twilio API key + credits
* A lambda layer that contains the requests library
  * If you don't know how to make a layer, or want instructions for doing it via the CLI, see below.
  

1. Create a function



# Making a lambda layer from the AWS CLI


The below instructions let you build a lambda function entirely from the AWS CLI. This can save the same / hassle of doing it on your local machine. Someone will probably say you should do this as two separate layers. Maybe you should. This is the lazy way. 

What we'll do here: Spin up a python venv, make a directory and download the packages we need there, zip up that folder, make an S3 bucket, move the zip to that S3 bucket, and then make a lambda layer out of the zip in that S3 bucket. 

* [Open AWS Cloudshell](https://console.aws.amazon.com/cloudshell) (Make sure you select the right region)
* Execute the following commands to make a director and start a python virtual environment
  * `mkdir layers`
  * `cd layers`
  * `python3 -m venv venv`
  * `source venv/bin/activate`
* Now, in the virtual environment, execute these commands
  * `mkdir my_layer_name`
  * `cd my_layer_name`
  * `pip install requests -t .`
  * cd ..
* Cool, all of the stuff we need is in the subdirectory, so let's zip it up, make a bucket, put it in that bucket, and turn it into a layer. You'll need to make your own S3 bucket name. 
  * `zip -r my_layer_name.zip my_layer_name`
  * `aws s3api create-bucket \
    --bucket a-cool-and-unique-bucket-name \
    --region us-east-1`
  * `aws s3 cp lazy_layer.zip s3://a-cool-and-unique-bucket-name/`
  * `aws lambda publish-layer-version \
    --layer-name requests_layer \
    --description "Python Layer for requests library" \
    --license-info "MIT" \
    --content S3Bucket=a-cool-and-unique-bucket-name,S3Key=my_layer_name.zip \
    --compatible-runtimes python3.9`
    
You should now see the lambda layer available. 
