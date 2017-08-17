from django.conf.urls import patterns, url

import oas.rpc

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('oas.rpc.engine',
                       (r'^jsonrpc/$', 'jsonrpc'),
                       (r'^jsonrpcsmd/$', 'jsonrpc_smd'),
                       )

urlpatterns += patterns('oas.views.googleauth',
                        (r'^google_login$', 'google_login'),
                        (r'^google_logout$', 'google_logout'),
                        )

urlpatterns += patterns('oas.views',
                        (r'^$', 'index'),
                        (r'^testpage$', 'test_page'),
                        (r'^disp_entity/(?P<legal_entity_code>\w+)/$', 'display_legal_entity'),
                        (r'^entry/(?P<legal_entity_code>\w+)/$', 'journal_entry'),
                        (r'^disp_accounts/(?P<legal_entity_code>\w+)/$', 'manage_accounts'),
                        (r'^import_accounts/(?P<legal_entity_code>\w+)/$', 'import_accounts'),
                        (r'^export_accounts/(?P<legal_entity_code>\w+)/$', 'export_accounts'),
                        (r'^disp_journal/(?P<legal_entity_code>\w+)/$', 'display_journal'),
                        (r'^save_entity/(?P<legal_entity_code>\w+)/$', 'save_legal_entity'),
                        (r'^remove_entity/(?P<legal_entity_code>\w+)/$', 'delete_legal_entity'),
                        (r'^upload_accounts/(?P<legal_entity_code>\w+)/$', 'upload_accounts_file'),
                        (r'^create_entity$', 'create_legal_entity'),
                        ###### OLD URLS BELOW
                        (r'^profile/(?P<entity_code>\w+)/$', 'company_profile'),
                        (r'^manageacct/(?P<entity_code>\w+)/create/$', 'create_account'),
                        (r'^manageacct/(?P<entity_code>\w+)/(?P<account_code>.+)/save/$', 'save_account'),
                        (r'^manageacct/(?P<entity_code>\w+)/select/$', 'select_account'),
                        (r'^manageacct/(?P<entity_code>\w+)/select/(?P<account_code>.+)/$', 'select_account'),
                        (r'^compadmin$', 'admin_entities'),
                        (r'^clean_journal$', 'clean_journal'),

                        # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
                        # to INSTALLED_APPS to enable admin documentation:
                        # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        # Uncomment the next line to enable the admin:
                        # (r'^admin/', include(admin.site.urls)),
                        )
