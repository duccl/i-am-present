# i-am-present
A script to automate presence check

# How to use

Firstly, you need to have `Python3.9.x` or `Python3.7.x` on your machine.

Secondly, just run the follwing command to install the packages

```python
pip install -r requirements.txt
```

Last but not least, import the `marcar_presenca` for your script and just call it with your FEI login.

```pyhton
from lambda_function import marcar_presenca

marcar_presenca('MYSUPERUSER','MYSUPERPASSWORD')
```