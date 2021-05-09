from typing import Iterable

from fpdf import FPDF
from django.utils.text import slugify

from FamilyStorage.settings import STATIC_DIR, BASE_DIR


def generate_pdf(name, data, font_name='Times'):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    file_width = pdf.fw
    cells_width = file_width - pdf.l_margin - pdf.r_margin
    if font_name == 'DejaVu':
        pdf.add_font('DejaVu', '', BASE_DIR / 'fonts/DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', BASE_DIR / 'fonts/DejaVuSans-Bold.ttf', uni=True)
    text_size = 14
    cell_height = 10

    pdf.add_page()

    # Title
    pdf.set_font(font_name, 'B', size=20)
    pdf.cell(190, cell_height, txt=name, ln=1, align="C")
    pdf.ln(5)

    # Main photo
    image_width = 75
    image_x = cells_width / 2 - image_width / 2 + pdf.l_margin

    photo_path = data.get('photo')
    if photo_path:
        pdf.image(photo_path, x=image_x, w=image_width)
        pdf.ln(5)

    for k, v in data.items():
        if k == 'photo':
            continue

        pdf.set_font(font_name, 'B', size=text_size)
        key = f"{k.title()}: "
        shift = pdf.l_margin + pdf.get_string_width(key) + 1

        if isinstance(v, list) or isinstance(v, set):
            v = '\n'.join([str(i) for i in v])

        if isinstance(v, str):
            v = v.replace('\r\n', '\n').strip()
            pdf.cell(0, cell_height, txt=key, ln=0, align="L")

            pdf.set_x(shift)
            pdf.set_font(font_name, size=text_size)

            if len(v) > cells_width:
                pdf.cell(0, cell_height, txt='', ln=1, align="L")
            pdf.multi_cell(0, cell_height, txt=f"{v or ''}", align="J")
        else:
            pdf.cell(0, cell_height, txt=key, ln=0, align="L")

            pdf.set_x(shift)
            pdf.set_font(font_name, size=text_size)
            pdf.cell(0, cell_height, txt=f"{v or ''}", ln=1, align="L")

    return pdf


def get_pdf_name(name, data):
    pdf = generate_pdf(name, data, font_name='Times')

    f_name = slugify(name, allow_unicode=True) + '.pdf'
    path = STATIC_DIR / f_name

    path.unlink(missing_ok=True)

    try:
        pdf.output(str(path))
    except UnicodeEncodeError:
        pdf = generate_pdf(name, data, font_name='DejaVu')
        try:
            pdf.output(str(path))
        except UnicodeEncodeError:
            return ''

    return f_name
