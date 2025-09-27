# 单双周 0 = 双, 1 = 单
oeWeek = lambda startWeek, endWeek, mode: [i for i in range(startWeek, endWeek + 1) if (i + mode) % 2 == 0]
# 周范围
rgWeek = lambda startWeek, endWeek: [i for i in range(startWeek, endWeek + 1)]

classes = [

]

class school:	
	name = "课表"

	classTime = [
		# 上午
		(8, 0),
		(8, 50),
		(10, 0),
		(10, 50),
		# 下午
		(13, 30),
		(14, 20),
		(15, 15),
		(16, 5),
		(18, 0),
		(18, 50),
	]                           	# 每节课的上课时间，24 小时制（如: 前 3 节课的上课时间分别是 上午 8:00、上午 8:50、上午 10:00）
									# 数据来自校历
									# 不要写令时时间, 在 timetable.py 中会自动课延后 30 分钟上课

	classPeriod = 45            	# 每一节课的时长分钟数（如: 45 分钟）

	starterDay = [2025, 2, 24]  	# 开学月第一周星期一的日期，存储为年、月、日三项

	AppleMaps = lambda loc: [   	# （如果不使用 Apple Maps 可以完全忽略！）返回 Apple Maps 地址字典的匿名函数
		
		# 使用 r-String 以及三引号文段可以避免转义符号的歧义

		{
			"judge": "教学楼一" in loc,  # 设置匹配「教学楼一」的条件
			"text": r"""LOCATION:某大学一教学楼\n某大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=某大学一教学楼\\n某大学内:geo:30.0000,100.000"""  # 复制 Apple Maps 信息
		},
		{
			"judge": True,        # 请设置一个一直为 True 的建筑用于缺省匹配
			"text": r"""LOCATION:某大学一教学楼\n某大学内
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-TITLE=某大学一教学楼\\n某大学内:geo:30.0000,100.000"""
		}
	]

	def geo(classroom):

		# 方法零：不使用地理坐标信息
		#return ""

		# 方法一：将教室文字搭配坐标信息显示在日历中(几乎所有 ICS 客户端都支持)

		loc = classroom  # 想要显示在日历项地址中的文字
		cor = "0.0000;0.000"   # 地理坐标，纬度、经度之间以 ; 间隔
		return f"LOCATION:{loc}\nGEO:{cor}"  # 包装为符合 ICS 文件要求的格式

		# 方法二：使用 Apple Maps，匹配 `AppleMaps` 数组当中的场所

		loc = ""
		for place in school.AppleMaps(classroom):
			if place["judge"]:
				loc = place["text"]
				break
		return loc
