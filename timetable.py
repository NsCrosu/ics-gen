from hashlib import md5
from datetime import datetime, timedelta

# 只需修改此处的导入文件名
from USTL import school    # 创建学校的对象并导入为 school
from USTL import classes   # 创建课表数组并导入为 classes

classTime = [None, *school.classTime]
weeks = [None]
starterDay = datetime(*school.starterDay)
for i in range(1, 30):
	singleWeek = [None]
	for d in range(0, 7):
		singleWeek.append(starterDay)
		starterDay += timedelta(days = 1)
	weeks.append(singleWeek)

uid_generate = lambda key1, key2: md5(f"{key1}{key2}".encode("utf-8")).hexdigest()

iCal = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:课表
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
END:VTIMEZONE
"""

runtime = datetime.now().strftime('%Y%m%dT%H%M%SZ')

for Class in classes:
	[Name, Teacher, Location, classWeek, classWeekday, classOrder] = Class[:]
	# 课程名  教师     教室    第几周上课   在周几上课    第几节课上课
	Title = Name

	for timeWeek in classWeek:
		classDate = weeks[timeWeek][classWeekday]
		startTime = classTime[classOrder[0]]
		endTime = classTime[classOrder[-1]]
		# python 中数组 -1 表示获取倒数第一个

		################################
		timeAddonWeek = 0
		current_date = classDate
		# 获取当前日期的年份、月、日
		if datetime(current_date.year, 5, 1) <= current_date <= datetime(current_date.year, 10, 1):
			if startTime[0] >= 12:  # 如果是下午
				timeAddonWeek = 30  # 延后30分钟
		# 5 月 1 号到 10 月 1 号期间，下午每节课上课的时间要延后 30 分钟
		################################

		timeAddonLocation = 0
		if classOrder == [3, 4] and "博学楼C" in Location:
			timeAddonLocation = 10
		# 博学楼 C 区上午第 3, 4 节向后错峰 10 分钟

		timeAddon = timeAddonWeek + timeAddonLocation
		classStartTime = classDate + timedelta(minutes = startTime[0] * 60 + startTime[1] + timeAddon)
		classEndTime = classDate + timedelta(minutes = endTime[0] * 60 + endTime[1] + school.classPeriod + timeAddon)

		Description = f"""第 {timeWeek} 周; 任课教师: {Teacher}"""
		StartTime = classStartTime.strftime('%Y%m%dT%H%M%S')
		EndTime = classEndTime.strftime('%Y%m%dT%H%M%S')

		singleEvent = f"""BEGIN:VEVENT
DTEND;TZID=Asia/Shanghai:{EndTime}
DESCRIPTION:{Description}
UID:{uid_generate(Name, StartTime)}
DTSTAMP:{runtime}
URL;VALUE=URI:
SUMMARY:{Title}
DTSTART;TZID=Asia/Shanghai:{StartTime}
{school.geo(Location)}
END:VEVENT
"""
		iCal += singleEvent

iCal += "END:VCALENDAR"

with open(f"{school.name}.ics", "w", encoding = "utf-8") as w:
	w.write(iCal)
