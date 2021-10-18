# Analytics FAQ

**Alliance Auth** has an opt-out analytics module using [Google Analytics Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/v1/).

## How to Opt-Out

Before you proceed, please read through this page and/or raise any concerns on the Alliance Auth discord. This data helps us make AA better.

To Opt-Out, modify our pre-loaded token using the Admin dashboard */admin/analytics/analyticstokens/1/change/

Each of the three features Daily Stats, Celery Events and Page Views can be enabled/Disabled independently.

![Analytics Tokens](/_static/images/features/core/analytics/tokens.png)

## What

Alliance Auth has taken great care to anonymize the data sent. In order to identify _unique_ installs we generate a UUIDv4, a random mathematical construct which does not contain any identifying information [UUID - UUID Objects](https://docs.python.org/3/library/uuid.html#uuid.uuid4)

Analytics comes pre-loaded with our Google Analytics Token, and the Three Types of task can be opted out independently. Analytics can also be loaded with your _own_ GA token and the analytics module will act any/all tokens loaded.

Our Daily Stats contain the following:

- A phone-in task to identify a servers existence
- A task to send the Number of User models
- A task to send the Number of Token Models
- A task to send the Number of Installed Apps
- A task to send a List of Installed Apps
- Each Task contains the UUID and Alliance Auth Version

Our Celery Events contain the following:

- Unique Identifier (The UUID)
- Celery Namespace of the task eg allianceauth.eveonline
- Celery Task
- Task Success or Exception
- A context number for bulk tasks or sometimes a binary True/False

Our Page Views contain the following:

- Unique Identifier (The UUID)
- Page Path
- Page Title
- The locale of the users browser
- The User-Agent of the users browser
- The Alliance Auth Version

## Why

This data allows Alliance Auth development to gather accurate statistics on our install base, as well as how those installs are used.

This allows us to better target our development time to commonly used modules and features and test them at the scales in use.

## Where

This data is stored in a Team Google Analytics Dashboard. The Maintainers all have Management permissions here, and if you have contributed to the Alliance Auth project or third party applications feel free to ask in the Alliance Auth discord for access.

## Using Analytics in my App

### Analytics Event

.. automodule:: allianceauth.analytics.tasks
    :members: analytics_event
    :undoc-members:
