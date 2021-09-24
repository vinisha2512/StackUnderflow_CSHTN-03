# A stream implementation using an in-memory bytes buffer
from xhtml2pdf import pisa
from io import BytesIO
# It inherits BufferIOBase
from django.http import HttpResponse
from django.template.loader import get_template
from base64 import b64decode
# pisa is a html2pdf converter using the ReportLab Toolkit,
# the HTML5lib and pyPdf.

# difine render_to_pdf() function


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    b64 = result.getvalue()

    f = open('prescription.pdf', 'wb')
    f.write(b64)
    f.close()
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return Nones
