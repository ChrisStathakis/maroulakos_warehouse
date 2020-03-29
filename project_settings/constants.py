CURRENCY = '€'

INVOICE_TYPES = (
    ('a', 'Τιμολογιο'),
    ('b', 'Δελτιο Αποστολης'),
    ('c', 'Εισαγωγη στην Αποθηκη'),
    ('d', 'Εξαγωγη απο την Αποθηκη')
)

POSITIVE_INVOICES = ['a', 'b', 'c']
NEGATIVE_INVOICES = ['d']


SALE_INVOICE_TYPES = (
    ('a', 'Πωληση'),
    ('b', 'Τιμολογιο'),
)