import csv
from num2words import num2words
import pdfkit
import os

from jinja2 import Template

state_codes = {
    'andaman and nicobar islands': '35',
    'andhra pradesh': '37',
    'arunachal pradesh': '12',
    'assam': '18',
    'bihar': '10',
    'chandigarh': '04',
    'chhattisgarh': '22',
    'dadra and nagar haveli and daman and diu': '26',
    'delhi': '07',
    'new delhi': '07',
    'goa': '30',
    'gujarat': '24',
    'haryana': '06',
    'himachal pradesh': '02',
    'jammu and kashmir': '01',
    'jharkhand': '20',
    'karnataka': '29',
    'kerala': '32',
    'ladakh': '37',
    'lakshadweep': '31',
    'madhya pradesh': '23',
    'madhyapradesh': '23',
    'maharashtra': '27',
    'manipur': '14',
    'meghalaya': '17',
    'mizoram': '15',
    'nagaland': '13',
    'odisha': '21',
    'puducherry': '34',
    'punjab': '03',
    'rajasthan': '08',
    'sikkim': '11',
    'tamil nadu': '33',
    'telangana': '36',
    'tripura': '16',
    'uttar pradesh': '09',
    'uttarakhand': '05',
    'west bengal': '19',
}

error_rows={}

sold_by='Moonfinity Fashions Pvt. Ltd.</br>B-2, M. P. Shah Industrial Estate, Saru Section Road JAMNAGAR, GUJARAT, 361008 IN'
pan_no= 'AAOCM0994J'
gst_no='24AAOCM0994J1Z0'

with open('invoice_template_b2b.html', 'r') as template_file:
    template_content = template_file.read()

template = Template(template_content)
folder_name = 'invoices'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
with open('b2b.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            total_amount=float(row['INVOICE AMOUNT'])
            gst_percent_str = str(row['GST% on this product'])
            gst_percent = int(gst_percent_str)

            total_amount_word = num2words(int(total_amount),lang='en').replace("-", " ")
            unit_price = round(total_amount/(1+(gst_percent/100)),2)
            is_igst= 'Yes'
            igst_price='0.00'
            icsgst_price='0.00'
            
            if is_igst == 'Yes':
                igst_price = round(total_amount-unit_price,2)
            else:
                icsgst_price = round((total_amount-unit_price)/2,2)
            

            state = row['STATE'] if row['STATE'] != '0' else 'Karnataka'
            city = row['CITY'] if row['CITY'] !=0 else 'BENGALURU'
            pincode = row['Pin'] if row['Pin'] !=0 else '560017'
            # break
            rendered_html = template.render(
                sold_by=sold_by,
                pan_no=pan_no,
                gst_no=gst_no,
                state=state,
                city=city,
                pincode=pincode,
                state_code=state_codes.get(row['STATE'].lower()),
                invoice_number=row['Invoice Number'],
                invoice_date=row['Order Date'],
                order_number=row['Order ID'],
                order_date=row['Order Date'],
                quantity=row.get('Quantity', '1'),
                description=row.get('Product Name', 'NA'),
                unit_price=unit_price,
                total_amount= "{:.2f}".format(total_amount),
                igst_price=igst_price,
                icsgst_price=icsgst_price,
                igst_percent=gst_percent,
                icsgst_percent=round(float(gst_percent/2),2),
                total_amount_word=total_amount_word.title(),
                )
            
            pdf_file = os.path.join(folder_name, f"{row['Invoice Number']}_invoice.pdf")
            pdfkit.from_string(rendered_html, pdf_file, options={'page-size': 'A4'})
            # with open('rendered_invoice.html', 'w') as output_file:
            #     output_file.write(rendered_html)
        except Exception as e:
            error_rows[row['Invoice Number']]=e
        # break                               

print(error_rows)
# with open('rendered_invoice.html', 'w') as output_file:
#     output_file.write(rendered_html)
