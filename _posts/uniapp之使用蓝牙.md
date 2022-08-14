---
title: uniapp之使用蓝牙
date: 2022-07-31 20:50:28
tags:
	- uniapp
---

--

```
<template>
	<view class="container">
		<uni-nav-bar title="设备管理" left-icon="back" fixed backgroundColor='#fff' color='#000' :border='false'>
		</uni-nav-bar>
		<view class="ul">
			<view class="li" v-for="(item, index) in bluetooth" :key="index" :title="item.name"
				@click="createBLEConnection(item.deviceId, index)">
				<view class="li-left">
					<view class="blueImg">
						<image src="../../static/c1.png" mode="widthFix"></image>
					</view>
					<view class="eqName">{{ item.name }}</view>
				</view>
				<view class="status">
					<view v-if="isLink[index]==0" class="ft-color-999999"></view>
					<view v-if="isLink[index]==1" class="ft-color-999999">连接中...</view>
					<view v-if="isLink[index]==2" class="ft-color-007FFF">已连接</view>
					<view v-if="isLink[index]==3" class="ft-color-999999">连接失败</view>
					<view v-if="isLink[index]==4" class="ft-color-999999">已断开</view>
					<view v-if="isLink[index]==2" @click.stop="closeBLEConnection(item.deviceId,index)"
						class="ft-color-green iconfont icon-info m-lt20 ft-40 ft-color-999999"> 断开连接</view>
				</view>

			</view>
		</view>
		<view style="display: flex;">
			<button @click="startBluetoothDevicesDiscovery" class="foot-btn-g">搜索周围设备</button>
		</view>
		<!-- <button type="default" @click="readBLECharacteristicValue">获取</button> -->
	</view>
</template>
<script>
	export default {
		data() {
			return {
				isSearch: false,
				bluetooth: [],
				isLink: [],
				// 调试数据
				serverList: [],
				characteristics: [],
				readCode: '',
				readCodeMsg: '',
				serviceId: '',
				characteristicId: '',
				value: '0102',
				returnMessage: '',
				macAddress: "",
				macValue: '', //获取的重量
			}
		},
		onShow() {

			this.getBlueInfo()

		},
		methods: {
			// 监听蓝牙设备连接状态
			listenerConnection() {
				console.log('监听蓝牙设备连接状态')
				let _this = this;
				plus.bluetooth.onBLEConnectionStateChange(function(e) {
					console.log('connection state changed: ' + JSON.stringify(e));
					_this.deviceId = e.deviceId;
					_this.createBLEConnection(_this.deviceId)
				});
			},

			// 蓝牙手机初始化
			getBlueInfo() {
				console.log('getBlueInfo')
				const _this = this
				plus.bluetooth.openBluetoothAdapter({
					success(res) {
						console.log(JSON.stringify(res))
						_this.startBluetoothDevicesDiscovery()
					},
					fail(err) {
						console.log('fail', err)
						uni.showToast({
							title: '未检测到蓝牙',
							icon: 'none'
						})
					}
				});
			},
			// 搜索周围蓝牙设备
			startBluetoothDevicesDiscovery() {
				console.log('开始搜索蓝牙设备')
				const _this = this
				this.isSearch = true
				this.bluetooth = []
				this.searchNoNameBluetooths = []
				plus.bluetooth.startBluetoothDevicesDiscovery({
					// services:['FE7D','FFF0'],//可选 要获取设备的uuid列表
					success(res) {
						console.log(JSON.stringify(res))
						plus.bluetooth.onBluetoothDeviceFound(res => {
							console.log(JSON.stringify(res))
							_this.getBluetoothDevices();
						})
					},
					fail(err) {
						console.log('错误信息', JSON.stringify(err))

						uni.showToast({
							title: '蓝牙未初始化',
							icon: 'none',
							duration: 2000
						});

					}
				})
			},
			// 停止搜索

			stopBluetoothDevicesDiscovery() {
				plus.bluetooth.stopBluetoothDevicesDiscovery({
					success: e => {
						console.log('停止搜索蓝牙设备:' + e.errMsg);
					},
					fail: e => {
						console.log('停止搜索蓝牙设备失败，错误码：' + e.errCode);
					}
				});
			},
			// 获取已发现的蓝牙设备
			getBluetoothDevices() {
				console.log('获取已发现的蓝牙设备')
				const _this = this
				plus.bluetooth.getBluetoothDevices({
					success(res) {
						// console.log(' 获取已发现的蓝牙设备',res)
						// _this.stopBluetoothDevicesDiscovery()
						_this.bluetooth = res.devices.filter(item => {
							return item.name
						})
						_this.isLink = []
						_this.bluetooth.forEach(e => {
							_this.isLink.push(0)
						})
					}
				})
			},
			// 获取蓝牙适配器状态
			getBluetoothAdapterState() {
				plus.bluetooth.getBluetoothAdapterState({
					success(res) {
						console.log('获取蓝牙适配器状态', res)
					}
				})
			},
			// 连接蓝牙
			createBLEConnection(deviceId, index) {
				console.log('连接蓝牙', deviceId, index)
				const _this = this
				this.deviceId = deviceId;
				if (this.isLink[index] == 2) {
					return;
				}
				this.isLink.splice(index, 1, 1)
				plus.bluetooth.createBLEConnection({
					deviceId: _this.deviceId,
					success: res => {
						console.log(res)
						_this.isLink.splice(index, 1, 2)
						_this.stopBluetoothDevicesDiscovery();
						_this.getBLEDeviceServices(_this.deviceId);
						uni.showLoading({
							title: '连接中...',
							mask: true
						});
					},
					fail: res => {

						if (res.message == 'already connect') {
							_this.isLink[index] = 2;
							_this.stopBluetoothDevicesDiscovery();
							_this.getBLEDeviceServices(_this.deviceId);
						} else {
							_this.isLink.splice(index, 1, 3)
						}
						console.log(JSON.stringify(res))
					}
				})
			},

			//获取蓝牙设备所有服务(service)。
			getBLEDeviceServices(deviceId) {
				const _this = this
				console.log(deviceId)
				setTimeout(() => {
					plus.bluetooth.getBLEDeviceServices({
						// 这里的 deviceId 需要已经通过 createBLEConnection 与对应设备建立链接
						deviceId: deviceId,
						success: (res) => {
							console.log('获取蓝牙设备所有服务:', JSON.stringify(res.services))
							_this.serverList = res.services
							var findItem = res.services.find(item => {
								//FE7D FFF0
								if (item.uuid != '00001800-0000-1000-8000-00805F9B34FB' && item
									.uuid != '00001801-0000-1000-8000-00805F9B34FB' &&
									item.uuid != '0000180A-0000-1000-8000-00805F9B34FB') {
									return item;
								}
							})
							console.log(JSON.stringify(findItem))
							_this.serviceId = findItem.uuid;
							_this.getBLEDeviceCharacteristics(_this.deviceId)
						},

						fail: res => {
							console.log(res)
						}
					})
				}, 4000)
			},

			// 获取蓝牙特征值
			getBLEDeviceCharacteristics(deviceId) {
				console.log("进入特征");
				const _this = this
				setTimeout(() => {
					plus.bluetooth.getBLEDeviceCharacteristics({
						// 这里的 deviceId 需要已经通过 createBLEConnection 与对应设备建立链接
						deviceId: deviceId,
						// 这里的 serviceId 需要在 getBLEDeviceServices 接口中获取
						serviceId: this.serviceId,
						success: (res) => {
							_this.characteristics = res.characteristics
							console.log('characteristics', JSON.stringify(_this.characteristics))

							let findItem = res.characteristics.find(item => {
								let uuid = item.uuid
								console.log(uuid)
								return item.properties.notify
							})
							_this.characteristicId = findItem.uuid;
							console.log('当前使用的特征characteristicId:', _this.characteristicId)
							_this.notifyBLECharacteristicValueChange(_this.deviceId)
							let bluetoothData = {
								deviceId: _this.deviceId,
								serviceId: _this.serviceId,
								characteristicId: _this.characteristicId
							}
							uni.setStorageSync('bluetoothData', bluetoothData)
							uni.hideLoading();

						},
						fail: (res) => {
							uni.hideLoading();
							console.log(res)
						}
					})
				}, 4000)
			},
			// 启用 notify 功能
			notifyBLECharacteristicValueChange(deviceId) {
				const _this = this;
				console.log('deviceId' + deviceId)
				console.log('serviceId' + _this.serviceId)
				console.log('characteristicId' + _this.characteristicId)
				plus.bluetooth.notifyBLECharacteristicValueChange({
					state: true, // 启用 notify 功能
					// 这里的 deviceId 需要已经通过 createBLEConnection 与对应设备建立链接
					deviceId: deviceId,
					// 这里的 serviceId 需要在 getBLEDeviceServices 接口中获取
					serviceId: _this.serviceId,
					// 这里的 characteristicId 需要在 getBLEDeviceCharacteristics 接口中获取
					characteristicId: _this.characteristicId,
					success: (res) => {
						console.log('notifyBLECharacteristicValueChange success', res)
						_this.$api.msg('连接成功', 'success')
					},
					fail: (res) => {
						console.log('notifyBLECharacteristicValueChange fail', res)
						console.log(JSON.stringify(res))
						_this.$api.msg('连接失败')
					}
				})
			},
			ab2hex(buffer) {
				const hexArr = Array.prototype.map.call(
					new Uint8Array(buffer),
					function(bit) {
						return ('00' + bit.toString(16)).slice(-2)
					}
				)
				return hexArr.join('')
			},
			//十六进制转字符串,调整高低位
			hexCharCodeToStr(hexCharCodeStr) {
				let trimedStr = hexCharCodeStr.trim();
				let rawStr =
					trimedStr.substr(0, 2).toLowerCase() === "0x" ?
					trimedStr.substr(2) :
					trimedStr;
				let len = rawStr.length;
				if (len % 2 !== 0) {
					alert("Illegal Format ASCII Code!");
					return "";
				}
				let curCharCode;
				let resultStr = [];
				for (let i = 0; i < len; i = i + 2) {
					curCharCode = parseInt(rawStr.substr(i, 2), 16); // ASCII Code Value
					resultStr.unshift(String.fromCharCode(curCharCode));
				}

				return Math.round(parseFloat(resultStr.join("")) * 100) / 100;
			},

			// 监听低功耗蓝牙设备的特征值变化
			onBLECharacteristicValueChange(deviceId) {
				const _this = this;
				plus.bluetooth.onBLECharacteristicValueChange((res) => {
					console.log(`characteristic ${res.characteristicId} has changed, now is`, res)
					console.log(this.ab2hex(res.value))
					_this.macAddress = res.deviceId;
					let val = _this.ab2hex(res.value);

					let resValue = _this.hexCharCodeToStr(val)
					_this.macValue = resValue
					console.log(resValue + '千克')
				})
			},

			// 读取设备二进制数据
			readBLECharacteristicValue() {
				let _this = this;
				plus.bluetooth.readBLECharacteristicValue({
					// 这里的 deviceId 需要已经通过 createBLEConnection 与对应设备建立链接
					deviceId: _this.deviceId,
					// 这里的 serviceId 需要在 getBLEDeviceServices 接口中获取
					serviceId: _this.serviceId,
					// 这里的 characteristicId 需要在 getBLEDeviceCharacteristics 接口中获取
					characteristicId: _this.characteristicId,
					success: (res) => {
						console.log('readBLECharacteristicValue:', res)
						this.readCode = res.errCode;
						this.readCodeMsg = res.errMsg;
						this.onBLECharacteristicValueChange(this.deviceId);
					},
					fail: (res) => {
						console.log('readBLECharacteristicValue:', res)
						this.readCode = res.errCode;
						this.readCodeMsg = res.errMsg;
						this.onBLECharacteristicValueChange(this.deviceId);
					}
				})

			},
			// 写入低功耗蓝牙设备的特征值
			writeBLECharacteristicValue(value) {
				const _this = this;
				console.log('写入低功耗蓝牙设备的特征值')
				// const data = new Uint8Array(_this.write.qp).buffer;
				//2
				let codeLength = value.length / 2;
				let buffer = new ArrayBuffer(codeLength)
				const dataView = new DataView(buffer)

				let data = [];
				//在这里解析将要写入的值  
				for (let i = 0; i < codeLength; i++) {
					dataView.setUint8(i, '0X' + value.substring(i * 2, i * 2 + 2));

					data.push(value.substring(2 * i, 2 * i + 2))
				}
				plus.bluetooth.writeBLECharacteristicValue({
					deviceId: _this.deviceId,
					serviceId: _this.serviceId,
					characteristicId: _this.characteristicId,
					value: buffer,
					success: function(e) {
						console.log('发送成功', data.join(','))
						console.log('write characteristics success: ' + JSON.stringify(e));
					},
					fail: function(e) {
						console.log('write characteristics failed: ' + JSON.stringify(e));
					}
				});
			},

			//断开蓝牙连接
			closeBLEConnection(deviceId, index) {
				const _this = this
				plus.bluetooth.closeBLEConnection({
					deviceId: deviceId,
					success: res => {
						console.log('断开蓝牙连接')
						_this.isLink.splice(index, 1, 4)
					}
				})
			},
		}
	}
</script>

<style scoped lang="scss">
	.ul {
		margin: 10px;

		.li {
			display: flex;
			justify-content: space-between;
			background: #FFFFFF;
			margin-top: 13upx;
			align-items: center;
			font-size: 30upx;
			border-radius: 20upx;
			height: 160upx;
			padding-left: 43upx;

			.li-left {
				display: flex;

				.blueImg {
					width: 77upx;
					height: 74upx;
					margin-right: 40upx;

					image {
						width: 100%;
						height: 100%;
					}
				}

				.eqName {
					color: #000000;
					font-size: 30upx;
					width: 250upx;
					word-break: break-all;
					display: flex;
					align-items: center;
				}
			}

			.status {
				display: flex;

				view {
					margin-right: 48upx;
				}
			}

		}
	}

	.search {
		width: 358upx;
		height: 70upx;
		border-radius: 35upx;
		border: 1px solid #5CA3F9;
		margin-top: 131upx;
		color: #5CA3F9;
		font-size: 24upx;
		line-height: 70upx;
		text-align: center;
	}

	.foot-btn-g {
		color: #007FFF;
		margin-top: 80upx;
	}

	.ft-color-999999 {
		color: #999999;
	}

	.ft-color-007FFF {
		color: #007FFF;
	}
</style>

```



参考资料

1、

https://blog.csdn.net/MrHao_/article/details/121467595