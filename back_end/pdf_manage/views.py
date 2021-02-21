from pdf_manage.utils import RL_Codecs
RL_Codecs.register()

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from pdfrw import PdfReader, PdfWriter
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from django.utils.translation import ugettext_lazy as _
import io


class PdfTester(APIView):

    def test(self, cc, i, test):
        for i1 in i:
            if i1.get('type') == 3:
                s = ""
                e = ""
                k = ""
                for i2 in i1.get('argument'):
                    if i2.get("key_label") == 'キー':
                        k = i2.get("key_value")
                    if i2.get("key_label") == '開始':
                        s = i2.get("key_value")
                    if i2.get("key_label") == '終了':
                        e = i2.get("key_value")
                for i2 in i1.get('contents'):
                    test_list = []
                    if int(s) == int(e):
                        test_list.append(test.get(k)[int(s)-1])
                    else:
                        test_list.append(test.get(k)[int(s)-1:int(e)])
                    if i2.get('if_value') in test_list:
                        self.test(cc, i2.get('contents'), test)
            elif i1.get('type') == 2:
                x = ""
                y = ""
                k = ""
                for i2 in i1.get('argument'):
                    if i2.get("key_label") == 'キー':
                        k = i2.get("key_value")
                    if i2.get("key_label") == 'x軸':
                        x = i2.get("key_value")
                    if i2.get("key_label") == 'y軸':
                        y = i2.get("key_value")
                cc.drawString(int(x), int(y), test.get(k))

    def post(self, request):
        fontname_g = "HeiseiKakuGo-W5"
        pdfmetrics.registerFont(UnicodeCIDFont(fontname_g))
        buffer = io.BytesIO()
        cc = canvas.Canvas(buffer)
        cc.setFont(fontname_g, 24)
        page = PdfReader('media/pdf/sample.pdf', decompress=False).pages
        pp = pagexobj(page[0])
        # reader = PdfFileReader('media/pdf/sample.pdf')
        # writer = PdfFileWriter()
        test = {"test1": "test1", "test2": "S2", "test3": "テスト",
                "test4": [
                    {"key_label": "テスト1", "flag": True},
                    {"key_label": "テスト2", "flag": True},
                    {"key_label": "テスト3", "flag": True},
                ]}
        a = request.data['test_list']
        for i in a:
            self.test(cc, i.get('contents'), test)
        cc.doForm(makerl(cc, pp))
        cc.showPage()
        cc.save()
        buffer.seek(0)
        # new_pdf = PdfFileReader(buffer)
        # existing_page = reader.getPage(0)
        # existing_page.mergePage(new_pdf.getPage(0))
        # writer.addPage(existing_page)

        # new = io.BytesIO()
        # writer.write(new)
        # new.seek(0)

        # output_pdf = open('media/pdf/sample2.pdf', 'wb')
        r = PdfReader(buffer)
        y = PdfWriter()
        y.addpage(r.pages[0])
        with open('media/pdf/sample2.pdf', 'wb') as f:
            y.write(f)
        # writer.write(output_pdf)
        # output_pdf.close()
        return Response({'detail': _('Successfully confirmed email.')},
                        status=status.HTTP_201_CREATED)