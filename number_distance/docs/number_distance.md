# Numbers Available

_Number_ is an of the set of five digit numbers, excluding those that start with zero. e.g. 10235 but not 01265. So a total set of 90,000 numbers.

New numbers are assigned and resigned over time so that at the present moment there are nearly 8,000 active and 14,000 resigned numbers, so around 22,000 numbers have been 'used' already.

Number can't be used more than once, so there are around 68,000 numbers available (90,000 - 22,000).

Numbers are entered by hand or by OCR reading of a form.

A _collision_ is where a number is entered incorrectly for some reason (usually OCR misread or user error) _and_ where the incorrectly entered number matches a valid, active number.

For example if 12345 is misentered as 72345 that is a collision if 72345 is an active list number. If not, it is a simple misread.

The aim is to select new numbers that minimise the risk of clashes.

## Method

Since we are comparing the numbers as we would strings, all numbers are converting to string types.

The [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) compares two strings of the same length, and counts the number of positions at which the corresponding symbols are different. I.e. it measures the minimum number of errors that could have transformed one string into the other.

So the pair 11111 & 21111 has a Hamming Distance of 1, since only one digit requires changing to create a match.

We can calculate the hamming distance for each available list number against all active list numbers and count up the scores.

So for example:

number	zeros	ones	twos	threes	fours	fives
10001	0		3		49		490		2312	4345

This number has zero 'zeros', i.e. no exact matches (which is what we would expect).

But there are 3 active list number within 1 transformation from it. e.g. 10000, 10901 and 10501.
