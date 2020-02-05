# Changelog

All notable changes to Puppy Reinforcement will be documented here. You can click on each release number to be directed to a detailed log of all code commits for that particular release. The download links will direct you to the GitHub release page, allowing you to manually install a release if you want.

If you enjoy Puppy Reinforcement, please consider supporting my work on Patreon, or by buying me a cup of coffee :coffee::

<p align="center">
<a href="https://www.patreon.com/glutanimate" rel="nofollow" title="Support me on Patreon 😄"><img src="https://glutanimate.com/logos/patreon_button.svg"></a>      <a href="https://ko-fi.com/X8X0L4YV" rel="nofollow" title="Buy me a coffee 😊"><img src="https://glutanimate.com/logos/kofi_button.svg"></a>
</p>

:heart: My heartfelt thanks goes out to everyone who has supported this add-on through their tips, contributions, or any other means (you know who you are!). All of this would not have been possible without you. Thank you for being awesome!

## [Unreleased]

## [1.0.0-beta.2] - 2020-02-05

### [Download](https://github.com/glutanimate/puppy-reinforcement/releases/tag/v1.0.0-beta.2)

### Fixed

- Fixed compatibility with Visual Feedback and other add-ons using newer versions of libaddon
- Print "card" instead of "cards" if count singular

## [1.0.0-beta.1] - 2020-01-28

### [Download](https://github.com/glutanimate/puppy-reinforcement/releases/tag/v1.0.0-beta.1)

### Added

- Anki 2.1 compatibility (thanks to @zjosua for his help with this!, #77)
- Optional support for showing puppies while creating new cards. Controlled by the `count_adding` option in the settings (thanks to @zjosua for the implementation and /u/xTheKezio / @ijgnd for the idea, #12)
- Support for more image file types and case-insensitive file extension detection
- A more advanced randomization approach that spreads the chances of particular images being drawn up evenly (#8)

### Fixed

- Added workaround for add-on import bug present in Anki versions <= 2.1.14

### Changed

- Rewrote large parts of the add-on, making it a lot more maintainable for the future
- Dropped Anki 2.0 support (legacy versions remain downloadable on AnkiWeb / GitHub)
- Added support for the new add-on hooks system that will be introduced with the upcoming Anki 2.1.20 release. This should make the add-on fairly future-proof.

## [0.2.0-alpha.1] - 2019-06-09

### [Download](https://github.com/glutanimate/puppy-reinforcement/releases/tag/v0.2.0-alpha.1)

**Important note**: As this release completely overhauls the add-on structure, you will have to uninstall any existing versions of the add-on before updating. Otherwise you might end up with duplicate versions of the add-on that would interfere with each other. *If you have customized the add-on with your own pictures or other adjustments, please make sure to back them up before deleting the old version!*

### Added

- Anki 2.1 compatibility (thanks to [@zjosua](https://github.com/zjosua) for his help with this!, #77)

### Changed

- Refactored add-on to improve stability and maintainability

## 0.1.2 - 2017-08-08 

### Added

- New options: duration, image size, card limits (thanks to Lucas on YT for the ideas!)

## 0.1.1 - 2017-08-06

### Changed

- Update license

## 0.1.0 - 2016-11-18

### Added

- Initial release of Puppy Reinforcement

[Unreleased]: https://github.com/glutanimate/puppy-reinforcement/compare/v1.0.0-beta.2...HEAD
[1.0.0-beta.2]: https://github.com/glutanimate/puppy-reinforcement/compare/v1.0.0-beta.1...v1.0.0-beta.2
[1.0.0-beta.1]: https://github.com/glutanimate/puppy-reinforcement/compare/v0.2.0-alpha.1...v1.0.0-beta.1
[0.2.0-alpha.1]: https://github.com/glutanimate/puppy-reinforcement/releases/tag/v0.2.0-alpha.1

-----

The format of this file is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).