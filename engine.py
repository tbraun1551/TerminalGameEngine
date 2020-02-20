### GAME-MAKER CAN EDIT/ADD TO ENGINE, HOWEVER BUILT TO BE SUFFICIENT FOR A BASIC GAME AS IS ###


import cursor
import time
import sys
import colorama
import shutil
from sty import bg, Style # https://github.com/feluxe/sty
from PIL import Image, ImageSequence, GifImagePlugin
import numpy as np
import os


# RESETS CONSOLE, EXITS SCRIPT
def exit_game():
	cursor.show()
	exit_dark_mode()

	exit()


# TAKES USER INPUT UNTIL IT MATCHES ONE OF THE GIVEN OPTIONS. ADDS CHOICE TO USER OBJECT.
# RETURN USER INPUT AS INT.
# PARAMETERS:
#	- num_options: int number of valid menu options
def get_valid_answer(num_options, user):
	while True:
		try:
			choice = int(input(""))
		except ValueError:
			print("Please enter one of the available numbers.")
			continue

		if choice < 1 or choice > num_options:
			print("Please enter one of the available numbers.")
			continue
		else:
			user.add_choice(choice)
			return choice


# PRINT QUESTION IN BOTTOM LEFT CORNER OF TERMINAL (DEFAULT TERMINAL PRINTING) AND CALL GET_VALID_ANSWER FOR CHOICE.
# RETURN CHOICE.
# PARAMETERS:
#	- question: string question asking to user
#	- options: list of strings of options
#	- animate: boolean whether or not you want the text to appear as if it is being typed out or simply appear as a normal print
#	- center_horiz: boolean representing whether or not text will be horizontally centered on console
#	- center_vert:  "									 " vertically "				"
#	- delay: float representing time in seconds between when characters appear - only applies when animate == True
def ask_question(question, options, user, bg_color=colorama.Back.LIGHTWHITE_EX, animate=True, center_horiz=True, center_vert=True, char_delay=0.04, line_delay=1):
	options_formatted = ""
	for i in range(len(options)):
		options_formatted += "\n{}: {}".format(i + 1, options[i])
	text = question + options_formatted
	show_text(text, bg_color=bg_color, animate=animate, center_horiz=center_horiz, center_vert=center_vert, char_delay=char_delay, line_delay=line_delay)
	cursor.show()
	choice = get_valid_answer(len(options), user)
	cursor.hide()
	return choice


# PRINTS STRINGS. CAN CENTER TEXT AND PRINT SUCH THAT TEXT APPEARS TO BE TYPED ONTO SCREEN.
# PARAMETERS:
#	- s: string to be printed
#	- animate: boolean whether or not you want the text to appear as if it is being typed out or simply appear as a normal print
#	- center_horiz: boolean representing whether or not text will be horizontally centered on console
#	- center_vert:  "									 " vertically "				"
#	- delay: float representing time in seconds between when characters appear - only applies when animate == True
# https://stackoverflow.com/questions/3160699/python-progress-bar/3160819#3160819
def show_text(s, bg_color=colorama.Back.LIGHTWHITE_EX, animate=True, center_horiz=True, center_vert=True, char_delay=0.04, line_delay=1):

	clear_screen(bg_color)

	columns, rows = shutil.get_terminal_size(fallback=(80, 24))
	sys.stdout.write("\x1b7\x1b[%d;%df\x1b8" % (rows-1, 0))
	sys.stdout.flush()

	# https://stackoverflow.com/questions/7392779/is-it-possible-to-print-a-string-at-a-certain-screen-position-inside-idle
	def show(text, rows_above, columns_left):
		sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (rows_above, columns_left, "".join(text)))
		sys.stdout.flush()

	indiv_lines = s.split("\n")
	num_lines = len(indiv_lines) + sum([int(len(line)/columns) for line in indiv_lines])
	lines = [""] * num_lines
	i = 0
	continued_lines = []
	for j in indiv_lines:
		parts = int(len(j)/columns) + 1
		for k in range(parts):
			lines[i] = j[k*columns:(k+1)*columns]
			if k > 0:
				continued_lines.append(i)
			i += 1

	if center_vert == False:
		rows_above = rows - num_lines
	else:
		rows_above = int(rows/2) - int(num_lines/2)
	line_break_index = [0]

	for i in range(len(lines)):
		if center_horiz == False:
			columns_left = 0
		else:
			columns_left = int(columns/2) - int(len(lines[i])/2)

		if animate == True:
			if i > 0 and i not in continued_lines: # don't delay first line or portion of split line
				time.sleep(line_delay)
			for j in range(len(lines[i])):
				if j != 0: # don't delay first char
					time.sleep(char_delay)
				show(lines[i][:j+1], rows_above + i, columns_left)
		else:
			show(lines[i], rows_above + i, columns_left)


# CLEAR TERMINAL WINDOW AND SET TO BACKGROUND COLOR.
# PARAMETERS:
#	- background: color
def clear_screen(background=colorama.Back.LIGHTWHITE_EX):
	columns, rows = shutil.get_terminal_size(fallback=(80, 24))
	for i in range(rows):
		print(background + (" " * columns))


# CLEAR SCREEN TO BLACK AND MAKE BACKGROUND BLACK AND TEXT WHITE GOING FORWARD
def dark_mode():
	clear_screen(colorama.Back.BLACK)
	print(colorama.Back.BLACK)
	print(colorama.Fore.WHITE)


