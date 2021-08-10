from django.core.exceptions import ValidationError
import re, os

def min_length(value):
    if len(value) < 1:
        raise ValidationError('Please use at least 1 character.')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.txt', '.doc', '.docx', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension!')

def deny_href(value):
    linksList = ['href=', 'src=', '<a>', '</a>', '<embed>', '</embed>', '<iframe>', '</iframe>']
    pattern = re.compile(
        r'(%s)' % '|'.join(linksList),
        re.IGNORECASE,
    )
    ocurrencies = pattern.findall(str(value))
    if  len(ocurrencies) > 0:
        raise ValidationError('Please, if you want to use links to other pages, just copy them in the text field.')
