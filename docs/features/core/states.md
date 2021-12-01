# States

States define the basic role of a user based on his affiliation with your organization. A user that has a character in your organization (e.g. alliance) will usually have the `Member` state. And a user, that has no characters in your organization will usually have the `Guest` state.

States are assigned and updated automatically. So a user which character just left your organization will automatically loose his `Member` state and get the `Guest` state instead.

The main purpose of states like `Member` is to have one place where you can assign all permissions that should apply to all users with that particular state. For example if all your members should have access to the SRP app you would add the permission that gives access to the SRP app to the `Member` state.

## Creating a State

States are created through your installation's admin site. Upon install three states are created for you: `Member`, `Blue`, and `Guest`. New ones can be created like any other Django model by users with the appropriate permission (`authentication | state | Can add state`) or superusers.

A number of fields are available and are described below.

### Name

This is the displayed name of a state. Should be self-explanatory.

### Permissions

This lets you select permissions to grant to the entire state, much like a group. Any user with this state will be granted these permissions.

A common use case would be granting service access to a state.

### Priority

This value determines the order in which states are applied to users. Higher numbers come first. So if a random user `Bob` could member of both the `Member` and `Blue` states, because `Member` has a higher priority `Bob` will be assigned to it.

### Public

Checking this box means this state is available to all users. There isn't much use for this outside the `Guest` state.

### Member Characters

This lets you select which characters the state is available to. Characters can be added by selecting the green plus icon.

### Member Corporations

This lets you select which Corporations the state is available to. Corporations can be added by selecting the green plus icon.

### Member Alliances

This lets you select which Alliances the state is available to. Alliances can be added by selecting the green plus icon.

### Member Factions

This lets you select which factions the state is available to. Factions can be added by selecting the green plus icon, and are limited to those which can be enlisted in for faction warfare.

## Determining a User's State

States are mutually exclusive, meaning a user can only be in one at a time.

Membership is determined based on a user's main character. States are tested in order of descending priority - the first one which allows membership to the main character is assigned to the user.

States are automatically assigned when a user registers to the site, their main character changes, they are activated or deactivated, or states are edited. Note that editing states triggers lots of state checks so it can be a very slow process.

Assigned states are visible in the `Users` section of the `Authentication` admin site.

## The Guest State

If no states are available to a user's main character, or their account has been deactivated, they are assigned to a catch-all `Guest` state. This state cannot be deleted nor can its name be changed.

The `Guest` state allows permissions to be granted to users who would otherwise not get any. For example access to public services can be granted by giving the `Guest` state a service access permission.
