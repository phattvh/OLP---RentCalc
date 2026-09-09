# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Dịch vụ xuất hóa đơn định dạng PDF chuẩn chính thức hỗ trợ 100% tiếng Việt Unicode."""

import io
import os

# Vá lỗi tempfile permission của xhtml2pdf trên Windows
try:
    from xhtml2pdf.files import pisaFileObject
    _orig_getNamedFile = pisaFileObject.getNamedFile

    def _patched_getNamedFile(self):
        if self.uri and os.path.isfile(self.uri):
            return self.uri
        return _orig_getNamedFile(self)

    pisaFileObject.getNamedFile = _patched_getNamedFile
except Exception:
    pass

try:
    from weasyprint import HTML
    _HAS_WEASYPRINT = True
except Exception:
    _HAS_WEASYPRINT = False


def render_html_to_pdf(html_content: str) -> bytes:
    """Render chuỗi HTML thành file PDF dạng bytes hỗ trợ chuẩn Unicode tiếng Việt."""
    if _HAS_WEASYPRINT:
        try:
            return HTML(string=html_content).write_pdf()
        except Exception:
            pass

    from xhtml2pdf import pisa
    output = io.BytesIO()
    pisa.CreatePDF(html_content, dest=output, encoding="utf-8")
    return output.getvalue()