# CLEAR SCREEN TO WHITE AND MAKE BACKGROUND WHITE AND TEXT BLACK GOING FORWARD
def light_mode():
	clear_screen(colorama.Back.LIGHTWHITE_EX)
	print(colorama.Back.LIGHTWHITE_EX)
	print(colorama.Fore.BLACK)


# "FADE" SCREEN TO BLAC/WHITE BY RAPIDLY CLEARING SCREEN (USING CLEAR_SCREEN) WITH INCREASINGLY DARK/LIGHT SHADES OF GRAY.
# AFTER CALLING, BACKGROUND WILL ALWAYS BE BLACK/WHITE AND TEXT ALWAYS WHITE/BLACK.
# PARAMETERS:
#	- mode: fade to "dark" or "light mode"
def fade_to_mode(mode="dark"):
	if mode == "light":
		r = range(23,0,-1)
	else:
		r = range(23)

	for i in r:
		color = bg(255-i)
		clear_screen(color)
		columns, rows = shutil.get_terminal_size(fallback=(80, 24))
		for i in range(rows):
			print(color + (" " * columns))
		time.sleep(0.04)

	if mode == "light":
		light_mode()
	else:
		dark_mode()


# RESET STANDARD COLOR SETTINGS
def exit_dark_mode():
	print(colorama.Style.RESET_ALL)


# TURN PNG IMAGE INTO ASCII ART.
# WILL NOT WORK FOR IMAGES THAT ARE *TOO* WIDE RELATIVE TO HEIGHT.
# RETURN ASCII ART STRING.
# PARAMETERS:
#	- f: file name of PNG to be converted
#	- SC: scale applied to image before turning to text - if 0, will be autoscaled
#	- GCF: intensity correction factor - essentially translates to how much of image data is transformed to ASCII
#	- white_to_at: boolean; if true, whitest pixels mapped to @, darkest to space; otherwise vice versa.
#		white_to_at's logic is inverse in dark mode - i.e. black will become @
# https://gist.github.com/cdiener/10567484
# https://stackoverflow.com/questions/56634634/convert-2d-array-to-3d-numpy-array
def asciinate(f, SC=0, GCF=1, white_to_at=True):

	# CALCULATES SCALING FACTOR SUCH THAT ASCII ART RESULTING FROM PNG WILL FILL CONSOLE TOP TO BOTTOM.
	# RETURN SCALING FACTOR.
	# PARAMETERS:
	#	- img: PngImageFile
	#	- rows: number of rows in terminal window
	def autoscale_png(img, rows):
		w, h = img.size
		SC = rows/h
		return SC

	chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
	img = Image.open(f)
	columns, rows = shutil.get_terminal_size(fallback=(80, 24))
	if SC == 0:
		SC = autoscale_png(img, rows)
	S = (round(img.size[0]*SC*(7/4)), round(img.size[1]*SC))
	img = np.asarray(img.resize(S))
	try:
		img = img.reshape((img.shape[0], img.shape[1], 1))
	except ValueError:
		img = img.reshape((img.shape[0], img.shape[1], 3))
	img = np.sum(img, axis=2)
	img -= img.min()
	if white_to_at == True:
		img = (1.0 - img/img.max())**GCF*(chars.size-1)
	else:
		img = (img/img.max())**GCF*(chars.size-1)

	return (" " * (int(columns/2) - int(img.shape[1]/2))) + ("\n" + (" " * (int(columns/2) - int(img.shape[1]/2)))).join(("".join(r) for r in chars[img.astype(int)]))


# TURNS GIF INTO PNGS REPRESENTING EACH FRAME OF GIF AND SAVES PNGS IN OUTPUT FOLDER.
# RETURNS NUMBER OF FRAMES IN GIF.
# PARAMETERS:
#	- f: gif input file name
#	- output_folder: name of folder to save PNGs to
# https://stackoverflow.com/questions/7503567/python-how-i-can-get-gif-frames
def gif_to_png(f, output_folder):
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	gif = Image.open(f)
	i = 0
	try:
		while 1:
			gif.seek(gif.tell()+1)
			gif.save("{}/frame{}.png".format(output_folder, i))
			i += 1
	except EOFError:
		pass
	return gif.n_frames


# USES GIF_TO_PNG AND ASCIINATE FUNCTIONS TO TURN GIF INTO ASCII "ANIMATION" WHICH IT THEN PRINTS.
# PARAMETERS:
#	- f: gif input file name
#	- output_folder: name of folder to save PNGs to
#	- SC: scale applied to image before turning to text
#	- GCF: intensity correction factor - essentially translates to how much of image data is transformed to ASCII
#	- white_to_at: boolean; if true, whitest pixels mapped to @, darkest to space; otherwise vice versa.
#		white_to_at's logic is inverse in dark mode - i.e. black will become @
#	- delay: float representing time between frames
def asciinate_gif(f, output_folder, SC=0, GCF=1, white_to_at=True, delay=0.1):
	nframes = gif_to_png(f, output_folder)
	for i in range(nframes-2):
		print(asciinate("{}/frame{}.png".format(output_folder, i), SC=SC, GCF=GCF, white_to_at=white_to_at))
		time.sleep(delay)

		