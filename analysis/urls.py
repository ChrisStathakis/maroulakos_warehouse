from django.urls import path

from .views import AnalysisHomepage, AnalysisSaleIncomeView, AnalysisOutcomeView, CashRowView, BalanceSheetView, StoreInventoryView, warehouse_movements_view

app_name='analysis'

urlpatterns = [
    path('homepage/', AnalysisHomepage.as_view(), name='homepage'),
    path('incomes/', AnalysisSaleIncomeView.as_view(), name='income_analysis'),
    path('warehouse/movements/', warehouse_movements_view, name='warehouse_movements'),
    path('outcomes/', AnalysisOutcomeView.as_view(), name='outcome_analysis'),
    path('cash-row/', CashRowView.as_view(), name='cash_row'),
    path('balance-sheet/', BalanceSheetView.as_view(), name='balance_sheet'),
    path('apografi/', StoreInventoryView.as_view(), name='store_inventory')
    
]