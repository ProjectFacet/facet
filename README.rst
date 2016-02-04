=============
Project Facet
=============

Project Facet is an open source project to help newsrooms efficiently plan content across all publishing platforms. Facet is an editorial workflow management app that fully covers all aspects of assigning, editing and managing news content.

Facet fosters collaboration across teams and with other organizations by allowing newsrooms to create networks to share the editorial process with teams both in and outside of the media organization.

`Project Facet <http://www.projectfacet.org/>`__

Deployment
==========

To Deploy This App
------------------

- `$ pip install requirements/???` should include awsebcli, django-storages, and boto. If not:
- `$ pip install awsebcli` to be able to talk to elastic beanstalk
- `$ pip install django-storages boto` to be able to store static files from s3
- add these to the requirements file
- `$ eb init`
 
.ebextensions
-------------

There should already be an .ebextensions folder in the project root, but if not, here are the steps to create one.

- mkdir .ebextensions
- subl .ebextensions/01-facet.config
- paste in:

    option_settings:
      "aws:elasticbeanstalk:application:environment":
        DJANGO_SETTINGS_MODULE: "project.settings"
        PYTHONPATH: "/opt/python/current/app/project:$PYTHONPATH"
      "aws:elasticbeanstalk:container:python":
        WSGIPath: "project/project/wsgi.py"
      "aws:elasticbeanstalk:container:python:staticfiles":
        "/static/": "www/static/"
    packages:
      yum:
        git: []
        libjpeg-turbo-devel: []
        postgresql93-devel: []

To Make a non-load-balancing EB App with a Database
---------------------------------------------------

- ` $ eb create --database.engine postgres --single`

Trying to create a database from the aws console currently results in an error (known bug for django apps).
Trying to create a non-load-balancing app using the config file currently still create a load balancer (known bug).

Set up your Bucket
------------------

- create a new IAM user in the aws console and make note of the users ARN
- Download their Security Credentials/Access Keys
- find the bucket Elasic Beanstalk created for you
- paste in the following bucket permissions, replace the three instances of BUCKET-NAME and single instance of USER_ARN

		{
		    "Statement": [
		        {
		          "Sid":"PublicReadForGetBucketObjects",
		          "Effect":"Allow",
		          "Principal": {
		                "AWS": "*"
		             },
		          "Action":["s3:GetObject"],
		          "Resource":["arn:aws:s3:::BUCKET-NAME/*"
		          ]
		        },
		        {
		            "Action": "s3:*",
		            "Effect": "Allow",
		            "Resource": [
		                "arn:aws:s3:::BUCKET-NAME",
		                "arn:aws:s3:::BUCKET-NAME/*"
		            ],
		            "Principal": {
		                "AWS": [
		                    "USER-ARN"
		                ]
		            }
		        }
		    ]
		}


Deploy
------

- `$ git status` to see if there are any changes to be committed. AWS runs off of your git commits.
- commit any changes
- `$ eb deploy`, but wait!

The first time, this might raise a KeyError. Set your keys using `$ eb setenv KEY="VALUE"`

You can generate a new SECRET_KEY using `$ python manage.py generatekey`
Insert the BUCKET_NAME you found using the AWS console
Replace AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY with the credentials you downloaded

- `$ eb deploy` again and you should be good to go!


Delete Everything
-----------------

If you want to start over, use

- `$ eb terminate --all` and confirm the name of your project environment

Troubleshooting
---------------

If you get a Bad Request (400) error, make sure your domain name is listed under
ALLOWED_HOSTS in your production settings.

If you get a permission denied error for your static files, make sure link is relative
to static diredtory from staticfiles. This is dynamic and will find s3 if you're
using it (if storages is set up correctly).

