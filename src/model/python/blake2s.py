#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# blake2s.py
# ---------
# Simple, pure Python model of the Blake2s hash function. The model
# is used as a functional reference for the HW implementation.
#
# See Blake2 paper and RFC 7693 for blake2s definition.
# - https://blake2.net/blake2.pdf
# - https://tools.ietf.org/html/rfc7693
#
#
# Author: Joachim Strömbergson
# Copyright (c) 2018 Assured AB
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Python module imports.
#-------------------------------------------------------------------
import sys


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
VERBOSE = False
UINT32 = 2**32


#-------------------------------------------------------------------
# Blake2s()
#-------------------------------------------------------------------
class Blake2s():
    NUM_ROUNDS = 10

    SIGMA = (( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15),
             (14, 10,  4,  8,  9, 15, 13,  6,  1, 12,  0,  2, 11,  7,  5,  3),
             (11,  8, 12,  0,  5,  2, 15, 13, 10, 14,  3,  6,  7,  1,  9,  4),
             ( 7,  9,  3,  1, 13, 12, 11, 14,  2,  6,  5, 10,  4,  0, 15,  8),
             ( 9,  0,  5,  7,  2,  4, 10, 15, 14,  1, 11, 12,  6,  8,  3, 13),
             ( 2, 12,  6, 10,  0, 11,  8,  3,  4, 13,  7,  5, 15, 14,  1,  9),
             (12,  5,  1, 15, 14, 13,  4, 10,  0,  7,  6,  3,  9,  2,  8, 11),
             (13, 11,  7, 14, 12,  1,  3,  9,  5,  0, 15,  4,  8,  6,  2, 10),
             ( 6, 15, 14,  9, 11,  3,  0,  8, 12,  2, 13,  7,  1,  4, 10,  5),
             (10,  2,  8,  4,  7,  6,  1,  5, 15, 11,  9, 14,  3, 12, 13,  0))

    IV = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)


    def __init__(self, verbose = 0):
        self.verbose = verbose
        self.m = [0] * 16
        self.h = [0] * 8
        self.v = [0] * 16
        self.t = [0] * 2


    def hash_message(m):
        self._init()
        return self._get_digest(n)


    def _init(self, param_block):
        self.h = self.IV[:]
        self.h[0] = self.h0


    def _next(self, block):
        pass


    def _finalize(self, block, blocklen):
        pass


    def _get_digest(self, n):
        return self.H


    def _F(self, m, final_block):
        # Initialize the work vector v based on the current hash state.
        for i in range(8):
            self.v[i] = self.h[i]
            self.v[(i + 8)] = self.IV[i]

        self.v[12] = self.v[12] ^ self.t[0]
        self.v[13] = self.v[13] ^ self.t[1]

        if final_block:
            self.v[14] = self.v[14] ^ (UINT32 - 1)

        # Process the m in NUM_ROUNDS, updating the work vector v.
        self._compress(self.NUM_ROUNDS)

        # Update the hash state with the result from the v processing.
        for i in range(8):
            self.h[i] = self.h[i] ^ self.v[i] ^ self.v[(i + 8)]


    def _compress(self, r):
        self._dump_m()
        print("State of v before compression:")
        self._dump_v()
        for i in range(r):
           (self.v[0], self.v[4], self.v[8], self.v[12]) =\
            self._G(self.v[0], self.v[4], self.v[8], self.v[12], self.m[self.SIGMA[i][0]], self.m[self.SIGMA[i][1]])

           (self.v[1], self.v[5], self.v[9], self.v[13]) =\
            self._G(self.v[1], self.v[5], self.v[9], self.v[13], self.m[self.SIGMA[i][2]], self.m[self.SIGMA[i][3]])

           (self.v[2], self.v[6], self.v[10], self.v[14]) =\
            self._G(self.v[2], self.v[6], self.v[10], self.v[14], self.m[self.SIGMA[i][4]], self.m[self.SIGMA[i][5]])

           (self.v[3], self.v[7], self.v[11], self.v[15]) =\
            self._G(self.v[3], self.v[7], self.v[11], self.v[15], self.m[self.SIGMA[i][6]], self.m[self.SIGMA[i][7]])


           (self.v[0], self.v[5], self.v[10], self.v[15]) =\
            self._G(self.v[0], self.v[5], self.v[10], self.v[15], self.m[self.SIGMA[i][8]], self.m[self.SIGMA[i][9]])

           (self.v[1], self.v[6], self.v[11], self.v[12]) =\
            self._G(self.v[1], self.v[6], self.v[11], self.v[12], self.m[self.SIGMA[i][10]], self.m[self.SIGMA[i][11]])

           (self.v[2], self.v[7], self.v[8], self.v[13]) =\
            self._G(self.v[2], self.v[7], self.v[8], self.v[13], self.m[self.SIGMA[i][12]], self.m[self.SIGMA[i][13]])

           (self.v[3], self.v[4], self.v[9], self.v[14]) =\
            self._G(self.v[3], self.v[4], self.v[9], self.v[14], self.m[self.SIGMA[i][14]], self.m[self.SIGMA[i][15]])

        print("State of v after compression")
        self._dump_v()
        print()


    def _G(self, a, b, c, d, m0, m1):
        if VERBOSE:
            print("G Inputs:")
            print("a = 0x%08x, b = 0x%08x, c = 0x%08x, d = 0x%08x, m0 = 0x%08x, m1 = 0x%08x" %\
                      (a, b, c, d, m0, m1))
        self.a1 = (a + b + m0) % UINT32

        self.d1 = d ^ self.a1
        self.d2 = self._rotr(self.d1, 16)

        self.c1 = (c + self.d2) % UINT32
        self.b1 = b ^ self.c1
        self.b2 = self._rotr(self.b1, 12)
        self.a2 = (self.a1 + self.b2 + m1) % UINT32
        self.d3 = self.d2 ^ self.a2
        self.d4 = self._rotr(self.d3, 8)
        self.c2 = (self.c1 + self.d4) % UINT32
        self.b3 = self.b2 ^ self.c2
        self.b4 = self._rotr(self.b3, 7)

        if VERBOSE:
            print("a1 = 0x%08x, a2 = 0x%08x" % (self.a1, self.a2))
            print("b1 = 0x%08x, b2 = 0x%08x, b3 = 0x%08x, b4 = 0x%08x" %\
                      (self.b1, self.b2, self.b3, self.b4))
            print("c1 = 0x%08x, c2 = 0x%08x" % (self.c1, self.c2))
            print("d1 = 0x%08x, d2 = 0x%08x, d3 = 0x%08x, d4 = 0x%08x" %\
                      (self.d1, self.d2, self.d3, self.d4))

        return (self.a2, self.b4, self.c2, self.d4)


    def _rotr(self, x, n):
        return  (((x) >> (n)) ^ ((x) << (32 - (n)))) % UINT32


    def _print_state(self):
        print("")


    def _dump_v(self):
        print("v00 - 07: 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x" %\
                  (self.v[0], self.v[1], self.v[2], self.v[3], self.v[4], self.v[5], self.v[6], self.v[7]))
        print("v08 - 15: 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x" %\
                  (self.v[8], self.v[9], self.v[10], self.v[11], self.v[12], self.v[13], self.v[14], self.v[15]))


    def _dump_m(self):
        print("m00 - 07: 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x" %\
                  (self.m[0], self.m[1], self.m[2], self.m[3], self.m[4], self.m[5], self.m[6], self.m[7]))
        print("m08 - 15: 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x 0x%08x" %\
                  (self.m[8], self.m[9], self.m[10], self.m[11], self.m[12], self.m[13], self.m[14], self.m[15]))


