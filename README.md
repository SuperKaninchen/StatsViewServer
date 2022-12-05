statsviewer

Periodically store system statistics in a Round-Robin Database
and display them using a Flask server

![Uploading image.png…]()


## Installation

```
pip install statsviewer
```

## Usage

### Step One

use `statsviewer init /path/to/database.rrd`, with the last argument
being the path where the Round-Robin Database will be created, to
initialize the RRD.

### Step Two

run `statsviewer record /path/to/database.rrd` to update the RRD every few seconds.

### Step Three

run `statsviewer serve /path/to/database.rrd` to start the flask server for displaying the stats
