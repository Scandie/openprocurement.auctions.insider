# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.award_document import (
    FinancialAuctionAwardDocumentResource,
)


@opresource(name='dgfInsider:Auction Award Documents',
            collection_path='/auctions/{auction_id}/awards/{award_id}/documents',
            path='/auctions/{auction_id}/awards/{award_id}/documents/{document_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction award documents")
class InsiderAuctionAwardDocumentResource(FinancialAuctionAwardDocumentResource):
    pass
