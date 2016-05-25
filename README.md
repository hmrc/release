# Releasing an artefact

This repo provides a script that allows to tag a git repository:
- It looks if the specified build completed successfully
- Gets the commit id from the build
- Suggests you the new version
- Tags the repository

##Prepare the environment

* To enable scripts to interact with jenkins, define a 'jenkins_key' and 'jenkins_user' environment variable in your bashrc file. 
```
export jenkins_user=<username>
export jenkins_key=<api-token>
```
Replace <username> with your jenkins username (no quotes)
Replace <api-token> with the value obtained from Jenkins

* In addition to that you need some python libraries: requests, pymongo and bottle. 
```
$ curl -O http://python-distribute.org/distribute_setup.py
$ sudo python distribute_setup.py
$ sudo easy_install pip
$ sudo pip install requests
$ sudo pip install pymongo
$ sudo pip install bottle
```
* Configure github and jenkins urls in src/universal/conf/hosts.json

## Release
* Tag the artefact: ```python release.py -v jenkins_job_name build_number```
The script in src/universal/bin will look at your jenkins instance for the specified green build and tag the repository with the same name as the job.

## License ##
 
This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
