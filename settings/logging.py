def get_logging_configuration(debug=False, debug_db=False):
    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'oracle.management': {
                'handlers': ['console'],
                'level': debug and 'DEBUG' or 'INFO',
                'propagate': False,
            },
        }
    }
    if debug and debug_db:
        logging['loggers']['django.db'] = {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    return logging
