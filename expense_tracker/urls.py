from django.contrib import admin
from django.urls import path
from .views.home import index
from .views.auth import register, doRegister, login, doLogin, forgetPass,logout
from .views.mode import getAllMode,processAddMode,processDeleteMode,processUpdateMode,updateMode,addMode
from .views.category import getAllCategory,processAddCategory,processDeleteCategory,processUpdateCategory,updateCategory,addCategory
from .views.transaction import getAllTransaction,processAddTransaction,processDeleteTransaction,processUpdateTransaction,addTransaction,updateTransaction
from .views.summary import getReportByType,importTransaction,processImportTransaction
urlpatterns = [
    path('index', getReportByType,name='index'),
    path('register/', register, name='register'),
    path('doRegister/', doRegister, name='doRegister'),
    path('login/', login, name='login'),
    path('doLogin/', doLogin, name='doLogin'),
    path('forgetPassword/', forgetPass, name='forgetPassword'),
    path('logout/',logout,name='logout'),
    #Mode
    path('mode/',getAllMode,name="mode"),
    path('mode/delete',processDeleteMode,name='processDeleteMode'),
    path('mode/add',addMode,name='addMode'),
    path('mode/process-add-Mode',processAddMode,name='processAddMode'),
    path('mode/edit',updateMode,name='updateMode'),
    path('mode/process-update-Mode',processUpdateMode,name='processUpdateMode'),
    # portfolio
    path('category/',getAllCategory,name="category"),
    path('category/delete',processDeleteCategory,name='processDeleteCategory'),
    path('category/add',addCategory,name='addCategory'),
    path('category/process-add-portfolio',processAddCategory,name='processAddCategory'),
    path('category/edit',updateCategory,name='updateCategory'),
    path('category/process-update-category',processUpdateCategory,name='processUpdateCategory'),
    #transaction
    path('transaction/',getAllTransaction,name="transaction"),
    path('transaction/delete',processDeleteTransaction,name='processDeleteTransaction'),
    path('transaction/add',addTransaction,name='addTransaction'),
    path('transaction/process-add-transaction',processAddTransaction,name='processAddTransaction'),
    path('transaction/edit',updateTransaction,name='updateTransaction'),
    path('transaction/process-update-transaction',processUpdateTransaction,name='processUpdateTransaction'),
    #report
    path ('report/',getReportByType,name='report'),
    path('import-report/',importTransaction,name='importTransaction'),
    path('import-report/process',processImportTransaction,name='processImportTransaction'),
]
