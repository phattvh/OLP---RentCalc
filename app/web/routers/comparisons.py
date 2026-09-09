# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router nhập tiền thực thu và đối chiếu chênh lệch so với quy định."""

from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_owner
from app.db.session import get_db
from app.services.invoice_service import InvoiceService

router = APIRouter(dependencies=[Depends(require_owner)])


@router.post("/invoices/{invoice_id}/comparison", response_class=RedirectResponse)
def update_comparison(
    invoice_id: int,
    actual_collected: str = Form(...),
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)
    service.update_actual_collected(
        invoice_id=invoice_id,
        actual_collected_str=actual_collected.strip(),
    )
    return RedirectResponse(f"/invoices/{invoice_id}", status_code=303)