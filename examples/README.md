This directory contains example Python scripts using the
[**cdrouter.py**](https://cdrouterpy.readthedocs.io/en/latest/introduction.html)
wrapper module for the [**CDRouter Web
API**](https://support.qacafe.com/cdrouter/cdrouter-web-api). Feel free to use
them or modify them to suit your needs.

| Name                                                       | Description
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------
| **[addpackage.py](addpackage.py)**                         | Create  new  test  packages  from  a  set  of  existing  config  files  and  tests  provided  by  the  user
| **[bulk_export.py](bulk_export.py)**                       | Export a arbitrary combination of Devices, Configs, Packages and Results as CDRouter export archive
| **[bulk_launch_jobs.py](bulk_launch_jobs.py)**             | Launch all test packages that match a particular tag
| **[create_config.py](create_config.py)**                   | Simple example that creates a new config file with fixed contents
| **[device_versioning.py](device_versioning.py)**           | Uploads a firmware image file to CDRouter as an attachment to a device
| **[fail_reasons.py](fail_reasons.py)**                     | Print reason for any tests that have failed
| **[gitlab.py](gitlab.py)**                                 | Launch tagged packages and generate a JUnit XML report which can be in a GitLab CI/CD pipeline as a report artifact
| **[import_archive.py](import_archive.py)**                 | Import the contents of a CDRouter export archive file
| **[jenkins.py](jenkins.py)**                               | Run a test package and generate a report in XML format compatible with Jenkins
| **[launch_job_by_wan_mode.py](launch_job_by_wan_mode.py)** | A set of packages repeatedly with different values of `wanMode` testvar
| **[mark_packets.py](mark_packets.py)**                     | Highlight lines in log of ***any*** test containing  DHCPOFFER packets, flag the test, and mark result with a star
| **[migrate.py](migrate.py)**                               | Migrate test results from one CDRouter system to another
| **[result_diff.py](result_diff.py)**                       | Run the *"Diff Results"* tool against several results and print results
| **[validate_package.py](validate_package.py)**             | Check whether a test package will run without config errors or skipped tests
