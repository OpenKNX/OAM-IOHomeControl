# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

> **Note:** The version scheme deviates from [Semantic Versioning](https://semver.org/).
> This is required by technical limitations of the ETS: every change to the ETS
> application requires a bump of the minor version. The major version is constrained
> by the version space, which provides only 1 byte for major.minor (4 bits each).

## [Unreleased]

## v0.1.0: 2026-06-24 (Initial assembly)

- Initial assembly of the OAM-IOHomeControl application
- Build targets for XIAO ESP32-S3 and REG1 ESP DevBoard with SX1262/SX1276 radios and KNX TP/IP
- Integration of OFM-IOHomeControl, OFM-LogicModule, OFM-FunctionBlocks, OFM-Network and OFM-ConfigTransfer
