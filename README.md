# statsviewer

Periodically store system statistics in a Round-Robin Database
and display them using a Flask server

![image](https://user-images.githubusercontent.com/16620882/206309294-c71309bc-ec87-4e06-a086-36bbd78cf802.png)

## Installation

Install the dependencies:
```
rrdtool-devel\
python3-devel
```
using whatever package manager fits your setup.

Fedora Example:
```
dnf install rrdtool-devel\
python3-devel`
```

Install the Python requirements using `pip install -r requirements.txt`

After that, clone the repository and install it from inside using pip

```
git clone https://github.com/SuperKaninchen/StatsViewServer
cd StatsViewServer-main
pip install .
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

### Step Four

Open the IP shown by Flask inside a web browser. You should see something similar to the image above.
