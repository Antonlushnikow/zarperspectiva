import xlwt

from django.http import HttpResponse
from mainapp.models import Course


def export_courses_to_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Price.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Прайс-лист')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    row_num = 0

    columns = [
        'Курс',
        'Цена за занятие',
        'Цена за занятие в группе',
        'Цена за месяц',
        'Цена за месяц в группе',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = Course.objects.all().values_list(
        'title',
        'price_once_alone',
        'price_once_group',
        'price_pass_alone',
        'price_pass_group',
    )

    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    ws.col(0).width = 12000
    ws.col(1).width = 5000
    ws.col(2).width = 5000
    ws.col(3).width = 5000
    ws.col(4).width = 5000

    wb.save(response)

    return response
