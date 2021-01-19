#! /usr/bin/env python
def _nothing(x):
    return x
from fbapp import app

if __name__ == "__main__":
    def _nothing(x):
        return x
    app.run(debug=True)
