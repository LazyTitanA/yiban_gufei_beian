"""
判断是否在高峰时段内
"""
import re
from datetime import datetime
from zoneinfo import ZoneInfo


def parse_peak_hours(peak_str):
    """
    解析高峰时段字符串，返回时间段列表
    格式: "09:00-12:00,14:00-18:00"
    返回: [((9,0), (12,0)), ((14,0), (18,0))]
    """
    periods = []
    if not peak_str:
        return periods
    for part in peak_str.split(','):
        part = part.strip()
        m = re.match(r'(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})', part)
        if m:
            h1, m1, h2, m2 = map(int, m.groups())
            periods.append(((h1, m1), (h2, m2)))
    return periods


def is_peak_time(now=None, peak_str='09:00-12:00,14:00-18:00'):
    """
    判断当前北京时间是否在高峰时段内
    """
    if now is None:
        now = datetime.now(ZoneInfo('Asia/Shanghai'))
    periods = parse_peak_hours(peak_str)
    current_minutes = now.hour * 60 + now.minute
    for (h1, m1), (h2, m2) in periods:
        start = h1 * 60 + m1
        end = h2 * 60 + m2
        if start <= current_minutes <= end:
            return True
    return False
