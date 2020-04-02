
def sort_months(querysets):
    months = []
    for queryset in querysets:
        for ele in queryset:
            if ele['month'] not in months:
                months.append(ele['month'])
    return sorted(months)


def create_data_for_chart(payment_analysis, month_analysis):
    months = sort_months([payment_analysis, month_analysis])
    result_per_months = []
    for month in months:
        data = {
            'month': month,
            'total': 0
        }
        for ele in payment_analysis:
            if ele['month'] == month:
                data['payments'] = ele['total']
        for ele in month_analysis:
            if ele['month'] == month:
                data['invoices'] = ele['total']
        # put the data together
        data['payments'] = data['payments'] if 'payments' in data.keys() else 0
        data['invoices'] = data['invoices'] if 'invoices' in data.keys() else 0
        result_per_months.append(data)
    return result_per_months







