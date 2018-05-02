# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    BaseWebTest,
    BaseAuctionWebTest,
    test_organization as base_test_organization,
    test_auction_data, base_test_bids
)
from openprocurement.auctions.core.utils import apply_data_patch


from openprocurement.auctions.insider.constants import DEFAULT_PROCUREMENT_METHOD_TYPE

now = datetime.now()
test_insider_auction_data = deepcopy(test_auction_data)
test_insider_auction_data["procurementMethodType"] = DEFAULT_PROCUREMENT_METHOD_TYPE

test_organization = deepcopy(base_test_organization)
test_organization['additionalIdentifiers'] = [{
    "scheme": u"UA-FIN",
    "id": u"А01 457213"
}]

test_bids = []
for i in base_test_bids:
    bid = deepcopy(i)
    bid.update({'eligible': True})
    bid.update({'qualified': True})
    bid['tenderers'] = [test_organization]
    test_bids.append(bid)

test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]

del test_insider_auction_data['minimalStep']

class BaseInsiderWebTest(BaseWebTest):

    """Base Web Test to test openprocurement.auctions.insider.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)


class BaseInsiderAuctionWebTest(BaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_insider_auction_data
    initial_organization = test_organization

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=5)).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now + timedelta(hours=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=2)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=12)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=20)).isoformat(),
                    "endDate": (now - timedelta(days=13)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=11)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=11)).isoformat(),
                                "endDate": (now - timedelta(days=10)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)
        auction = self.db.get(self.auction_id)
        auction.update(apply_data_patch(auction, data))
        self.db.save(auction)
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        #response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response
