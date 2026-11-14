# Issue #15753: Bug: num_digits_fast() returns incorrect digit count for large integers
https://github.com/TheAlgorithms/Python/issues/15753
state: open  labels: bug

### Repository commit

30507bbe41397065728167fb09aa820f9fce8dc7

### Python version (python --version)

Python 3.14.4

### Dependencies version (pip freeze)

```text
aptdaemon==2.0.2
attrs==25.4.0
autocommand==2.2.2
babel==2.17.0
bcc==0.35.0
bcrypt==5.0.0
blinker==1.9.0
Brlapi==0.8.6
certifi==2026.1.4
chardet==5.2.0
click==8.1.8
command-not-found==0.3
configobj==5.0.9
cryptography==46.0.5
cupshelpers==1.0
dasbus==1.7
dbus-python==1.4.0
defer==1.0.6
distro==1.9.0
distro-info==1.15
gyp-next==0.16.2
httplib2==0.22.0
idna==3.11
inflect==7.5.0
jaraco.context==6.0.1
jaraco.functools==4.1.0
jaraco.text==4.0.0
Jinja2==3.1.6
jsonpatch==1.32
jsonpointer==2.4
jsonschema==4.19.2
jsonschema-specifications==2023.12.1
language-selector==0.1
launchpadlib==2.1.0
lazr.restfulclient==0.14.6
lazr.uri==1.0.6
libpass==1.9.3
linkify-it-py==2.0.3
louis==3.36.0
markdown-it-py==3.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
more-itertools==10.8.0
netaddr==1.3.0
oauthlib==3.3.1
olefile==0.47
packaging==26.0
pexpect==4.9.0
pillow==12.1.1
pip==25.1.1
psutil==7.1.0
ptyprocess==0.7.0
pycairo==1.27.0
pycups==2.0.4
Pygments==2.19.2
PyGObject==3.56.2
PyJWT==2.10.1
pyparsing==3.3.2
pyserial==3.5
python-apt==3.1.0+ubuntu1.1
python-debian==1.0.1+ubuntu2
pyxdg==0.28
PyYAML==6.0.3
referencing==0.36.2
requests==2.32.5
rich==13.9.4
rpds-py==0.27.1
screen-resolution-extra==0.0.0
setproctitle==1.3.7
setuptools==78.1.1
systemd-python==235
typeguard==4.4.4
typing_extensions==4.15.0
ubuntu-drivers-common==0.0.0
ubuntu-pro-client==8001
uc-micro-py==1.0.3
ufw==0.36.2
unattended-upgrades==0.1
urllib3==2.6.3
wadllib==2.0.0
wheel==0.46.3
xdg==5
xkit==0.0.0
zipp==3.23.0
```

### Expected behavior

num_digits_fast(9999999999999999) should return 16,
because the input contains exactly 16 decimal digits.

It should agree with num_digits() and len(str(n)).

### Actual behavior

### Bug reproduction

The `num_digits_fast()` function in `maths/number_of_digits.py` incorrectly counts the digits of certain large integers.

**Steps to reproduce:**

```python
from maths.number_of_digits import num_digits_fast, num_digits

n = 10**16 - 1

print("Expected:", len(str(n)))
print("Actual:", num_digits_fast(n))
print("Standard implementation:", num_digits(n))
```

**Observed output:**

```text
Expected: 16
Actual: 17
Standard implementation: 16
```

### Possible cause

The function uses:

```python
math.floor(math.log(abs(n), 10) + 1)
```

Floating-point rounding near powers of ten can produce an off-by-one error.

### Suggested improvement

Consider using exact integer arithmetic or validating the logarithmic estimate against integer powers of ten.

A regression test using `10**16 - 1` would help prevent this issue from recurring.

### Environment

- Python: 3.14.4
- Repository commit: `30507bbe41397065728167fb09aa820f9fce8dc7`
- Third-party dependencies required: None

Related issue: #2220 introduced the motivation for the faster implementation through PR #2221. This report concerns correctness, not performance.

PR description must include: Fixes #15753
