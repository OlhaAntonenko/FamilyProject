from fpdf import FPDF
from django.utils.text import slugify

from FamilyStorage.settings import STATIC_DIR


def get_pdf_name(name, data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    file_width = pdf.fw
    cells_width = file_width - pdf.l_margin - pdf.r_margin

    pdf.add_page()

    # Title
    pdf.set_font('Times', 'B', size=20)
    pdf.cell(190, 10, txt=name, ln=1, align="C")
    pdf.ln(5)

    # Main photo
    image_width = 100
    image_x = cells_width / 2 - image_width / 2 + pdf.l_margin
    pdf.image('/home/user/MyFolder/FamilyProject/FamilyStorage/static/default_photo.png',
              x=image_x, w=image_width)
    pdf.ln(5)

    for k, v in data.items():  # TODO + siblings and children
        pdf.set_font('Times', 'B', size=14)
        key = f"{k.title()}: "
        shift = pdf.l_margin + pdf.get_string_width(key) + 1

        if isinstance(v, str):
            v = v.replace('\u2013', '-').replace('\r\n', '\n').strip()  # TODO unicode
            pdf.cell(0, 10, txt=key, ln=0, align="L")

            pdf.set_x(shift)
            pdf.set_font('Times', size=14)
            if len(v) > 190:
                pdf.cell(0, 10, txt='', ln=1, align="L")
                pdf.multi_cell(0, 10, txt=f"{v or ''}", align="J")
            else:
                pdf.cell(0, 10, txt=f"{v or ''}", ln=1, align="L")
        else:
            pdf.cell(0, 10, txt=key, ln=0, align="L")

            pdf.set_x(shift)
            pdf.set_font('Times', size=14)
            pdf.cell(0, 10, txt=f"{v or ''}", ln=1, align="L")

    f_name = slugify(name) + '.pdf'
    path = STATIC_DIR / f_name

    if path.is_file():
        path.unlink()
    pdf.output(str(path))

    return f_name
