# Changelog

<!--next-version-placeholder-->

## v0.7.3 (2022-10-02)
### Fix
* Handle ibeacon with impossible power value of 0 ([#16](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/16)) ([`9a9206a`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/9a9206a5db1c843ae227ba7bdc08d2618dee6e86))

## v0.7.2 (2022-09-30)
### Fix
* Add 1CA92E23F0874DF7B9A2FD4B716A4BF6 to banned uuids ([#15](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/15)) ([`f00d6aa`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/f00d6aa4a35767675598fad4acccd6248b778e24))

## v0.7.1 (2022-09-28)
### Fix
* Ignore tilt ble devices ([#14](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/14)) ([`6ce26fa`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/6ce26faa04eafa187b34b0478b66180c99d12c71))

## v0.7.0 (2022-09-23)
### Feature
* Add update_distance method ([#13](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/13)) ([`56edbb5`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/56edbb50569406fc5bf609acb0b8b01bf430ad58))

## v0.6.5 (2022-09-23)
### Fix
* Clamp distance to max theoretical value ([#12](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/12)) ([`ae71fbd`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/ae71fbdebba18f0fbaf1dcdf6db135eb6e86edc2))

## v0.6.4 (2022-09-19)
### Fix
* Round to int to avoid wobble ([#11](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/11)) ([`f87c150`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/f87c15078c5d03bb0ce9f336e59dd5f0ec1ff93d))

## v0.6.3 (2022-09-19)
### Fix
* Add guard for short data ([#10](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/10)) ([`4057bfd`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/4057bfd4d7cf22b29256f0416e379b45b2cec953))

## v0.6.2 (2022-09-18)
### Fix
* Handle more garage data ([#9](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/9)) ([`9ee81c7`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/9ee81c7ffed6dd0877116f95c6f5f9879a453910))

## v0.6.1 (2022-09-18)
### Fix
* Round distance ([#8](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/8)) ([`4abfe18`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/4abfe18c7486db36dc061c0955b1e1b82e384fb7))

## v0.6.0 (2022-09-18)
### Feature
* Abstract checking a service_info into is_ibeacon_service_info ([#7](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/7)) ([`2b95037`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/2b950373a790372ac1f49b297f9f3ff27f85a38b))

## v0.5.0 (2022-09-18)
### Feature
* Reject invalid distance data and return None ([#6](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/6)) ([`be8b9b6`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/be8b9b67e07bbb3f5bc82103f196392f663388e3))

## v0.4.0 (2022-09-18)
### Feature
* Add name and distance ([#5](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/5)) ([`042130e`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/042130e0d2bdc0cdc226901eb88fe89e7a4bdd73))

## v0.3.0 (2022-09-18)
### Feature
* Add distance calculator ([#4](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/4)) ([`4684dab`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/4684dabf2bf83ddee83227ea9b299a85aadb74ac))

## v0.2.0 (2022-09-17)
### Feature
* Port the parser ([#3](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/3)) ([`584a501`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/584a501a733a085a658b7689b4987b7e9e796646))

## v0.1.0 (2022-09-17)
### Feature
* Init ci ([#1](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/1)) ([`574364e`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/574364eb471d4fb86a82ef58c278690851996c9a))

### Fix
* Ci ([#2](https://github.com/Bluetooth-Devices/ibeacon-ble/issues/2)) ([`5a2d2b1`](https://github.com/Bluetooth-Devices/ibeacon-ble/commit/5a2d2b1110aa189098ad42fa04f03a150d598c67))
