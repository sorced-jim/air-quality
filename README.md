# air-quality

A repo of code for me futzing with my air quality sensor.

To use this code there are few things to do:
1.   Create a GCP project and set GOOGLE_CLOUD_PROJECT to your project name.
1.   Create a service account and give the service a monitoring metric write role.
1.   Create a key for the account, copy to the machine you want and set GOOGLE_APPLICATION_CREDENTIALS to the key file you've downloaded.
1.   Set up a crontab to run main.py, e.g.
     */10 * * * * GOOGLE_CLOUD_PROJECT=P GOOGLE_APPLICATION_CREDENTIALS=some-key.json SOME_PATH/main.py
