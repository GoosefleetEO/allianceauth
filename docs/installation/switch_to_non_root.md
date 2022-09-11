# Switch to non-root

If you followed the official installation guide for Alliance Auth (AA) pre AA 3.x you usually ended up with a "root installation". A root installation means that you have installed AA with the root user and now need to log in as root every time to perform maintenance for AA, e.g. updating existing apps.

Since working as root is [generally not recommended](https://askubuntu.com/questions/16178/why-is-it-bad-to-log-in-as-root), this guide explains how you can easily migrate your existing "root installation" to a "non-root installation".

## How to switch to non-root

We will change the setup so that you can use your `allianceserver` user to perform most maintenance operations. In addition, you also need a sudo user for invoking root privileges, e.g. when restarting the AA services.

The migration itself is rather straightforward. The main idea is to change ownership for all relevant directories and files to `allianceserver`.

First, log in as your sudo user and run the following commands in order:

```shell
sudo chown -R allianceserver: /home/allianceserver
sudo chown -R allianceserver: /var/www/myauth
sudo chmod -r 655 /var/www/myauth
```

That's it. Your AA installation is now configured to be maintained with the `allianceserver` user.

## How to do maintenance with a non-root user

Here is how you can maintain your AA installation in the future:

First, log in with your sudo user.

Then, switch to the `allianceserver` user:

```shell
sudo su allianceserver
```

Go to your home folder and activate your venv:

```shell
cd ~
source venv/auth/bin/activate
```

Finally, switch to the main AA folder, from where you can run most commands directly:

```shell
cd myauth
```

When you want to restart myauth, you need to switch back to your sudo user, because `allianceserver` does not have sudo privileges:

```shell
exit
sudo supervisorctl restart myauth:
```

Alternatively, you can open another terminal with your sudo user for restarting myauth. That has the added advantage that you can now continue working with both your allianceauth user and your sudo user for restarts at the same time.
