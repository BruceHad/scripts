# Numbers Available

## Problem

The _number_ is the set of five digit numbers excluding those that start with zero. e.g. 10235 but not 01265. So the total set contains 90,000 numbers ranging from 10000 to 99999.

New numbers are assigned and resigned over time. So far, around 22,000 numbers have been assigned, but 14,000 have since resigned, leaving 8,000 numbers active and in use, and around 68,000 numbers still available for use.

A _misread_ is where a number is entered incorrectly for some reason (usually OCR misread or user error). A _collision_ is a misread that happens to match one of the active numbers.

The problem is how to find and assign new numbers that minimise the risk of collisions.

## String Distance

The [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) compares two strings of the same length, and counts the number of positions at which the corresponding symbols are different. I.e. it measures the minimum number of errors that could have transformed one string into the other.

So 11111 & 21111 have a Hamming Distance of 1, while 11111 & 22221 have a hamming distance of 4.

## Method

We can calculate the Hamming Distance for each available number against each active list numbers. Any number that has no other active number with a Hamming Distance of 1 (i.e. 1 transformation away) would be considered a 'hit'. This would ensure that two or more characters would have to be misread before any possibility of a collision arises, hopefully reducing the risk significantly.

When comparing to 'active' list numbers, we also have to take into account 'hits' that have been found already (i.e. numbers that will be 'active' in the future), to ensure that we don't add two new numbers that are only 1 transformation away from each other (no idea how likely this is). Therefore each 'hit' should be added to the list of active numbers, before any further checks are made.

We also have to be careful in defining 'active' numbers, as they can remain in use up to 15 months after being resigned.

For a five digit number there are approximately 50 other numbers within 1 transform from the original. 

## Performance

There are around 68,000 potential numbers, which have to be compared to the 8,000 active numbers. A full analysis of each number would result in 544,000,000 comparisons.

Testing shows that the hamming distance comparison take around 5x10**-6 seconds which is pretty quick, but 544 million comparisons still take over an hour to process.

