#!/usr/bin/python3
from os import closerange
import serial
import serial.tools
import serial.tools.list_ports
import threading
import time
import sys

SerialPorts = []
class SerialCommunication():
	def __init__(self):
		self.ThreadEnable = 0
		self.main_engine = serial.Serial()
		print("fuck 11111111111 %d" %(self.main_engine.is_open))

	#初始化
	def Config(self,com,bps,timeout):
		return False

	# 打印设备基本信息
	def Print_Name(self):
		print(self.main_engine.name) #设备名字
		print(self.main_engine.port)#读或者写端口
		print(self.main_engine.baudrate)#波特率
		print(self.main_engine.bytesize)#字节大小
		print(self.main_engine.parity)#校验位
		print(self.main_engine.stopbits)#停止位
		print(self.main_engine.timeout)#读超时设置
		print(self.main_engine.writeTimeout)#写超时
		print(self.main_engine.xonxoff)#软件流控
		print(self.main_engine.rtscts)#软件流控
		print(self.main_engine.dsrdtr)#硬件流控
		print(self.main_engine.interCharTimeout)#字符间隔超时

	#打开串口
	def OpenEngine(self, port, bps, timeout):
		way = 0

		if self.main_engine and self.main_engine.is_open:
			self.CloseEngine()

		try:
			# 打开串口，并得到串口对象
			self.main_engine = serial.Serial(port, bps, timeout=timeout)
			# 判断是否打开成功
			if (self.main_engine.is_open == 0):
				print("open serial port %s fail" %(self.main_engine.name))
				return False
		except Exception as e:
			print("Exception: ", e)
			return False

		#ret = self.main_engine.open()
		print("serial port %s enable:%d start to receive data" %(self.main_engine.name, self.main_engine.is_open))
		self.ThreadEnable = 1
		def sTaskRecv():
			while self.ThreadEnable:
				#print("read com 11 ")
				try:
					# 一个字节一个字节的接收
					if self.main_engine.in_waiting:
						if(way == 0):
							self.SerialPortReadLineCallback(self.main_engine.readline().decode("utf-8","ignore"))
						if(way == 1):
							#整体接收
							data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8","ignore")#方式一
							#data = self.main_engine.read_all()#方式二print("接收ascii数据：", data)
				except Exception as e:
					#self.ThreadEnable = 0
					print("异常报错：",e)
				#print("read com 33 ")
		self.ThreadRecv = threading.Thread(target=sTaskRecv)
		self.ThreadRecv.setDaemon(True)
		self.ThreadRecv.start()

		return True

	#关闭串口
	def CloseEngine(self):
		if self.ThreadEnable:
			print("to stop serial port thread")
			while self.ThreadRecv.is_alive():
				self.ThreadEnable = 0
				print("wait thread finish...")
				time.sleep(1)
		else:
			print("serial port thread is not enabled ")
		if self.main_engine and self.main_engine.is_open:
			print("to stop serial port phy %s" %(self.main_engine.name))
			self.main_engine.close()
			self.main_engine.__del__()

	# 打印可用串口列表
	@staticmethod
	def GetComList():
		# return list(serial.tools.list_ports.comports())
		for port in list(serial.tools.list_ports.comports()):
		    print('端口号：' + port[0] + '   端口名：' + port[1])
		    SerialPorts.append(port[0])
		return SerialPorts

	#接收指定大小的数据
	#从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
	def ReadSize(self,size):
		if self.main_engine:
			return self.main_engine.read(size=size)

	#接收一行数据
	# 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
	# 如果没有超时，readline会报异常。
	def ReadLine(self):
		if self.main_engine:
			return self.main_engine.readline()

	#发数据
	def Senddata(self,data):
		if self.main_engine:
			self.main_engine.write(data)

	#更多示例
	# self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
	# print(self.main_engine.read().hex())  #  # 十六进制的读取读一个字节
	# print(self.main_engine.read())#读一个字节
	# print(self.main_engine.read(10).decode("gbk"))#读十个字节
	# print(self.main_engine.readline().decode("gbk"))#读一行
	# print(self.main_engine.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
	# print(self.main_engine.in_waiting)#获取输入缓冲区的剩余字节数
	# print(self.main_engine.out_waiting)#获取输出缓冲区的字节数
	# print(self.main_engine.readall())#读取全部字符。

	#接收数据
	#一个整型数据占两个字节
	#一个字符占一个字节
	def SetSerialPortReadLineCallback(self, Callback):
		self.SerialPortReadLineCallback = Callback

	def Start(self,way):
		print("开始接收数据：")
		self.ThreadEnable = 1
		def sTaskRecv():
			while self.ThreadEnable:
				#print("read com 11 ")
				try:
					# 一个字节一个字节的接收
					if self.main_engine.in_waiting:
						if(way == 0):
							#for i in range(self.main_engine.in_waiting):
							if self.main_engine.in_waiting:
								self.SerialPortReadLineCallback(self.main_engine.readline().decode("utf-8"))
						if(way == 1):
							#整体接收
							data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8")#方式一
							#data = self.main_engine.read_all()#方式二print("接收ascii数据：", data)
				except Exception as e:
					#self.ThreadEnable = 0
					print("异常报错：",e)
				#print("read com 33 ")
		self.ThreadRecv = threading.Thread(target=sTaskRecv)
		self.ThreadRecv.setDaemon(True)
		self.ThreadRecv.start()

	def Close(self):
		if self.ThreadEnable:
			while self.ThreadRecv.is_alive():
				self.ThreadEnable = 0
				print("wait thread finish...")
				time.sleep(1)
		else:
			print("123...")