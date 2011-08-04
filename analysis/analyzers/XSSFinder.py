#
# Author: Seth Law
#
# Copyright (c) 2011 RAFT Team
#
# This file is part of RAFT.
#
# RAFT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# RAFT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RAFT.  If not, see <http://www.gnu.org/licenses/>.
#

import re

from ..AbstractAnalyzer import AbstractAnalyzer

class XSSFinder(AbstractAnalyzer):
    AlertRegex = re.compile("(alert\((.*?)\))",re.I)
    
    def __init__(self):
        self.desc="Identification of successful XSS attacks."
        self.friendlyname="XSS Finder"
    
    def analyzeTransaction(self, target, results):
        responseBody = target.responseBody
        rawRequest = target.rawRequest
        
        for found in self.AlertRegex.finditer(responseBody):
            print "Found %s in responseBody" % found.group(2)
            #TempRegex = re.compile(found.group(0))
            #print "rawReq: %s" % rawRequest
            match = re.search(found.group(2),target.requestHeaders + target.requestBody)
            print match
            if match is not None:
                print "Success: %s" % found.group(2)
                highlight=found.group(1)
                results.addPageResult(pageid=target.responseId, 
                                url=target.responseUrl,
                                type=self.friendlyname,
                                desc=self.desc,
                                data={'Javascript Alert found':found.group(1)},
                                span=found.span(),
                                highlightdata=highlight)