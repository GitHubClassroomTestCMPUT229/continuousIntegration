#---------------------------------------------------------------
# Assignment:           1
# Due Date:             January 27, 2017
# Name:                 Stuart Hoye
# Unix ID:              hoye
# Lecture Section:      B1
# Instructor:           Karim Ali
# Lab Section:          H05 (Thursday 170:0 - 20:00)
# Teaching Assistant:   Noah Weininger
#---------------------------------------------------------------

#---------------------------------------------------------------
#
# This program prompts the user to enter in an integer value.
# After getting the integer, the program flips its endianness:
# little-endian ints become big-endian & big-endian vice-versa.
#
# Register Usage:
#
#		v0: used to make syscalls
#       a0: holds the flipped value to be printed.
#		t0: move the rightmost byte to the leftmost position
#		t1: move the next byte to the next leftmost position
#		t2: move the next byte to the second from rightmost
#		t3: move the leftmost byte to the rightmost position
#
#---------------------------------------------------------------

.data

.text

main:
	li	$v0, 5				# syscall readint
	syscall					# $v0 <- 0xWWXXYYZZ

	andi $t0, $v0, 0xFF		# $t0 <- 0x000000ZZ
	sll  $t0, $t0, 0x18		# $t0 <- 0xZZ000000
	andi $t1, $v0, 0xFF00	# $t1 <- 0x0000YY00
	sll  $t1, $t1, 0x8		# $t1 <- 0x00YY0000
	srl  $v0, $v0, 0x10		# $v0 <- 0x0000WWXX
	andi $t2, $v0, 0xFF		# $t2 <- 0x000000XX
	sll  $t2, $t2, 0x8		# $t2 <- 0x0000XX00
	andi $t3, $v0, 0xFF00	# $t3 <- 0x0000WW00
	srl  $t3, $t3, 0x8		# $t3 <- 0x000000WW

	add  $a0, $t0, $zero	# $a0 <- 0xZZ000000
	add  $a0, $a0, $t1		# $a0 <- 0xZZYY0000
	add  $a0, $a0, $t2		# $a0 <- 0xZZYYXX00
	add  $a0, $a0, $t3		# $a0 <- 0xZZYYXXWW

	li	$v0, 1				# syscall printint
	syscall

	jr	$ra					# Return
