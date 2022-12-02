# appointment-bot
Ethical bot that checks for website changes (like appointments or products being available) and alerts you when it notices one.

**tl;dr: This repo has two lambda functions in it. One checks a website and reports if it has changed from a user-defined state. The other function sends an SMS to the user when triggered.**

This can be used to monitor websites for a variety of reasons. You might be looking to make an appointment, or just want to know if a site changes (New blogpost or video, etc.) You can basically think of this as a lightweight notification layer for a website. I built this because I needed to book an appointment on an ancient government website that had no waitlist or schedule for appointment availability. 

**Limitations:** This bot is very simple, and assumes the target site has some kind of static element to it. It can only handle basic logins, and can't handle MFA. **Most importantly, by design it doesn't take any direct action on its findings.** 

Bots that scoop up appointments or buy up tickets are lame as fuck and make the world worse, don't build those. 



# Set up

**Tl;dr: Set up two lambdas for each python script. Trigger the website checker function via an eventbridge schedule, and give it permission to execute other lambdas.**

You will need:
* An AWS account
* A Twilio API key + credits
