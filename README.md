# Compare_and_Move
Computes file hashes for all files in a directory. 
If there are multiple matching hashes it will move all but one of those files to a user specified directory
Saves hashes to a .json file
Next time the script is ran it will use those hashes as a reference to speed up the process

## Usage

```
Fill out the paths to the source and output directories

then run:
python3 main.py
```
## Dependencies

- hashlib
- argparse
- os
- json
