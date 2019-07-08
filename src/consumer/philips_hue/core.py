import json
import requests

args = None


def init(program):
	global args

	if not args:
		program.add_argument('--philips-hue-host', required = True)
		program.add_argument('--philips-hue-username', required = True)
		program.add_argument('--philips-hue-group', action = 'append', required = True)
	args = program.parse_known_args()[0]


def run(status):
	groups = args.philips_hue_group

	return process(status, groups)


def process(status, groups):
	result = []

	# process groups

	for group in groups:
		if status == 'passed':
			result.append({
				'consumer': 'philips_hue',
				'name': group,
				'active': static(group, 25500),
				'status': status
			})
		if status == 'process':
			result.append({
				'consumer': 'philips_hue',
				'name': group,
				'active': static(group, 12500),
				'status': status
			})
		if status == 'errored':
			result.append({
				'consumer': 'philips_hue',
				'name': group,
				'active': pulsate(group, 34000),
				'status': status
			})
		if status == 'failed':
			result.append({
				'consumer': 'philips_hue',
				'name': group,
				'active': pulsate(group, 0),
				'status': status
			})
	return result


def static(group, hue):
	return update(group,
	{
		'hue': hue,
		'on': True,
		'bri': 255,
		'alert': 'none'
	})


def pulsate(group, hue):
	return update(group,
	 {
		'hue': hue,
		'on': True,
		'bri': 255,
		'alert': 'lselect'
	})


def update(group, data):
	response = None
	host = args.philips_hue_host
	user = args.philips_hue_user

	if host and user:
		response = requests.put(host + '/api/' + user + '/groups/' + group + '/action', data = json.dumps(data))

	# process response

	if response and response.status_code == 200:
		return True
	return False
