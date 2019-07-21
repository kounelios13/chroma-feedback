import copy
from chroma_feedback import color
from .api import get_api


def get_devices(devices, device_names):
	if device_names:
		for device in copy.copy(devices):
			if device not in device_names:
				devices.remove(device)
	return devices


def process_devices(status, devices):
	result = []

	# process devices

	for device in devices:
		if status == 'passed':
			result.append(
			{
				'consumer': 'thingm_blink',
				'type': 'device',
				'name': device,
				'active': static_device(color.get_passed_rgb()),
				'status': status
			})
		if status == 'process':
			result.append(
			{
				'consumer': 'thingm_blink',
				'type': 'device',
				'name': device,
				'active': static_device(color.get_process_rgb()),
				'status': status
			})
		if status == 'errored':
			result.append(
			{
				'consumer': 'thingm_blink',
				'type': 'device',
				'name': device,
				'active': static_device(color.get_errored_rgb()),
				'status': status
			})
		if status == 'failed':
			result.append(
			{
				'consumer': 'thingm_blink',
				'type': 'device',
				'name': device,
				'active': static_device(color.get_failed_rgb()),
				'status': status
			})
	return result


def static_device(state):
	api = get_api()

	return api is not None and api.fade_to_rgb(100, state['red'], state['green'], state['blue']) is None