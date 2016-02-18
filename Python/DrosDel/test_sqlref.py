# tests functionality of sqlref script
# Copyright (C) 2014 Jessica Strein jessica.strein@uconn.edu
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import unittest
import sqlref

class SqlRefTestCase(unittest.TestCase):
    """Tests for sqlref.py"""

    def test_cg_n_cont(self):
        """Does the list of cg and n percentages match up?"""
        cg = ['0.5', '0.4', '0.3', '0.2']
        n = ['0', '0.1', '0', '0']
        self.assertEqual(sqlref.cg_n_cont('cg_test.tab'), (cg, n))

    def test_mk_data(self):
        """Is the list of tuples correct?"""
        cg = ['0.5', '0.4', '0.3', '0.2']
        n = ['0', '0.1', '0', '0']
        tot = [('A', '0', 'ATGAATTGCCTGATAAAAAGGATTACCTTGATAGGGTAAATCATGCAGTT', '0.5', '0'), 
               ('A', '1', 'TTCTGCATTCATTGACTGATTTATATATTATTTATAAAGATGATTTTATA', '0.4', '0.1'),
               ('A', '2', 'TTTAATAGAATTAAACTATTTCTAAAAGTATCAAAAACTTTTGTGCATCA', '0.3', '0'),
               ('B', '0', 'TACACCAAAATATATTTACAAAAAGATAAGCTAATTAAGCTACTGGGTTC', '0.2', '0')]
        self.assertEqual(sqlref.mk_data(cg, n, 'fasta_test.fa'), tot)

if __name__ == '__main__':
    unittest.main()