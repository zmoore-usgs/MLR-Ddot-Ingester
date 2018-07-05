# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html). (Patch version X.Y.0 is implied if not specified.)

## [Unreleased]
### Added
- Dockerfile Healthcheck

### Removed
- Dockerfile
- Dockerfile-DOI

## [0.3] - 2017-11-20
### Added
- GET endpoint /version to show the current version and artifact name
- Check for invalid transaction type
- Check for unknown component codes
- Authentication for the /ddots endpont
- HTTPS Support

## [0.2] - 2017-11-01
### Added
- The latitude and longitude fields are inspected to ensure that the first character is either a space or a '-'. If this 
is not true, the latitude or longitude field parsed from the ddot file has a space prepended to it.
- This CHANGELOG file

## 0.1 - 2017-10-02
### Added
- POST to upload a ddot file and parse into a json object at /ddots endpoint
- Swagger document at /api endpoint

[Unreleased]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.3.0...master
[0.3]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.2.0...MLR-Ddot-Ingester-0.3.0
[0.2]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.1.0...MLR-Ddot-Ingester-0.2.0
