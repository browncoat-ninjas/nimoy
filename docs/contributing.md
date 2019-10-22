# Contributing

Nimoy is an open source project and welcomes contributions of any kind - bug reports, feature requests, documentation
improvements and code.

## Bug Reports

If you think you've found a bug in Nimoy, first make sure that you are using the latest version. We also suggest
searching for a similar report in the project's open GitHub issues.

Bug reports in form of actual test cases are best as they provide the quickest path to reproduction.

## Contributing Code

To contribute new features or bug fixes:

* Fork and clone the repository
* Use `pipenv` to download the dependencies using: `pipenv install -d`
* Apply your changes, including test cases that prove them
* Run `pylint` to make sure that the quality of the code hasn't deteriorated: `find nimoy -name "*.py" | xargs pylint`
* Run all tests and make sure none have been broken: `pipenv run test`
* Submit the changes using a pull request. Make sure you provide as much detail as possible