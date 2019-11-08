import asyncio
from mavsdk import System
from mavsdk import Param
from mavsdk import ParamError
from argparse import ArgumentParser
import sys

# I don't want to write a class
drone = System()
fp = None

param_names = []
param_vals = []
failed_list = []


async def run():
	await drone.connect(system_address="serial:///dev/ttyACM0:57600")

	# iterate over the list and write the parameters
	i = 0
	for p in param_names:
		await write_param(p, param_vals[i])
		i = i + 1

	# Verify our parameters are written
	for p in param_names:


	if len(failed_list) > 0:
		print(str(len(failed_list)) + " parameters failed:")
		for p in failed_list:
			print(p)


async def write_param(name, val):
	attempts = 0
	while attempts < 3:
		try:
			if isinstance(val, int):
				await drone.param.set_int_param(name, val)
				print("WRITE -- " + name + " -- Success!")
			if isinstance(val, float):
				await drone.param.set_float_param(name, val)
				print("WRITE -- " + name + " -- Success!")

			return

		except ParamError as error:
			print("WRITE -- " + name + " -- Fail!")
			print(f"Starting offboard mode failed with error code: \
				{error._result.result}")

			attempts = attempts + 1
			print("Retrying... attempt " + str(attempts))

			if attempts == 3:
				failed_list.append(name)

async def read_param(name):



def main():
	parser = ArgumentParser(description=__doc__)
	parser.add_argument('file', metavar='PORT', nargs='?', default = None,
			help='file name dumbass')

	# Ensure arguement is passed
	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	args = parser.parse_args()

	# Parse the input file
	fp = open(args.file)


	for line in fp:
		wl = line.split(None,5)

		# ignore comments
		if wl[0] == '#':
			continue

		# Print the NAME and VAL
		name = wl[2]
		val = wl[3]

		# Convert params with a decimal to floats
		if val.find('.') != -1:
			val = float(val)
		else:
			val = int(val)

		if isinstance(val, str):
			print(val)

		# Append names and values to the list
		param_names.append(name)
		param_vals.append(val)

	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())

if __name__ == "__main__":
	main()
