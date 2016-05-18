# Releasing an artefact

This repo provides a script that allows to tag a git repository:
- It looks if the specified build completed successfully
- Gets the commit id from the build
- Suggests you the new version
- Tags the repository

##Prepare the environment

* Set up your local configuration by creating a file ```~/.hmrc/release.conf``` which is a json formatted file that should look like this:

```
{
    "git":"git@<your_git-instance:your_repo>",
    "jenkins":"https://<your-jenkins>",
    "jenkins_user": "<username>",
    "jenkins_key": "<api-token>"
}
```

  - Replace <username> with your jenkins username.
  - Replace <api-token> with the value obtained from Jenkins.
  - Configure github and jenkins urls to the appropriate values.

* In addition to that you need some python libraries: requests, pymongo and bottle. 
```
$ curl -O http://python-distribute.org/distribute_setup.py
$ sudo python distribute_setup.py
$ sudo easy_install pip
$ sudo pip install requests
$ sudo pip install pymongo
$ sudo pip install bottle
```

## Release
* Tag the artefact: ```python release.py -v jenkins_job_name build_number```
The script in src/universal/bin will look at your jenkins instance for the specified green build and tag the repository with the same name as the job.

## License ##
 
This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
