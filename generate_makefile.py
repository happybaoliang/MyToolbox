import os
import re
import sys

c_file_list = list()
asm_file_list = list()
header_dir_list = set()
header_file_list = list()
c_object_file_list = list()
asm_object_file_list = list()
pattern_for_c_file=r'.[cC]$'
pattern_for_asm_file=r'.[sS]$'
pattern_for_c_header=r'.(h|H|inc)$'


def make_generator(root_dir):
	for root, dirs, files in os.walk(root_dir):
		for f in files:
			if re.search(pattern_for_c_header,f):
				header_dir_list.add(root)
				header_file_list.append(os.path.join(root,f))
			elif re.search(pattern_for_c_file,f):
				c_file_list.append(os.path.join(root,f))
				c_object_file_list.append(os.path.join(root,f)+".o")
			elif re.search(pattern_for_asm_file,f):
				asm_file_list.append(os.path.join(root,f))
				asm_object_file_list.append(os.path.join(root,f)+".o")

	fout = file('makefile','w')

	fout.write("CC=\n")
	fout.write("AS=\n")
	fout.write("LD=\n")
	fout.write("CCFLAG=\n")
	fout.write("ASFLAG=\n")
	fout.write("LDFLAG=\n")
	fout.write("MACROS=\n")
	fout.write("TARGET=\n")

	fout.write("INCS=")
	for dir in header_dir_list:
		fout.write('" -I\"'+dir+'\"')
	fout.write("\n\n")

	fout.write("OBJS=")
	for obj in c_object_file_list:
		fout.write(" "+obj)
	for obj in asm_object_file_list:
		fout.write(" "+obj)
	fout.write("\n\n\n")

	fout.write("all:")
	for obj in asm_object_file_list:
		fout.write(" "+obj)
	for obj in c_object_file_list:
		fout.write(" "+obj)
	fout.write("\n")
	fout.write("	$(LD) $^ $(LDFLAG) -o $(TARGET)\n\n")

	for cfile in c_file_list:
		fout.write(cfile+".o:"+cfile)
		for header in header_file_list:
			fout.write(" "+header)
		fout.write("\n")
		fout.write("	$(CC) $(CCFLAG) $(INCS) $(MACROS) $< -c -o $@\n\n")

	for asmfile in asm_file_list:
		fout.write(asmfile+".o:"+asmfile+"\n")
		fout.write("	$(AS) $(ASFLAG) $< -o $@\n\n")

	fout.write(".PHONY:clean all\n\n")

	fout.write("clean:\n")
	fout.write("	-rm -rf")
	for obj in c_object_file_list:
		fout.write(" "+obj)
	for obj in asm_object_file_list:
		fout.write(" "+obj)

	fout.close

if len(sys.argv)<2:
	print("please specify the source directory!")

make_generator(sys.argv[1])

