# Changelog

All notable changes to Moon Phase Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-09-14
### Changed
- GitHub Repo name changed from Moon-Phase-Tracker -> MoonPhase-CLI.
- Update made to PKGBUILD for Arch AUR requirements.



## [0.2.0] — 2026-09-14
### Added
- Addition of config.toml file for mostly const value (e.x. location).
- Clearner UI for moon info output.

### Fixed
- Only one API request a day.
    - Done by storing the first API call of the day as env variables for later use.

### Changed
- Moon ascii made smaller



## [0.1.0] — 2026-07-21
### Added
- Initial release of Moon Phase Tracker.
- Moon phase tracking from the terminal.
- Arch Linux packaging through PKGBUILD.
- Configuration through ~/.config/moonphase/.env.