#-------------------------------------------------------------------
# test_code()
#
# Small test routines used during development.
#-------------------------------------------------------------------
def test_code():
    my_hash = Blake2s()

    print("rotr(0x80000000, 31) = 0x%08x" % (my_hash._rotr(0x80000000, 31)))

    print("Testing the G function.")
    my_hash._G(0x6b08c647, 0x510e527f, 0x6a09e667, 0x510e523f, 0x03020100, 0x07060504)


    # Test the complete compression function. We need to load m and v to known states.
    print("Testing the compression function.")
    my_hash.h = [0] * 16
    my_hash.v = [0xe065e50d, 0x01a7d670, 0xc933bba4, 0x866aa41e, 0x18ab3e05, 0x26edc492, 0x04c59a4f, 0x95dd5a91,
                 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e523e, 0x9b05688c, 0xe07c2654, 0x5be0cd19]
    my_hash._compress(10)


#-------------------------------------------------------------------
# main()
#
# If executed tests the ChaCha class using known test vectors.
#-------------------------------------------------------------------
def main():
    print("Testing the Blake2s Python model")
    print("--------------------------------")
    test_code()



#-------------------------------------------------------------------
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__":
    # Run the main function.
    sys.exit(main())

#=======================================================================
# EOF blake2s.py
#=======================================================================
