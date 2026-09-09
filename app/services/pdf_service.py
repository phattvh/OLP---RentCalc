# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Dịch vụ xuất hóa đơn định dạng PDF chuẩn chính thức."""

import io


def render_html_to_pdf(html_content: str) -> bytes:
    """Render chuỗi HTML thành file PDF dạng bytes."""
    try:
        from weasyprint import HTML
        return HTML(string=html_content).write_pdf()
    except Exception:
        # Fallback an toàn cho môi trường Windows khi thiếu thư viện GTK
        from xhtml2pdf import pisa
        output = io.BytesIO()
        pisa.CreatePDF(html_content, dest=output)
        return output.getvalue()