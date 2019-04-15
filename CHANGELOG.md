# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html). (Patch version X.Y.0 is implied if not specified.)

## [Unreleased]

## [0.7] - 2019-04-12 - End of Pilot
### Added
- Docker configuration

### Changed
- Merged this repository with the mlr-ddot-ingester-docker repository
- Changed versioning to proper semantic without the service name

## [0.6] - 2019-03-01
## Changed
- Fixed a bug when DDots are parsed that have lines < 21 characters. 
- Standardize all error messages
- update `flask-restplus` to 0.12.1

## [0.5] - 2019-01-31
### Added
- site number length validation and associated tests

### Changed
- update `requests` to 2.20.0
- update `Flask` to 0.12.3
- update `urllib3` to 1.23

## [0.4] - 2018-08-23
### Changed
- isuftin@usgs.gov - Updated the version constraint for pyca/cryptography due to
CVE https://nvd.nist.gov/vuln/detail/CVE-2018-10903
- When incoming siteWebReadyCode is a 'C', update to 'Y' in parsed ddot result.

### Added
- Dockerfile Healthcheck
- handling of incoming longitudes < 100 degrees with no leading zero.

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

[Unreleased]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.7.0...master
[0.7]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.6.0...0.7.0
[0.6]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.5.0...MLR-Ddot-Ingester-0.6.0
[0.5]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.4.0...MLR-Ddot-Ingester-0.5.0
[0.4]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.3.0...MLR-Ddot-Ingester-0.4.0
[0.3]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.2.0...MLR-Ddot-Ingester-0.3.0
[0.2]: https://github.com/USGS-CIDA/MLR-Ddot-Ingester/compare/MLR-Ddot-Ingester-0.1.0...MLR-Ddot-Ingester-0.2.0
