import re
i=re.search(pattern=".*\.(jpg|gif|png)",string="http://static.ettoday.net/images/1387/d1387895.jPg",flags=re.I)
print(i)

m= re.search(pattern='.*[-\w]+\.(jpg|gif|png)', string="http://static.ettoday.net/images/1387/d1387895.jpg").group(0)
print(m)