from django import template

register = template.Library()


@register.filter(name='dic_val_or_null')
def dic_val_or_null(crime_data, year_crime):
	year_crime = year_crime.split(';')
	year = int(year_crime[0])
	crime = year_crime[1]
	print(crime_data)
	#print(dic[str(key)])
	#print(dic[key])
	if str(crime) in crime_data[year]:
		return crime_data[year][str(crime)]
	else:
		return 0


@register.filter(name='get_val')
def get_val(list_name, index):
	return list_name[index]

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)