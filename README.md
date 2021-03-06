# Cplugins

Dev framework for nagios like check plugins writen in python.

## Developemnt

You can use pipenv to generate a specific virtualenv:

```bash
pipenv --three install -e .
```

## Documentation

Modules documentation can be found here: [doc](docs/cplugins)

This documentation is generated with the following commnd:

```bash
pipenv run pdoc --html --overwrite --html-dir docs cplugins
```

## Features

- generate well formated output (short, long and performances data), compliant with Centreon, Nagios, etc
- ability to use external SDK (boto3 for AWS, etc ...)

## Usage

1. Copy or clone this repo to your nagios plugins directory
2. Add a cplugins_notifications.json file for notifications (default is in "/etc/centreon/cplugins_notifications.json")

### Notifications

To receive a notificaation with the accurate informations, you have to supply the nagios variables in that order to the "-p" switch:

- '0': 'host_name'
- '1': 'host_state'
- '2': 'host_output'
- '3': 'host_ack_author'
- '4': 'host_ack_comment'
- '5': 'service_desc'
- '6': 'service_state'
- '7': 'service_output'
- '8': 'service_ack_author'
- '9': 'service_ack_comment'
- '10': 'notification_type'
- '11': 'long_date_time'

Example of notification command in Centreon:

```bash
$USER1$/cplugins/cplugins-notification-email.py -H localhost -c $USER1$/cplugins/cplugins_notifications.json --to $CONTACTEMAIL$ -p '$HOSTNAME$' '$HOSTSTATE$' '$HOSTOUTPUT$' '$HOSTACKAUTHOR$' '$HOSTACKCOMMENT$' '$SERVICEDESC$' '$SERVICESTATE$' '$SERVICEOUTPUT$' '$SERVICEACKAUTHOR$' '$SERVICEACKCOMMENT$' '$NOTIFICATIONTYPE$' '$LONGDATETIME$'
```

Example of received email (design inherited from [centreon-notifications](https://github.com/Shini31/centreon-notifications)):

- Email UP/OK

![Email UP/OK](/docs/images/email-ok.png)

- Email Down/Critical

![Email Down/Critical](/docs/images/email-down.png)

- Email Unknown/Other

![Email Unknown/Other](/docs/images/email-unknown.png)

### Examples

| File                           | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| cplugins_aws_list_instances.py | simple nagios check to list AWS EC2                |
| cplugins_check_ssl.py          | Check SSL certificate validy for a website         |
| cplugins_http.py               | simple nagios check to get a website response time |
| cplugins_notification_email.py | Send formated email notifications                  |
| cplugins_check_template.py     | sample file to used as reference                   |

## ToDo

- add templates for notifications
