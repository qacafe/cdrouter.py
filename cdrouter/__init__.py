#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Python client for the CDRouter Web API."""

__version__ = "0.0.7"

from .cdrouter import Service

from .configs import ConfigsService
from .devices import DevicesService
from .attachments import AttachmentsService
from .jobs import JobsService
from .packages import PackagesService
from .results import ResultsService
from .testresults import TestResultsService
from .annotations import AnnotationsService
from .captures import CapturesService
from .highlights import HighlightsService
from .imports import ImportsService
from .exports import ExportsService
from .history import HistoryService
from .system import SystemService
from .tags import TagsService
from .testsuites import TestsuitesService
from .users import UsersService
